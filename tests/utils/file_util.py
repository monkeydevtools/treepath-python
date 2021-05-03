import os

"""
Utility for common test methods

"""


def find_file(file_to_find):
    """
    Recursively searches up the path for the specified file
    :param file_to_find: the file name  or  event the subpath + file_name
    :return: The fully qualified path to the existing file
    :raise ValueError if the file cannot be found
    """
    current_folder = os.getcwd()
    last_folder = None
    while current_folder != last_folder:
        file_path = os.path.join(current_folder, file_to_find)
        if os.path.exists(file_path):
            return file_path
        last_folder = current_folder
        current_folder = os.path.dirname(current_folder)

    raise ValueError("cannot find: '%s'. expecting it to be under test folder." % file_to_find)



