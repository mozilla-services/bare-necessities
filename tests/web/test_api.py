import pytest
from flask import g, request


def test_hello(client):
    response = client.get("/")
    assert response.status == "200 OK"
    assert response.data == b"Hello World!"


def test_hello_name(client):
    import random
    import string

    letters = string.ascii_lowercase
    random_name = "".join(random.choice(letters) for i in range(10))

    response = client.get(f"/{random_name}")
    assert response.status == "200 OK"
    assert response.data.decode("utf-8") == f"Hello {random_name}"
    print(random_name)
