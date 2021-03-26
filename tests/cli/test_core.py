from argparse import ArgumentParser

import pytest

import zum
from zum.cli.core import dispatcher, get_config_file_name
from zum.constants import DEFAULT_CONFIG_FILE_NAME


class TestDispatcher:
    def setup_method(self):
        self.invalid_config = (
            "[metadata]\n"
            "server = ''\n"
            "[endpoints.test]\n"
            "route = '/test'\n"
            "method = 'get'\n"
        )

    def test_help_flag(self, capsys):
        with pytest.raises(SystemExit):
            dispatcher(["--help"])
        captured = capsys.readouterr().out
        assert "Command line interface tool for zum." in captured

    def test_version_flag(self, capsys):
        with pytest.raises(SystemExit):
            dispatcher(["--version"])
        captured = capsys.readouterr().out
        assert f"zum version {zum.__version__}" in captured


class TestGetConfigFileName:
    def setup_method(self):
        self.file_name = "custom.toml"

    def test_empty_call(self):
        file_name = get_config_file_name()
        assert file_name == DEFAULT_CONFIG_FILE_NAME

    def test_filled_call(self):
        file_name = get_config_file_name(["--file", self.file_name])
        assert file_name == self.file_name
