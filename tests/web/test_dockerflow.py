import pytest
import logging
from flask import g, request


def test_lbheartbeat(client):
    response = client.get("/__lbheartbeat__")
    assert response.status == "200 OK"


def test_heartbeat(client):
    response = client.get("/__lbheartbeat__")
    assert response.status == "200 OK"


def test_version_json(client):
    response = client.get("/__version__")
    assert response.status == "200 OK"


def test_request_summary(caplog, client):
    client.get(
        "/", headers={"User-Agent": "dockerflow/tests", "Accept-Language": "tlh"}
    )
    assert getattr(g, "_request_id") is not None
    assert isinstance(getattr(g, "_start_timestamp"), float)

    for record in caplog.records:
        if hasattr(record, "method"):
            assert record.levelno == logging.INFO
            assert record.errno == 0
            assert record.agent == "dockerflow/tests"
            assert record.lang == "tlh"
            assert record.method == "GET"
            assert record.path == "/"
            assert record.rid == g._request_id
            assert isinstance(record.t, int)
            assert getattr(request, "uid", None) is None
