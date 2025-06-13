"""Root endpoint."""

import fastapi

from qto_categorizer_api.endpoints.router import router

ENDPOINT_DESCRIPTION = """
Returns the description of the project.
"""


@router.get("/", description=ENDPOINT_DESCRIPTION, status_code=fastapi.status.HTTP_200_OK)
async def default() -> str:
    """Default route.

    Returns
    -------
    str
        return info message
    """
    return "API - Powered by Qto categorizer Team"
