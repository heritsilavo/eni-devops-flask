
import unittest
from app import app


class TestHello(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_hello(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b"Hello World! Deployed automatically with Jenkins and Kubernetes.\n"
        )

    def test_hello_route(self):
        response = self.client.get("/hello/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b"Hello World! Deployed automatically with Jenkins and Kubernetes.\n"
        )

    def test_hello_username(self):
        response = self.client.get("/hello/Tsilavo")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Hello Tsilavo!\n")


if __name__ == "__main__":
    unittest.main()
