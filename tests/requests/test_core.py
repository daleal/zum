import pytest

from zum.requests.core import reduce_arguments, generate_request
from zum.requests.errors import MissingEndpointParamsError
from zum.requests.models import Request


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


class TestGenerateRequest:
    def setup_method(self):
        self.raw_endpoint = {
            "route": "/example/{id}?query={query}",
            "method": "post",
            "params": ["id", "query"],
            "body": ["name", "city"],
        }
        self.params = {"id": 69, "query": "nais"}
        self.body = {"name": "Dani", "city": "Barcelona"}
        self.arguments = [
            self.params["id"],
            self.params["query"],
            self.body["name"],
            self.body["city"],
        ]
        self.expected_route = (
            f"/example/{self.params['id']}?query={self.params['query']}"
        )

    def test_request_generation(self):
        request = generate_request(self.raw_endpoint, self.arguments)
        assert isinstance(request, Request)
        assert request.params == self.params
        assert request.body == self.body
        assert request.route == self.expected_route
