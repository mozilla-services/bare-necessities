import pytest
from flask import g, request


def test_hello(client):
    response = client.get("/")
    assert response.status == "200 OK"
    assert response.data == b"Hello World!"


def test_hello_name(client):
    random_name = make_random_name()
    response = client.get(f"/{random_name}")
    assert response.status == "200 OK"
    assert response.data.decode("utf-8") == f"Hello {random_name}"
    print(random_name)


def test_create_new_user(client):
    random_name = make_random_name()
    response = client.post(
        f"/user", json=dict(name=random_name, email=f"{random_name}@example.net")
    )

    assert response.status_code == 202
    data = response.json
    assert data["name"] == random_name
    assert data["email"] == f"{random_name}@example.net"

    # get the newly created user through the /user/ endpoint
    # to verify that it was properly inserted in database.
    response = client.get(f"/user/{random_name}")
    assert response.status == "200 OK"
    data = response.json
    assert data["name"] == random_name
    assert data["email"] == f"{random_name}@example.net"


def make_random_name():
    import random
    import string

    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(10))
