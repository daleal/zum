import pytest

from zum.requests.core import reduce_arguments
from zum.requests.errors import MissingEndpointParamsError


class TestReduceArguments:
    def setup_method(self):
        self.keys = ["first", "second", "third"]
        self.short_args = [1, 2]
        self.perfect_args = [1, 2, 3]
        self.long_args = [1, 2, 3, 4, 5]
        self.output = {
            "perfect": {
                "processed": {
                    "first": 1,
                    "second": 2,
                    "third": 3
                },
                "remaining": []
            },
            "long": {
                "processed": {
                    "first": 1,
                    "second": 2,
                    "third": 3
                },
                "remaining": [4, 5]
            }
        }

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
