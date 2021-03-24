import json

import pytest

from zum.configs.errors import InvalidConfigFileError, MissingConfigFileError
from zum.engine import Engine

# This tests will only test behaviour, as the module being tested
# is a behavoiural-driven module, and hides some of its details to
# the exterior of the interface.


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
            engine._validate_configurations()

    def test_invalid_config(self, tmpdir):
        with pytest.raises(InvalidConfigFileError):
            config_file = tmpdir.join("zum.toml")
            with open(config_file.strpath, "w") as raw_config_file:
                raw_config_file.write(self.invalid_config)
            engine = Engine(config_file.strpath)
            engine._validate_configurations()

    def test_valid_config(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        with open(config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.valid_config)
        engine = Engine(config_file.strpath)
        engine._validate_configurations()


class TestEngineActionsList:
    def setup_method(self):
        self.multiple_actions = (
            "[metadata]\n"
            "server = 'http://localhost:8000'\n"
            "[endpoints.test]\n"
            "route = '/test'\n"
            "method = 'get'\n"
            "[endpoints.second-test]\n"
            "route = '/second-test'\n"
            "method = 'get'\n"
        )

    def test_no_config(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        engine = Engine(config_file.strpath)
        assert engine.actions == []

    def test_multiple_actions(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        with open(config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.multiple_actions)
        engine = Engine(config_file.strpath)
        assert "test" in engine.actions and "second-test" in engine.actions


class TestExecutionBehaviour:
    @pytest.fixture(autouse=True)
    def patch_request(self, patch_request):
        pass

    def setup_method(self):
        self.valid_config = (
            "[metadata]\n"
            "server = 'http://localhost:8000'\n"
            "[endpoints.test]\n"
            "route = '/test'\n"
            "method = 'get'\n"
        )
        self.invalid_config = (
            "[metadata]\n"
            "server = ''\n"
            "[endpoints.test]\n"
            "route = '/test'\n"
            "method = 'post'\n"
        )
        self.valid_output = {
            "url": "http://localhost:8000/test",
            "method": "get",
            "json": {},
            "headers": {},
        }
        self.invalid_output = "No URL specified for method 'post'"

    def test_valid_config(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        with open(config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.valid_config)
        engine = Engine(config_file.strpath)
        engine.execute("test", [])
        assert self.valid_output == json.loads(engine.output)

    def test_invalid_config(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        with open(config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.invalid_config)
        engine = Engine(config_file.strpath)
        engine.execute("test", [])
        assert self.invalid_output in engine.output
