"""Test route."""

import fastapi

from qto_categorizer_api.endpoints.router import router

DEFAULT_OUTPUT = {
    "category_example": {"type": "str", "category": "Bank Fees & Charges: Other Bank Charges"},
}


def format_output_json(dict_):
    """
    Transform the dict with example keys and into format as json.

     :param dict_:
     :return:
    """
    result = {key: value["category"] for key, value in dict_.items()}
    return result


ENDPPOINT_DESCRIPTION = """
Returns a default dictionary of values, normally with the same format as
ordinary predictions.
"""


@router.get("/test", description=ENDPPOINT_DESCRIPTION, status_code=fastapi.status.HTTP_200_OK)
async def test() -> dict:
    """Test/example route.

    Returns
    -------
    dict
        Format return
    """
    output_data = format_output_json(DEFAULT_OUTPUT)
    return output_data
