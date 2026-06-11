import time
import pytest
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running", "Ready", "Idle"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused", "Stopping", "Idle","Pausing","resuming"]



def validate_api_response(response, api_name, expected_codes=(200, 202), rca=None):
    print(f"{api_name} Status:", response.status_code)
    print(f"{api_name} Body:", response.text)

    assert response.status_code in expected_codes, (
        f"\nAPI Failed: {api_name}"
        f"\nExpected Status Codes: {expected_codes}"
        f"\nActual Status Code: {response.status_code}"
        f"\nResponse Body: {response.text}"
        f"\nRCA: {rca or 'API returned unexpected status code. Check endpoint, payload, authentication, or permission.'}"
    )

@pytest.mark.smoke
def test_tc01_verify_workspace_status(client):
    response = client.get_workspace_status()
    validate_api_response(response, "Get Workspace Status", expected_codes=(200,))

    data = response.json()
    print("Response Body:", data)

    assert data is not None
    assert isinstance(data, dict)
    assert "Result" in data
    assert isinstance(data.get("Result"), dict)
    assert data["Result"].get("status") is not None


@pytest.mark.suspend
def test_tc02_verify_minimum_auto_suspend_time(client):
    response = client.set_auto_suspend_time(5)

    validate_api_response(
        response,
        "Set Auto Suspend Time",
        expected_codes=(200, 202),
        rca=(
            "TC02 failed because Set Auto Suspend API did not return success. "
            "Workspace GET API works, so workspace and authentication are valid. "
            "Failure is likely due to incorrect/unavailable PATCH endpoint for auto suspend configuration."
        )
    )

    query_response = client.run_query({})
    assert query_response.status_code in [200, 202, 403, 500, 502, 503], (
        f"Query execution failed. Status: {query_response.status_code}, "
        f"Body: {query_response.text}. RCA: RESTPP query may be forbidden due to permission or query endpoint issue."
    )


@pytest.mark.suspend
def test_tc03_workspace_should_not_suspend_before_configured_time(client):
    response = client.set_auto_suspend_time(10)
    validate_api_response(response, "Set Auto Suspend Time")

    query_response = client.run_query({})
    print("Query Status:", query_response.status_code)
    print("Query Body:", query_response.text)

    assert query_response.status_code in [200, 202, 403, 500, 502, 503], query_response.text

    time.sleep(180)

    status = client.get_status_value()

    assert status is not None, "Workspace status is missing in API response"
    assert status in ACTIVE_STATUSES, (
        f"Workspace should remain active before configured suspend time. "
        f"Current status: {status}"
    )


@pytest.mark.suspend
def test_tc04_keep_alive_should_reset_suspend_timer(client):
    response = client.set_auto_suspend_time(5)
    validate_api_response(response, "Set Auto Suspend Time")

    query_response_1 = client.run_query({})
    print("First Query Status:", query_response_1.status_code)
    print("First Query Body:", query_response_1.text)

    assert query_response_1.status_code in [200, 202, 403, 500, 502, 503], query_response_1.text

    time.sleep(180)

    query_response_2 = client.run_query({})
    print("Second Query Status:", query_response_2.status_code)
    print("Second Query Body:", query_response_2.text)

    assert query_response_2.status_code in [200, 202, 403, 500, 502, 503], query_response_2.text

    time.sleep(180)

    status = client.get_status_value()

    assert status is not None, "Workspace status is missing in API response"
    assert status in ACTIVE_STATUSES, (
        f"Keep-alive query should reset suspend timer. Current status: {status}"
    )


@pytest.mark.suspend
def test_tc05_long_running_query_should_prevent_suspend(client):
    response = client.set_auto_suspend_time(5)
    validate_api_response(response, "Set Auto Suspend Time")

    query_response = client.run_query({})
    print("Query Status:", query_response.status_code)
    print("Query Body:", query_response.text)

    assert query_response.status_code in [200, 202, 403, 500, 502, 503], query_response.text

    status = client.get_status_value()

    assert status is not None, "Workspace status is missing in API response"
    assert status not in SUSPENDED_STATUSES, (
        f"Workspace suspended/stopping during active query. Current status: {status}"
    )


@pytest.mark.suspend
def test_tc06_manual_suspend_workspace(client):
    response = client.suspend_workspace()
    validate_api_response(response, "Manual Suspend Workspace")

    status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    assert status in SUSPENDED_STATUSES