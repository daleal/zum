import os

import pytest

from zum.configs.core import (
    search_for_config_file,
    retrieve_config_file,
    validate_endpoints,
    validate_metadata,
)
from zum.configs.errors import InvalidConfigFileError, MissingConfigFileError


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

    def test_path_does_not_exist(self, tmpdir):
        with pytest.raises(MissingConfigFileError):
            config_file = tmpdir.join("zum.toml")
            search_for_config_file(config_file.strpath)


class TestRetrieveConfigFile:
    def setup_method(self):
        self.content = (
            "[metadata]\n"
            'server = "http://localhost:8000"\n'
            "[endpoints.example]\n"
            'route = "/example"\n'
            'method = "get"\n'
        )
        self.parsed = {
            "metadata": {"server": "http://localhost:8000"},
            "endpoints": {"example": {"route": "/example", "method": "get"}},
        }

    def test_expected_retrieval(self, tmpdir):
        config_file = tmpdir.join("zum.toml")
        with open(config_file.strpath, "w") as raw_config_file:
            raw_config_file.write(self.content)
        assert retrieve_config_file(config_file.strpath) == self.parsed


class TestValidateMetadata:
    def setup_method(self):
        self.missing = {"some-key": "some-value"}
        self.invalid_type = {"some-key": "some-value", "metadata": "nice"}
        self.missing_server = {
            "some-key": "some-value",
            "metadata": {"some-thing": "some-value"},
        }

    def test_missing_metadata_key(self):
        with pytest.raises(InvalidConfigFileError) as excinfo:
            validate_metadata(self.missing)
        assert "Missing 'metadata' section" in str(excinfo.value)

    def test_invalid_endpoints_key_type(self):
        with pytest.raises(InvalidConfigFileError) as excinfo:
            validate_metadata(self.invalid_type)
        assert ("The 'metadata' section shold be a dictionary or mapping") in str(
            excinfo.value
        )

    def test_empty_endpoints_key(self):
        with pytest.raises(InvalidConfigFileError) as excinfo:
            validate_metadata(self.missing_server)
        assert "Missing 'server' value from the 'metadata' section" in str(
            excinfo.value
        )


class TestValidateEndpoints:
    def setup_method(self):
        self.missing = {"some-key": "some-value"}
        self.invalid_type = {"some-key": "some-value", "endpoints": "nice"}
        self.empty = {"some-key": "some-value", "endpoints": {}}

    def test_missing_endpoints_key(self):
        with pytest.raises(InvalidConfigFileError) as excinfo:
            validate_endpoints(self.missing)
        assert "Missing 'endpoints' section" in str(excinfo.value)

    def test_invalid_endpoints_key_type(self):
        with pytest.raises(InvalidConfigFileError) as excinfo:
            validate_endpoints(self.invalid_type)
        assert ("The 'endpoints' section shold be a dictionary or mapping") in str(
            excinfo.value
        )

    def test_empty_endpoints_key(self):
        with pytest.raises(InvalidConfigFileError) as excinfo:
            validate_endpoints(self.empty)
        assert "At least one endpoint is required" in str(excinfo.value)
