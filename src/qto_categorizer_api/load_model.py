import logging
import pickle
import pathlib
from cachetools.func import ttl_cache
from typing import Union


from qto_categorizer_api.errors import APIModelNotFoundError, APIModelNotLoadableError
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

    ai_model_external_url: Union[str, pathlib.Path] = settings.ai_model_external_url

    logger.info(
        "[API::load_model] Machine Learning (ML) model pickle file: %s", {ai_model_external_url}
    )

    # Read the Pickled model from the file-system
    model_filepath = pathlib.Path(ai_model_external_url)
    model = None
    if not model_filepath.exists():
        err_msg = "[API::load_model] The model file (%s) cannot be found"
        raise APIModelNotFoundError(err_msg, {model_filepath})

    with open(model_filepath, "rb") as f:
        logging.info("[API::load_model] Load model from %s ...", {model_filepath})
        model = pickle.load(f)

    if not model:
        err_msg = (
            "[API::load_model] The model file "
            "({model_filepath}) cannot be loaded back into memory"
        )
        raise APIModelNotLoadableError(err_msg)

    logging.info(
        "[API::load_model] The ML model has been successfully loaded from %s", {model_filepath}
    )

    return model
