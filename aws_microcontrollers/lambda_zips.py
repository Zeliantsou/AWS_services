
from os import listdir
import logging

from services.generic.generic_services import (
    get_zip_file_path,
    get_writable_file_path,
    create_zip_file_for_lambda_function
)


logger = logging.getLogger(__name__)


def generate_lambda_zips(
        directory_path_lambda: str,
        directory_path_zip_storage: str) -> None:
    """
    Generate zips for lambda functions.
    """
    try:
        for file_name in listdir(directory_path_lambda):
            zip_file_path = get_zip_file_path(
                directory_path_zip_storage=directory_path_zip_storage,
                file_name=file_name
            )
            writable_file_path = get_writable_file_path(
                storage_directory=directory_path_lambda,
                file_name=file_name
            )
            create_zip_file_for_lambda_function(
                zip_file_path=zip_file_path,
                writable_file_path=writable_file_path,
                arc_name=file_name
            )
    except Exception:
        message = 'Could not create zip files for lambda'
        logger.exception(message)
        raise
