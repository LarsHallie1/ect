from unittest import mock

import pytest

from ect import utils


@pytest.fixture
def fake_path():
    return "Users/folder1/folder2/folder3/file1"


def test_get_last_string(fake_path):
    """Tests get part of a string"""

    last_string = utils.get_last_string(fake_path)
    assert last_string == "file1"


@mock.patch("os.path.abspath")
def test_get_root_path(mock_os_path, fake_path):
    """Tests get root path"""

    mock_os_path.return_value = fake_path
    root_directory = utils.get_root_path()
    assert root_directory == fake_path
