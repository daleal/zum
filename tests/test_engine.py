import pytest

from zum.configs.errors import InvalidConfigFileError, MissingConfigFileError
from zum.engine import Engine


class TestEngineValidation:
    def setup_method(self):
        self.valid_config = (
            "[metadata]\n"
            "server = 'http://localhost:8000'\n"
            "[endpoints.test]\n"
            "route = '/test'\n"
            "method = 'get'\n"
        )
        self.invalid_config = "[invalid]\ninvalid = 'invalid'"

    def test_no_config(self, tmpdir):
        with pytest.raises(MissingConfigFileError):
            config_file = tmpdir.join("zum.toml")
            engine = Engine(config_file.strpath)
            engine._Engine__validate_configurations()

    def test_invalid_config(self, tmpdir):
        with pytest.raises(InvalidConfigFileError):
            config_file = tmpdir.join("zum.toml")
            with open(config_file.strpath, "w") as raw_config_file:
                raw_config_file.write(self.invalid_config)
            engine = Engine(config_file.strpath)
            engine._Engine__validate_configurations()

    def test_valid_config(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        with open(config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.valid_config)
        engine = Engine(config_file.strpath)
        engine._Engine__validate_configurations()
