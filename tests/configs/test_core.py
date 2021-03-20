import os

import pytest

from zum.configs.core import search_for_config_file
from zum.configs.errors import MissingConfigFileError


class TestSearchForConfigFile:
    def test_path_is_file(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        open(config_file.strpath, "a").close()
        search_for_config_file(config_file.strpath)

    def test_path_is_folder(self, tmpdir):
        with pytest.raises(MissingConfigFileError):
            config_file = tmpdir.join("zum.toml")
            os.mkdir(config_file.strpath)
            search_for_config_file(config_file.strpath)
