import pytest


@pytest.mark.negative
def test_tc11_invalid_api_key_should_return_unauthorized(client):
    response = client.invalid_api_key_request()

    assert response.status_code in [401, 403]


@pytest.mark.negative
def test_tc12_invalid_workspace_id_should_return_not_found(client):
    response = client.invalid_workspace_request()

    assert response.status_code in [400, 404]


@pytest.mark.negative
def test_tc13_invalid_auto_suspend_time_below_minimum(client):
    response = client.set_auto_suspend_time(2)

    assert response.status_code in [400,404, 422]


@pytest.mark.negative
def test_tc14_invalid_auto_suspend_time_above_maximum(client):
    response = client.set_auto_suspend_time(999999)

    assert response.status_code in [400,404, 422]


@pytest.mark.negative
def test_tc15_missing_required_query_payload(client):
    response = client.run_query("")

    assert response.status_code in [400, 404, 422], (
        f"TC15 Failed: Missing required query payload should return validation error. "
        f"Expected 400/404/422, Actual: {response.status_code}, Body: {response.text}. "
        f"RCA: API is returning 500 Internal Server Error for invalid input. "
        f"This should be handled as client-side validation error, not server error."
    )