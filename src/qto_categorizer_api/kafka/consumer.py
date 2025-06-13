"""Kafka consumer for prediction requests."""
import json
import logging
from typing import Dict, Any

import pandas as pd
from confluent_kafka import Consumer, KafkaError
from pydantic import BaseModel

from qto_categorizer_api.endpoints.predict import InputData
from qto_categorizer_api.settings.app_settings import Settings, get_settings
from qto_categorizer_api.load_model import load_model
from qto_categorizer_api.models import init_db, Prediction


class KafkaPredictionConsumer:
    """Kafka consumer for prediction requests."""

    def __init__(self, settings: Settings):
        """Initialize the consumer.

        Args:
            settings: Application settings
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(settings.log_level)
        self.settings = settings

        # Kafka configuration
        self.consumer_config = {
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'group.id': 'prediction-consumer-group',
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.consumer_config)
        self.topic = settings.kafka_prediction_topic

        # Load model
        self.model = load_model(settings=settings)

    def process_prediction(self, request: InputData) -> None:
        """Process a prediction request.

        Args:
            request: The prediction request to process
        """
        try:
            # Convert request to dict
            input_data = request.model_dump()

            # Prepare data for model
            data = pd.DataFrame.from_records([input_data])

            # Make prediction
            predictions = self.model.predict(data)

            # Store in database
            db = init_db(self.settings.database_url)()
            try:
                db_prediction = Prediction(
                    amount=input_data["AMOUNT"],
                    type_of_payment=input_data["TYPE_OF_PAYMENT"],
                    merchant_name=input_data["MERCHANT_NAME"],
                    description=input_data["DESCRIPTION"],
                    prediction=str(predictions[0]),
                    model_path=str(self.settings.url_or_model_path)
                )
                db.add(db_prediction)
                db.commit()
                self.logger.info(f"Prediction stored in database with ID: {db_prediction.id}")
            except Exception as e:
                self.logger.error(f"Failed to store prediction in database: {str(e)}")
                db.rollback()
            finally:
                db.close()
                
        except Exception as e:
            self.logger.error(f"Failed to process prediction: {str(e)}")
            raise

    def start_consuming(self):
        """Start consuming messages from Kafka."""
        self.consumer.subscribe([self.topic])
        
        try:
            while True:
                msg = self.consumer.poll(1.0)
                
                if msg is None:
                    continue
                    
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        self.logger.info('Reached end of partition')
                    else:
                        self.logger.error(f'Error: {msg.error()}')
                else:
                    try:
                        # Parse message
                        request_dict = json.loads(msg.value().decode('utf-8'))
                        request = InputData(**request_dict)
                        
                        # Process prediction
                        self.process_prediction(request)
                        
                    except Exception as e:
                        self.logger.error(f"Failed to process message: {str(e)}")
                        
        except KeyboardInterrupt:
            self.logger.info("Stopping consumer...")
        finally:
            self.consumer.close()


def main():
    """Main function to start the consumer."""
    settings: Settings = get_settings()
    consumer = KafkaPredictionConsumer(settings)
    consumer.start_consuming()


if __name__ == "__main__":
    main() 