""" Health route.
"""
import fastapi

from qto_categorizer_api.endpoints.router import router

ENDPOINT_DESCRIPTION = """
Returns "OK" with a 200 status code (meaning that everything is fine).

That API endpoint may be used for instance for livelyness and readyness probes.
"""


@router.get("/health", description=ENDPOINT_DESCRIPTION, status_code=fastapi.status.HTTP_200_OK)
async def health() -> str:
    """Health route.

    Returns
    -------
    str
        "return OK"
    """
    return "OK"
