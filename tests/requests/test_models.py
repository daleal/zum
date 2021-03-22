from zum.requests.models import Request


class TestRequestModel:
    def setup_method(self):
        self.simple = {
            "route": "/example",
            "method": "get",
            "params": {},
            "headers": {},
            "body": {},
        }
        self.complex = {
            "route": "/example/{id}?query={query}",
            "method": "get",
            "params": {"query": "mystring", "id": 35},
            "headers": {},
            "body": {},
        }
        self.simple_route = "/example"
        self.complex_route = (
            f"/example/{self.complex['params']['id']}"
            f"?query={self.complex['params']['query']}"
        )

    def test_simple_request_route_interpolation(self):
        request = Request(**self.simple)
        assert request.route == self.simple_route

    def test_complex_request_route_interpolation(self):
        request = Request(**self.complex)
        assert request.route == self.complex_route
