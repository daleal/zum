from argparse import ArgumentParser

import pytest

import zum
from zum.cli import dispatcher, generate_parser, log


class TestGenerateParser:
    def setup_method(self):
        self.empty_actions = []
        self.one_action = ["test"]
        self.multiple_actions = ["test1", "test2", "test3"]

    def test_empty_actions(self, capsys):
        parser = generate_parser(self.empty_actions)
        assert isinstance(parser, ArgumentParser)

        parser.print_help()
        captured = capsys.readouterr().out
        assert "No config file" in captured

    def test_one_action(self, capsys):
        parser = generate_parser(self.one_action)
        assert isinstance(parser, ArgumentParser)

        parser.print_help()
        captured = capsys.readouterr().out
        assert "No config file" not in captured
        assert f"{{{','.join(self.one_action)}}}" in captured

    def test_multiple_actions(self, capsys):
        parser = generate_parser(self.multiple_actions)
        assert isinstance(parser, ArgumentParser)

        parser.print_help()
        captured = capsys.readouterr().out
        assert "No config file" not in captured
        assert f"{{{','.join(self.multiple_actions)}}}" in captured


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


class TestLogger:
    def test_logger(self, capsys):
        log("test")
        captured = capsys.readouterr().out
        assert "test" in captured
