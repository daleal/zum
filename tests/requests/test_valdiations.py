import pytest

from zum.requests.errors import InvalidEndpointDefinitionError
from zum.requests.validations import (
    validate_raw_endpoint_method,
    validate_raw_endpoint_route,
)


class TestRawEndpointMethodValidation:
    def setup_method(self):
        self.missing = {"some": "thing"}
        self.invalid_type = {"method": 4}
        self.invalid_content = {"method": "not valid"}
        self.spaced_valid = {"method": " get   "}
        self.uppercased_valid = {"method": "GET"}

    def test_missing_method(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_raw_endpoint_method(self.missing)
        assert "Missing 'method' attribute" in str(excinfo.value)

    def test_invalid_type_method(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_raw_endpoint_method(self.invalid_type)
        assert "The 'method' attribute for the endpoint must be a string" in str(
            excinfo.value
        )

    def test_invalid_content_method(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_raw_endpoint_method(self.invalid_content)
        assert (
            "Invalid 'method' value for the endpoint (not a valid HTTP method)"
            in str(excinfo.value)
        )

    def test_spaced_valid_method(self):
        validate_raw_endpoint_method(self.spaced_valid)

    def test_uppercased_valid_method(self):
        validate_raw_endpoint_method(self.uppercased_valid)


class TestRawEndpointRouteValidation:
    def setup_method(self):
        self.missing = {"some": "thing"}
        self.invalid_type = {"route": 4}
        self.valid = {"route": "/valid"}

    def test_missing_route(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_raw_endpoint_route(self.missing)
        assert "Missing 'route' attribute" in str(excinfo.value)

    def test_invalid_type_route(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_raw_endpoint_route(self.invalid_type)
        assert "The 'route' attribute of the endpoint must be a string" in str(
            excinfo.value
        )

    def test_valid_route(self):
        validate_raw_endpoint_route(self.valid)
