from argparse import ArgumentParser

from zum.cli.generators import generate_config_file_parser, generate_main_parser


class TestGenerateMainParser:
    def setup_method(self):
        self.config_file_name = "zum.toml"
        self.empty_actions = []
        self.one_action = ["test"]
        self.multiple_actions = ["test1", "test2", "test3"]

    def test_empty_actions(self, capsys):
        parser = generate_main_parser(self.config_file_name, self.empty_actions)
        assert isinstance(parser, ArgumentParser)

        parser.print_help()
        captured = capsys.readouterr().out
        assert "No config file" in captured
        assert self.config_file_name in captured

    def test_one_action(self, capsys):
        parser = generate_main_parser(self.config_file_name, self.one_action)
        assert isinstance(parser, ArgumentParser)

        parser.print_help()
        captured = capsys.readouterr().out
        assert "No config file" not in captured
        assert f"{{{','.join(self.one_action)}}}" in captured

    def test_multiple_actions(self, capsys):
        parser = generate_main_parser(self.config_file_name, self.multiple_actions)
        assert isinstance(parser, ArgumentParser)

        parser.print_help()
        captured = capsys.readouterr().out
        assert "No config file" not in captured
        assert f"{{{','.join(self.multiple_actions)}}}" in captured


class TestGenerateConfigFileParser:
    def setup_method(self):
        self.filename = "filename"

    def test_parser_creation(self):
        parser = generate_config_file_parser()
        assert not parser.add_help

        known, _ = parser.parse_known_args(["--file", self.filename])
        assert known.file == self.filename
