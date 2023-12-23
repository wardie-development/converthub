from app import healthcheck


def test_healthcheck():
    result = healthcheck()

    assert result == {"status": "success", "data": "ok"}
