import logging

import numpy as np
import toml
import filecmp

from ect import constants
from ect.utils import get_files_from_dir, get_path_of_dir, get_root_path, get_file_name_file_path_dict

LOGGER = logging.getLogger(__name__)


def compare_files(left_name_env: str, right_name_env: str, name_dir: str) -> None:
    """
    Compares the list of files from environment left with environment right.
    If there is no difference, the logger will say SUCCESS. If there is a difference,
    the logger will say an error, and list the differences between the two environments.

    Args:
        left_name_env (str): name of left environment for comparison.
        right_name_env (str): name of right environment for comparison.
        name_dir (str): name of folder you want to compare the files.

    Returns:
        None.
    """
    LOGGER.info(f"Start searching in env '{left_name_env}'")

    env_left_list_of_files = get_files_from_env(
        name_env=left_name_env,
        name_dir=name_dir,
    )

    LOGGER.info(f"Finished searching in env '{left_name_env}'")
    LOGGER.info(f"Start searching in env '{right_name_env}'")

    env_right_list_of_files = get_files_from_env(
        name_env=right_name_env,
        name_dir=name_dir,
    )

    LOGGER.info(f"Finished searching in env '{right_name_env}'")
    LOGGER.info(f"Start comparing envs")

    if len(env_left_list_of_files) == 0 and len(env_right_list_of_files) == 0:
        raise ValueError("Both envs have zero results. "
                         "Check your current path or TOML config file "
                         "with non-existing folders to include")

    env_left_file_name_path_dict = get_file_name_file_path_dict(env_left_list_of_files)
    env_right_file_name_path_dict = get_file_name_file_path_dict(env_right_list_of_files)

    LOGGER.info(f"Compare files in the two environments")

    compare_list_of_files(
        list_env_left=[*env_left_file_name_path_dict],
        list_env_right=[*env_right_file_name_path_dict],
        name_env_left=left_name_env,
        name_env_right=right_name_env,
    )

    LOGGER.info(f"Compare file contents in the two environments")

    compare_content_of_shared_files(
        dict_env_left=env_left_file_name_path_dict,
        dict_env_right=env_right_file_name_path_dict,
    )


def get_files_from_env(name_env: str, name_dir: str) -> list:
    """
    Gets list of files from environment. Important: the assumption is that the folder
    of your environment is higher in the hierarchy than the folder you want to compare
    all files of.

    Args:
        name_env (str): name of environment folder you want to compare.
        name_dir (str): name of folder you want to compare all underlying files.

    Returns:
        List of files.
    """
    root_path = get_root_path()
    LOGGER.debug(
        f"[{name_env}] Search of files will be initiated from path: '{root_path}'"
    )

    config = get_toml_config(name_env=name_env, root_path=root_path)
    folders_to_include = config[constants.PROJECT_NAME][constants.INCLUDE_KEY]
    folders_to_exclude = config[constants.PROJECT_NAME][constants.EXCLUDE_KEY]

    LOGGER.info(
        f"[{name_env}] Folders to compare in directory '{name_dir}': "
        f"'{folders_to_include}'"
    )
    LOGGER.info(
        f"[{name_env}] Folders not to compare in directory '{name_dir}': "
        f"'{folders_to_exclude}'"
    )

    path_of_env = get_path_of_dir(starting_path=root_path, dir_name=name_env)
    LOGGER.debug(f"[{name_env}] Path of env '{name_env}' found: '{path_of_env}'")

    path_of_env_files = get_path_of_dir(starting_path=path_of_env, dir_name=name_dir)
    LOGGER.debug(
        f"[{name_env}] Path of directory '{name_dir}' found: '{path_of_env_files}'"
    )

    list_of_files = get_files_from_dir(
        path=path_of_env_files,
        folders_to_include=folders_to_include,
        folders_to_exclude=folders_to_exclude,
    )
    LOGGER.info(
        f"[{name_env}] List of files in directory '{name_dir}' "
        f"contains '{len(list_of_files)}' files"
    )
    LOGGER.debug(f"[{name_env}] List of files for env '{name_env}': '{list_of_files}'")

    return list_of_files


