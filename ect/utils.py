import logging
import os

LOGGER = logging.getLogger(__name__)


def get_last_string(string: str) -> str:
    """
    Gets last element of string consisting of /.

    Args:
        string (str): string consisting of /.

    Returns:
        Last element of string.
    """
    last_string = string.split("/")[-1]

    return last_string


def get_root_path() -> str:
    """
    Gets the root path of the user.
    """
    current_working_path = os.path.abspath(os.curdir)

    return current_working_path


def get_path_of_dir(starting_path: str, dir_name: str) -> str:
    """
    Gets path of directory to be found.

    Return:
        starting_path (str): Starting path to search from.
        dir_name (str): directory name to be found.

    Returns:
        The path of the directory name.
    """
    for root, dirs, files in os.walk(os.path.abspath(starting_path)):
        for name in dirs:
            if name == dir_name:
                path = os.path.abspath(os.path.join(root, name))
                return path

            else:
                continue

    raise ValueError(
        f"No dir_name '{dir_name}' found from starting_path '{starting_path}'"
    )


def get_files_from_dir(
    path: str, folders_to_include: list, folders_to_exclude: list
) -> list:
    """
    Gets all files from the directory of interest.

    path (str): Path to search from.
    folders_to_include (list): list of folders to include in the file search.
    folders_to_exclude (list): list of folders to exclude in the file search.

    returns:
        List of files from the directory of interest.
    """
    list_of_file_paths = []

    for root, dirs, files in os.walk(os.path.abspath(path)):
        directories_of_root_path = root.split("/")
        if folders_to_include:
            search = any(
                [folder in directories_of_root_path for folder in folders_to_include]
            )
        else:
            search = True

        if folders_to_exclude:
            not_search = any(
                [folder in directories_of_root_path for folder in folders_to_exclude]
            )
        else:
            not_search = False

        if search and not not_search:
            root_directory = get_last_string(root)
            for file in files:
                combined_file_path = root_directory + "/" + file
                list_of_file_paths.append(combined_file_path)

    return sorted(list_of_file_paths)
