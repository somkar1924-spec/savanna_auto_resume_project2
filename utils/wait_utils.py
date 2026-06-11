import time

ACTIVE_STATUSES = ["Active", "Running", "Ready", "Idle"] 
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused", "Pausing", "resuming"]
STABLE_SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused", "Idle"]
TRANSIENT_STATUSES = ["Pausing", "Resuming", "Stopping", "Starting", "PauseRoll"]


def wait_until_status(client, expected_statuses, timeout=300, interval=20):
    end_time = time.time() + timeout
    last_status = None

    while time.time() < end_time:
        status = client.get_status_value()
        print(f"Current workspace status: {status}")

        last_status = status

        if status in expected_statuses:
            return status

        time.sleep(interval)

    assert False, (
        f"Workspace did not reach expected status {expected_statuses}. "
        f"Last observed status: {last_status}"
    )


def ensure_workspace_active(client, timeout=900, interval=20):
    end_time = time.time() + timeout
    last_status = None

    while time.time() < end_time:
        status = client.get_status_value()
        print(f"Ensuring active workspace, current status: {status}")

        if status in ACTIVE_STATUSES:
            return status

        if status in STABLE_SUSPENDED_STATUSES:
            response = client.resume_workspace()
            print(f"Resume workspace request status: {response.status_code}")
            if response.status_code not in [200, 202, 204]:
                raise AssertionError(
                    f"Failed to resume workspace before tests. "
                    f"Status: {response.status_code}, Body: {response.text}"
                )
            return wait_until_status(client, expected_statuses=ACTIVE_STATUSES, timeout=timeout, interval=interval)

        last_status = status
        time.sleep(interval)

    assert False, (
        f"Workspace did not become active before timeout. "
        f"Last observed status: {last_status}"
    )