def get_toml_config(name_env: str, root_path: str) -> dict:
    """
    Gets the TOML config file. If the TOML config file exists, it will read the config.
    If the TOML config file does not exist, it will initialize an empty TOML config
    file.

    Args:
         name_env (str): name of environment folder you want to compare.
            Used for logging.
        root_path (str): root path of user.
    """
    file_name = constants.TOML_CONFIG_FILE_NAME
    toml_file_path = root_path + "/" + file_name

    try:
        with open(toml_file_path, "r") as file:
            config = toml.load(file)

        LOGGER.info(
            f"[{name_env}] Found config file '{file_name}' with path '{toml_file_path}'"
        )

        return config

    except:
        LOGGER.warning(
            f"[{name_env}] Could not find config file '{file_name}' with "
            f"path '{toml_file_path}'"
        )
        LOGGER.warning(
            f"[{name_env}] Config file created '{file_name}' with "
            f"path '{toml_file_path}'"
        )
        LOGGER.warning(
            f"[{name_env}] Default will be invoked: all folders will be compared"
        )

        config = constants.DEFAULT_TOML_CONFIG
        with open(toml_file_path, "w") as file:
            toml.dump(config, file)

        return config


def compare_content_of_shared_files(dict_env_left: dict, dict_env_right: dict) -> None:
    """
    Compares the content of files in the two environments.

    Args:
        dict_env_left (dict): dict of file names and paths from environment left.
        dict_env_right (dict): dict of file names and paths from environment right.
    """
    files_with_different_content = []

    shared_files = dict_env_left.keys() & dict_env_right.keys()
    for file in shared_files:
        path_left_file = dict_env_left[file]
        path_right_file = dict_env_right[file]
        comparison = filecmp.cmp(path_left_file, path_right_file, shallow=True)

        if not comparison:
            files_with_different_content.append(file)

    if not files_with_different_content:
        LOGGER.info("Compare file contents in the two environments: SUCCESS")

    else:
        LOGGER.warning("Compare file contents in the two environments: FAILED")
        LOGGER.warning(f"The following files have different content:")
        for file in files_with_different_content:
            LOGGER.warning(f"----{file}")


def compare_list_of_files(
    list_env_left: list, list_env_right: list, name_env_left: str, name_env_right: str
) -> None:
    """
    Compares the file names in the lists of the two environments.

    Args:
        list_env_left (list): list of files from environment left.
        list_env_right (list): list of files from environment right.
        name_env_left (str): name of left environment folder you want to compare.
            Used for logging.
        name_env_right (str): name of right environment folder you want to compare.
            Used for logging.
    """
    try:
        np.testing.assert_array_equal(
            list_env_left,
            list_env_right
        )
        LOGGER.info("Compare files in the two environments: SUCCESS")

    except:
        LOGGER.warning("Compare files in the two environments: FAILED")

        log_different_files(
            list_env_left=list_env_right,
            list_env_right=list_env_left,
            name_env=name_env_left,
        )

        log_different_files(
            list_env_left=list_env_left,
            list_env_right=list_env_right,
            name_env=name_env_right,
        )


def log_different_files(
    list_env_left: list, list_env_right: list, name_env: str
) -> None:
    """
    Logs differences between the list of files.

    Args:
        list_env_left (list): list of files from environment left.
        list_env_right (list): list of files from environment right.
        name_env (str): name of environment folder you want to compare.
            Used for logging.
    """
    diff_left = set(list_env_left).difference(list_env_right)
    if diff_left != set():
        LOGGER.warning(f"The following files are missing in env '{name_env}':")
        for file in diff_left:
            LOGGER.warning(f"----{file}")
