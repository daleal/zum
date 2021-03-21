from argparse import ArgumentParser

from zum.cli import generate_parser


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
