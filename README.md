# # Savanna Auto Suspend & Auto Resume API Automation Framework

## Overview

This project is a Python Pytest-based API automation framework created to validate Savanna / TigerGraph workspace auto suspend and auto resume behavior.

The framework validates workspace status, auto suspend behavior, auto resume behavior, RESTPP query execution, negative scenarios, and state transition scenarios.

---

## Tech Stack

| Tool | Usage |
|---|---|
| Python | Automation scripting |
| Pytest | Test framework |
| Requests | API automation |
| python-dotenv | Environment variable handling |
| pytest-html | HTML report generation |

---

## Project Structure

```text
savanna_auto_suspend_tests/
│
├── tests/
│   ├── test_debug_connection.py
│   ├── test_auto_suspend.py
│   ├── test_auto_resume.py
│   ├── test_negative_cases.py
│   └── test_state_transition.py
│
├── utils/
│   ├── savanna_client.py
│   └── wait_utils.py
│
├── reports/
│   ├── test_report.html
│   ├── auto_suspend_report.html
│   └── negative_report.html
│
├── screenshots/
├── logs/
├── Test_Plan.md
├── Traceability_Matrix.md
├── BUG_REPORT_TC15.md
├── RCA_AND_SOLUTIONS.md
├── .env
├── conftest.py
├── pytest.ini
├── requirements.txt
└── README.md


Install dependencies:

pip install -r requirements.txt

## How to Run Tests:

Run debug connection test
pytest tests/test_debug_connection.py -v -s

Run auto suspend tests
pytest tests/test_auto_suspend.py -v -s

Run auto resume tests
pytest tests/test_auto_resume.py -v -s

Run negative tests
pytest tests/test_negative_cases.py -v -s

Run state transition tests
pytest tests/test_state_transition.py -v -s

Run all tests
pytest -v -s

If you are running against TigerGraph Cloud / Savanna RESTPP, set a RESTPP token in your `.env`:

RESTPP_TOKEN=<your-restpp-token>
RESTPP_TOKEN_METHOD=header  # or query

Generate HTML Reports
Full report
pytest -v -s --html=reports/test_final_report.html --self-contained-html


Auto Suspend Scenarios:

TC ID	Scenario
TC01	Verify workspace API is reachable
TC02	Verify minimum auto suspend configuration
TC03	Verify workspace should not suspend before configured time
TC04	Verify keep-alive activity resets suspend timer
TC05	Verify long-running query prevents suspend
TC06	Verify manual suspend workspace

Auto Resume Scenarios:
TC ID	Scenario
TC07	Verify workspace auto resumes from API request
TC08	Verify query execution after resume
TC09	Verify workspace remains active after resume
TC10	Verify resume timeout handling

Negative Scenarios:

TC ID	Scenario
TC11	Invalid API key should return unauthorized
TC12	Invalid workspace ID should return not found
TC13	Invalid auto suspend time below minimum
TC14	Invalid auto suspend time above maximum
TC15	Invalid RESTPP endpoint or query payload

State Transition Scenarios:

TC ID	Scenario
TC16	Verify active to suspended transition
TC17	Verify suspended to active transition
TC18	Verify multiple resume requests
TC19	Verify workspace status consistency

## Debug / Connectivity Scenarios

TC20 Verify Workspace Status API Connectivity

## Execution Summary

Total Test Cases : 20

Passed : 12

Failed : 8

Execution Type : API Automation

Framework : Pytest + Requests

Environment : TigerGraph Savanna Cloud


---

## Test Coverage

### Covered Areas

* Workspace Status Validation
* Auto Suspend Validation
* Auto Resume Validation
* Manual Suspend / Resume
* State Transition Validation
* RESTPP Query Validation
* Negative API Validation

### Out of Scope

* UI Testing
* Performance Testing
* Load Testing
* Security Testing
* Multi Region Validation

---

## Known Issues

* TC08 and TC18 fail due to RESTPP authentication token validation issue (HTTP 403).
* TC09 and TC10 fail due to backend resume API returning HTTP 500.
* TC12, TC13, TC14 and TC15 expose backend validation handling issues.
* Detailed RCA is available in RCA_AND_SOLUTIONS.md.


---

## Execution Evidence

Execution Logs:

- pytest_output.log
- resume_output.log
- pytest_run.txt

Execution Reports:

- reports/test_report.html
- reports/final_report.html
- reports/debug_connection_report.html

Screenshots:

- screenshots/ (execution screenshots captured during test execution)

Bug Reports:

- BUG_REPORT_TC15.md

RCA Documentation:

- RCA_AND_SOLUTIONS.md

Note:

Execution evidence is provided through screenshots, generated HTML reports, execution logs, bug reports, and RCA documentation.