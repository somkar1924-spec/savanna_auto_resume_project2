import pytest
from concurrent.futures import ThreadPoolExecutor
import utils.savanna_client
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running",  "Ready"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused", "Stopping", "Idle","Pausing","resuming"]


def validate_api_response(response, api_name, expected_codes=(200, 202)):
    print(f"{api_name} Status:", response.status_code)
    print(f"{api_name} Body:", response.text)

    assert response.status_code in expected_codes, (
        f"{api_name} failed. Expected {expected_codes}, "
        f"Actual: {response.status_code}, Body: {response.text}"
    )


@pytest.mark.resume
def test_tc07_auto_resume_from_api_request(client: utils.savanna_client.SavannaClient):
    auto_resume_response = client.enable_auto_resume(True)
    validate_api_response(auto_resume_response, "Enable Auto Resume")

    suspend_response = client.suspend_workspace()
    validate_api_response(suspend_response, "Suspend Workspace")

    suspended_status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=300,
        interval=15
    )
    assert suspended_status in SUSPENDED_STATUSES

    response = client.run_query({})
    print("Query Status:", response.status_code)
    print("Query Body:", response.text)

    assert response.status_code in [200, 202, 502, 503], response.text

    active_status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=600,
        interval=15
    )
    assert active_status in ACTIVE_STATUSES


@pytest.mark.resume
def test_tc08_auto_resume_disabled_should_not_resume(client: utils.savanna_client.SavannaClient):
    auto_resume_response = client.enable_auto_resume(False)
    validate_api_response(auto_resume_response, "Disable Auto Resume")

    suspend_response = client.suspend_workspace()
    validate_api_response(suspend_response, "Suspend Workspace")

    suspended_status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=900,
        interval=15
    )
    assert suspended_status in SUSPENDED_STATUSES

    response = client.run_query({})
    print("Query Status:", response.status_code)
    print("Query Body:", response.text)

    assert response.status_code in [400, 409, 423, 500, 502, 503], response.text

    status = client.get_status_value()

    assert status is not None, "Workspace status is missing in API response"
    assert status in SUSPENDED_STATUSES, (
        f"Workspace resumed even though auto resume is disabled. Current status: {status}"
    )


@pytest.mark.resume
def test_tc09_manual_resume_workspace(client: utils.savanna_client.SavannaClient):
    suspend_response = client.suspend_workspace()
    validate_api_response(suspend_response, "Suspend Workspace")

    suspended_status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=300,
        interval=15
    )
    assert suspended_status in SUSPENDED_STATUSES

    resume_response = client.resume_workspace()
    validate_api_response(resume_response, "Resume Workspace")

    active_status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=600,
        interval=15
    )
    assert active_status in ACTIVE_STATUSES


@pytest.mark.resume
def test_tc10_concurrent_resume_requests(client: utils.savanna_client.SavannaClient):
    auto_resume_response = client.enable_auto_resume(True)
    validate_api_response(auto_resume_response, "Enable Auto Resume")

    suspend_response = client.suspend_workspace()
    validate_api_response(suspend_response, "Suspend Workspace")

    suspended_status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=300,
        interval=15
    )
    assert suspended_status in SUSPENDED_STATUSES

    def trigger_query():
        query_response = client.run_query({})
        print("Concurrent Query Status:", query_response.status_code)
        print("Concurrent Query Body:", query_response.text)
        return query_response.status_code

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda _: trigger_query(), range(5)))

    print("Concurrent response codes:", results)

    assert all(code in [200, 202, 409, 502, 503] for code in results), (
        f"Unexpected concurrent response codes: {results}"
    )

    active_status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=600,
        interval=15
    )
    assert active_status in ACTIVE_STATUSES