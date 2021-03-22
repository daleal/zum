import pytest

from zum.requests.core import generate_request
from zum.requests.models import Request


class TestGenerateRequest:
    def setup_method(self):
        self.raw_endpoint = {
            "route": "/example/{id}?query={query}",
            "method": "post",
            "params": ["id", "query"],
            "headers": ["Authorization"],
            "body": ["name", "city"],
        }
        self.params = {"id": 35, "query": "mystring"}
        self.headers = {"Authorization": "Bearer F"}
        self.body = {"name": "Dani", "city": "Barcelona"}
        self.arguments = [
            self.params["id"],
            self.params["query"],
            self.headers["Authorization"],
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
        assert request.headers == self.headers
        assert request.body == self.body
        assert request.route == self.expected_route
