import pytest

from zum.requests.errors import InvalidEndpointDefinitionError
from zum.requests.validations import (
    validate_raw_endpoint,
    validate_raw_endpoint_method,
    validate_raw_endpoint_route,
    validate_body_parameter_definition,
)


class TestRawEndpointValidation:
    # Just tests that a valid raw endpont passes, as the sub-methods are
    # tested against errors and invalid formats
    def setup_method(self):
        self.raw_endpoint = {"method": "get", "route": "/valid"}

    def test_valid_raw_endpoint(self):
        validate_raw_endpoint(self.raw_endpoint)


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


class TestBodyParameterDefinitionValidation:
    def setup_method(self):
        self.invalid_parameter = ["asdf"]
        self.no_name = {"type": "integer"}
        self.invalid_type = {"name": "test", "type": "invalid"}
        self.valid = [
            "valid",
            {"name": "valid"},
            {"name": "valid", "type": "integer"}
        ]

    def test_invalid_parameter(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_body_parameter_definition(self.invalid_parameter)
        assert "should be a string or an object" in str(excinfo.value)

    def test_no_name(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_body_parameter_definition(self.no_name)
        assert "A name is required for every endpoint" in str(excinfo.value)

    def test_invalid_type(self):
        with pytest.raises(InvalidEndpointDefinitionError) as excinfo:
            validate_body_parameter_definition(self.invalid_type)
        assert "Invalid type definition" in str(excinfo.value)

    def test_valid_parameter_definitions(self):
        for parameter in self.valid:
            validate_body_parameter_definition(parameter)
