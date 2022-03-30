
import zipfile


def create_zip_file_for_lambda_function(
        zip_file_path: str,
        writable_file_path: str,
        arc_name: str = None
) -> None:
    """
    Creates zip file for lambda function.
    """
    with zipfile.ZipFile(zip_file_path, 'w') as zip_pointer:
        zip_pointer.write(writable_file_path, arc_name)


def get_zip_file_name(file_name: str) -> str:
    """
    Gets zip file full name from python file name.
    """
    return file_name.split('.')[0] + '.zip'


def get_zip_file_path(
        directory_path_zip_storage: str,
        file_name: str) -> str:
    """
    Gets zip file path.
    """
    return (directory_path_zip_storage +
            file_name.split('.')[0] + '.zip')


def get_writable_file_path(
        storage_directory: str,
        file_name: str) -> str:
    """
    Gets path for python file for lambda function.
    """
    return storage_directory + file_name
