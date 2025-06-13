"""Kafka producer for prediction requests."""

import json
import logging

from confluent_kafka import Producer

from qto_categorizer_api.settings.app_settings import Settings, get_settings
from qto_categorizer_api.endpoints.predict import InputData


class KafkaPredictionProducer:
    """Kafka producer for prediction requests."""

    def __init__(self, settings: Settings):
        """Initialize the producer.

        Args:
            settings: Application settings
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(settings.log_level)

        # Kafka configuration
        self.producer_config = {
            "bootstrap.servers": settings.kafka_bootstrap_servers,
            "client.id": "prediction-producer",
        }
        self.producer = Producer(self.producer_config)
        self.topic = settings.kafka_prediction_topic

    def delivery_report(self, err, msg):
        """Handle delivery reports."""
        if err is not None:
            self.logger.error(f"Message delivery failed: {err}")
        else:
            self.logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send_prediction_request(self, request: InputData) -> None:
        """Send a prediction request to Kafka.

        Args:
            request: The prediction request to send
        """
        try:
            # Convert request to JSON
            request_dict = request.model_dump()

            # Produce message
            self.producer.produce(
                self.topic, json.dumps(request_dict).encode("utf-8"), callback=self.delivery_report
            )

            # Wait for any outstanding messages to be delivered
            self.producer.flush()
            self.logger.info(f"Sent prediction request: {request_dict}")

        except Exception as e:
            self.logger.error(f"Failed to send prediction request: {str(e)}")
            raise


def main():
    """Main function to demonstrate producer usage."""
    settings = get_settings()
    producer = KafkaPredictionProducer(settings)

    # Example prediction request
    request = InputData(
        AMOUNT=3.36,
        TYPE_OF_PAYMENT="Direct Debit",
        MERCHANT_NAME="Qonto",
        DESCRIPTION="Transaction Carte One En Devise Étrangère - fx_card",
    )

    producer.send_prediction_request(request)


if __name__ == "__main__":
    main()
