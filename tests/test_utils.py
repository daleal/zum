from zum.utils import log


class TestLogger:
    def setup_method(self):
        self.string = "testing string"

    def test_logger(self, capsys):
        log(self.string)
        captured = capsys.readouterr().out
        assert self.string in captured
