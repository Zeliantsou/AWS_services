
import zipfile


def create_zip_file_for_lambda_function(zip_file_path,
                                        writable_file_path,
                                        arc_name=None):
    with zipfile.ZipFile(zip_file_path, 'w') as zip_pointer:
        zip_pointer.write(writable_file_path, arc_name)


def get_zip_file_name(file_name):
    return file_name.split('.')[0] + '.zip'


def get_zip_file_path(directory_path_zip_storage,
                      file_name):
    return (directory_path_zip_storage +
            file_name.split('.')[0] + '.zip')


def get_writable_file_path(storage_directory, file_name):
    return storage_directory + file_name
