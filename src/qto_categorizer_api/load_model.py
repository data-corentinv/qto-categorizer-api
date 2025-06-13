""" """

import logging
import pathlib
from cachetools.func import ttl_cache
from typing import Union

from qto_categorizer_ml.io.registries import CustomLoader
from qto_categorizer_api.errors import APIModelNotLoadableError
from qto_categorizer_api.settings.app_settings import Settings


@ttl_cache(maxsize=1, ttl=86400)
def load_model(settings: Settings):
    """Load model.

    Parameters
    ----------
    settings : Settings
        _description_

    Returns
    -------
    _type_
        _description_

    Raises
    ------
    APIModelNotFoundError
        _description_
    APIModelNotLoadableError
        _description_
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.log_level)

    # categorizer_engine_uri = Union[str, pathlib.Path] = f"""
    #         models:/{settings.categorizer_engine_name}/{settings.categorizer_engine_version}
    #     """

    url_or_model_path: Union[str, pathlib.Path] = settings.url_or_model_path

    logger.info("[API::load_model] Machine Learning (ML) model: %s", {url_or_model_path})

    loader = CustomLoader()
    model = loader.load(uri=url_or_model_path)

    if not model:
        err_msg = (
            "[API::load_model] The model URI "
            "({url_or_model_path}) cannot be loaded back into memory"
        )
        raise APIModelNotLoadableError(err_msg)

    logging.info(
        "[API::load_model] The ML model has been successfully loaded from %s", {url_or_model_path}
    )

    return model
