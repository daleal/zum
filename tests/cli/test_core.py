from argparse import ArgumentParser

import pytest

import zum
from zum.cli.core import dispatcher, get_config_file_name
from zum.constants import DEFAULT_CONFIG_FILE_NAME


class TestDispatcher:
    def setup_method(self):
        self.invalid_config_file_name = "invalid.toml"
        self.valid_config_file_name = "valid.toml"
        self.endpoint_name = "exmple"
        self.configs = (
            "[metadata]\n"
            'server = "http://localhost:8000"\n'
            f"[endpoints.{self.endpoint_name}]\n"
            'route = "/example"\n'
            'method = "get"\n'
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

    def test_invalid_config_file(self, tmpdir, capsys):
        invalid_config_file = tmpdir.join(self.invalid_config_file_name)
        valid_config_file = tmpdir.join(self.valid_config_file_name)
        with open(valid_config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.configs)

        with pytest.raises(SystemExit):
            dispatcher(["--file", invalid_config_file.strpath, "--help"])

        captured = capsys.readouterr().out
        assert "No config file" in captured
        assert self.invalid_config_file_name in captured

    def test_valid_config_file(self, tmpdir, capsys):
        valid_config_file = tmpdir.join(self.valid_config_file_name)
        with open(valid_config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.configs)

        with pytest.raises(SystemExit):
            dispatcher(["--file", valid_config_file.strpath, "--help"])

        captured = capsys.readouterr().out
        assert "No config file" not in captured
        assert f"{{{self.endpoint_name}}}" in captured


class TestGetConfigFileName:
    def setup_method(self):
        self.file_name = "custom.toml"

    def test_empty_call(self):
        file_name = get_config_file_name()
        assert file_name == DEFAULT_CONFIG_FILE_NAME

    def test_filled_call(self):
        file_name = get_config_file_name(["--file", self.file_name])
        assert file_name == self.file_name
