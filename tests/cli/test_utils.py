from argparse import ArgumentParser

from zum.cli.utils import attach_file_flag


class TestAttachFileFlag:
    def setup_method(self):
        self.filename = "filename"

    def test_adding_flag(self):
        parser = ArgumentParser()

        known, _ = parser.parse_known_args(["--file", self.filename])
        assert not hasattr(known, "file")

        attach_file_flag(parser)
        known, _ = parser.parse_known_args(["--file", self.filename])
        assert known.file == self.filename
