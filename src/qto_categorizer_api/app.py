import fastapi

from qto_categorizer_api import __version__
from qto_categorizer_api.endpoints import root, health, info, test, predict

#
app = fastapi.FastAPI(
    title="API",
    description="Expose machine learning system designed to automatically categorize financial transactions",
    version=__version__,
)

# Register the endpoints. See the endpoints/ directory
# for the corresponding source code.
app.include_router(root.router)
app.include_router(health.router)
app.include_router(info.router)
app.include_router(test.router)
app.include_router(predict.router)
