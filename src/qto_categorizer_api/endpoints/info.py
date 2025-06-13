"""Info page."""

import pathlib
import fastapi
from fastapi.responses import PlainTextResponse

from qto_categorizer_api.endpoints.router import router

ENDPOINT_DESCRIPTION = """
Dump the content of the data/info.txt file when it exists.
The source for that info.txt file is
"""


@router.get(
    "/info",
    description=ENDPOINT_DESCRIPTION,
    status_code=fastapi.status.HTTP_200_OK,
    response_class=PlainTextResponse,
)
async def info():
    """Info route.

    Returns
    -------
    _type_
        _description_
    """
    file_content = None
    file_path = pathlib.Path("data/info.txt")
    if file_path.exists():
        with open(file_path, encoding="utf-8") as f:
            file_content = f.read()

    return file_content
