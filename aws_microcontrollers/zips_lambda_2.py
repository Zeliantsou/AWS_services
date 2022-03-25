
from os import listdir

from services.generic.generic_services import (
    get_zip_file_path,
    get_writable_file_path,
    create_zip_file_for_lambda_function
)


def generate_zips_lambda(directory_path_lambda,
                         directory_path_zip_storage):

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


if __name__ == '__main__':
    import settings
    generate_zips_lambda(
        directory_path_lambda=settings.DIRECTORY_PATH_LAMBDA,
        directory_path_zip_storage=settings.DIRECTORY_PATH_ZIP_STORAGE
    )
