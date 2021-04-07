import pytest

from zum.requests.errors import (
    InvalidBodyParameterTypeError,
    MissingEndpointParamsError,
)
from zum.requests.helpers import cast_parameter, cast_value, reduce_arguments


class TestReduceArguments:
    def setup_method(self):
        self.keys = ["first", "second", "third"]
        self.short_args = [1, 2]
        self.perfect_args = [1, 2, 3]
        self.long_args = [1, 2, 3, 4, 5]
        self.output = {
            "perfect": {
                "processed": {"first": 1, "second": 2, "third": 3},
                "remaining": [],
            },
            "long": {
                "processed": {"first": 1, "second": 2, "third": 3},
                "remaining": [4, 5],
            },
        }

    def test_empty_keys(self):
        processed, remaining = reduce_arguments(None, self.perfect_args)
        assert processed == {}
        assert remaining == self.perfect_args

    def test_short_args(self):
        with pytest.raises(MissingEndpointParamsError):
            processed, remaining = reduce_arguments(self.keys, self.short_args)

    def test_perfect_args(self):
        processed, remaining = reduce_arguments(self.keys, self.perfect_args)
        assert processed == self.output["perfect"]["processed"]
        assert remaining == self.output["perfect"]["remaining"]

    def test_long_args(self):
        processed, remaining = reduce_arguments(self.keys, self.long_args)
        assert processed == self.output["long"]["processed"]
        assert remaining == self.output["long"]["remaining"]


class TestCastParameter:
    def setup_method(self):
        self.string = {"input": ["key", "value"], "output": {"key": "value"}}
        self.no_type = {"input": [{"name": "key"}, "value"], "output": {"key": "value"}}
        self.casted = {
            "input": [{"name": "key", "type": "integer"}, "35"],
            "output": {"key": 35},
        }
        self.invalid_casting = [{"name": "key", "type": "integer"}, "invalid"]

    def test_string_definition_casting(self):
        output = cast_parameter(*self.string["input"])
        assert output == self.string["output"]

    def test_no_type_definition_casting(self):
        output = cast_parameter(*self.no_type["input"])
        assert output == self.no_type["output"]

    def test_casted_definition_casting(self):
        output = cast_parameter(*self.casted["input"])
        assert output == self.casted["output"]

    def test_invalid_casting(self):
        with pytest.raises(InvalidBodyParameterTypeError) as excinfo:
            cast_parameter(*self.invalid_casting)
        assert "can't be casted" in str(excinfo.value)


class TestCastValue:
    def setup_method(self):
        self.integer = {"input": ["57", "integer"], "output": 57}
        self.float = {"input": ["6.9", "float"], "output": 6.9}
        self.invalid_boolean = ["invalid", "boolean"]
        self.true = {"input": ["true", "boolean"], "output": True}
        self.false = {"input": ["false", "boolean"], "output": False}
        self.invalid_null = ["invalid", "null"]
        self.null = {"input": ["null", "null"], "output": None}
        self.string = {"input": ["valid", "string"], "output": "valid"}

    def test_integer(self):
        output = cast_value(*self.integer["input"])
        assert output == self.integer["output"]

    def test_float(self):
        output = cast_value(*self.float["input"])
        assert output == self.float["output"]

    def test_number(self):
        integer_output = cast_value(self.integer["input"][0], "number")
        float_output = cast_value(self.float["input"][0], "number")
        assert (
            integer_output == self.integer["output"]
            and float_output == self.float["output"]
        )

    def test_invalid_boolean(self):
        with pytest.raises(InvalidBodyParameterTypeError) as excinfo:
            cast_value(*self.invalid_boolean)
        assert "only 'true' or 'false'" in str(excinfo.value)

    def test_true_boolean(self):
        output = cast_value(*self.true["input"])
        assert output == self.true["output"]

    def test_false_boolean(self):
        output = cast_value(*self.false["input"])
        assert output == self.false["output"]

    def test_invalid_null(self):
        with pytest.raises(InvalidBodyParameterTypeError) as excinfo:
            cast_value(*self.invalid_null)
        assert "only 'null'" in str(excinfo.value)

    def test_null(self):
        output = cast_value(*self.null["input"])
        assert output == self.null["output"]

    def test_string(self):
        output = cast_value(*self.string["input"])
        assert output == self.string["output"]
