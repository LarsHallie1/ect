import logging

import numpy as np
import toml

from ect import constants
from ect.utils import get_files_from_dir, get_path_of_dir, get_root_path

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

    try:
        np.testing.assert_array_equal(env_left_list_of_files, env_right_list_of_files)
        LOGGER.info("SUCCESS")

    except:
        LOGGER.warning("FAILED")

        log_different_files(
            list_env_left=env_right_list_of_files,
            list_env_right=env_left_list_of_files,
            name_env=left_name_env,
        )

        log_different_files(
            list_env_left=env_left_list_of_files,
            list_env_right=env_right_list_of_files,
            name_env=right_name_env,
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


# https://stackoverflow.com/questions/254350/in-python-is-there-a-concise-way-of-comparing-whether-the-contents-of-two-text
