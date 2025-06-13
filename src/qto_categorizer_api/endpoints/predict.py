""" Predict route.
"""
from typing import Any

import logging
import pydantic
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from qto_categorizer_api.settings.app_settings import Settings, get_settings
from qto_categorizer_api.endpoints.router import router
from qto_categorizer_api.load_model import load_model
from qto_categorizer_api.models import init_db, Prediction

#
class InputData(pydantic.BaseModel):
    """ InputData format.
    """
    AMOUNT: float = 3.36
    TYPE_OF_PAYMENT: str = "Direct Debit"
    MERCHANT_NAME: str = "Qonto"
    DESCRIPTION: str = "Transaction Carte One En Devise Étrangère - fx_card"

ENDPOINT_DESCRIPTION = (
    "Expose machine learning system designed to automatically categorize financial transactions."
)

def log_api_call_in_db(input_data: dict, predictions, settings: Settings, logger: Any):
    """ Log each API call in db for traceability.
    """
    db = init_db(settings.database_url)()
    try:
        db_prediction = Prediction(
            amount=input_data["AMOUNT"],
            type_of_payment=input_data["TYPE_OF_PAYMENT"],
            merchant_name=input_data["MERCHANT_NAME"],
            description=input_data["DESCRIPTION"],
            prediction=str(predictions[0]),
            model_path=str(settings.url_or_model_path)
        )
        db.add(db_prediction)
        db.commit()
        logger.info("[API::predict] Prediction stored in database with ID: %s", db_prediction.id)
    except SQLAlchemyError as e:
        logger.error("[API::predict] Failed to store prediction in database: %s", str(e))
        db.rollback()
    finally:
        db.close()

@router.post("/predict", description=ENDPOINT_DESCRIPTION)
def predict(request_data: InputData) -> dict:
    """Predict the output based on the input data.

    Args:
        request_data (InputData): The input data for the prediction.

    Returns:
        dict: The output of the prediction.
    """
    settings: Settings = get_settings()

    logger = logging.getLogger(__name__)
    logger.setLevel(settings.log_level)

    logger.info("[API::predict] Request data %s", request_data)

    input_data = request_data.model_dump()
    logger.info("[API::predict] Input data: %s", input_data)

    # Read the Pickled model from the file-system
    model = load_model(settings=settings)

    # Prepare the data for the model
    data = pd.DataFrame.from_records([input_data])

    # Make the prediction
    predictions = model.predict(data)
    logger.info(predictions)

    # Basic example of how to return the predictions
    output = {}
    output["predictions"] = predictions[0]

    # Store prediction in database
    log_api_call_in_db(
        input_data=input_data,
        predictions=predictions,
        settings=settings,
        logger=logger
    )

    logger.info("[API::predict] Prediction made: %s", output)

    return output
