""" Predict route.
"""
import logging
import pydantic

import pandas as pd


from qto_categorizer_api.settings.app_settings import Settings, get_settings
from qto_categorizer_api.endpoints.router import router
from qto_categorizer_api.load_model import load_model

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


@router.post("/predict", description=ENDPOINT_DESCRIPTION)
def predict(request_data: InputData) -> dict:
    """Predict the output based on the input data.

    Args:
        request_data (InputData): The input data for the prediction.

    Returns:
        dict: The output of the prediction.
    """
    print('heloo')
    print(request_data)
    settings: Settings = get_settings()

    logger = logging.getLogger(__name__)
    logger.setLevel(settings.log_level)

    logger.info(f"[API::predict] Request data {request_data}")

    #input_data = request_data.dict()
    input_data = request_data.model_dump()
    logger.info(f"[API::predict] Input data: {input_data}")

    # Read the Pickled model from the file-system
    model = load_model(settings=settings)

    # Prepare the data for the model
    data = pd.DataFrame.from_records([input_data])

    # Make the prediction
    predictions = model.predict(data)

    # Basic example of how to return the predictions
    output = {}
    output["predictions"] = predictions[0]

    logger.info("[API::predict] Prediction made: %s, {output}")

    #
    return output
