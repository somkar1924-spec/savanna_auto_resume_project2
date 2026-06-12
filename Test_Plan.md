# Test Plan

## Objective
Validate Savanna workspace Auto Suspend and Auto Resume functionality using API automation.

## Scope
- Workspace Status Validation
- Auto Suspend Validation
- Auto Resume Validation
- Manual Suspend / Resume
- State Transition Validation
- RESTPP Query Validation
- Negative Validation

## Test Environment

Environment: TigerGraph Savanna Cloud

Authentication:
- API Key
- RESTPP Token

Tools:
- Python
- Pytest
- Requests

## Entry Criteria

- Workspace is active
- API credentials are available
- RESTPP token is generated
- Network connectivity is available

## Exit Criteria

- All test cases executed
- Reports generated
- Bugs documented
- RCA documented

## Test Scenarios

TC01 – TC20

## Risks & Assumptions

- RESTPP token expiration
- Workspace state delays
- Backend API availability

## Deliverables

- Automation Framework
- README.md
- Traceability_Matrix.md
- Bug Reports
- RCA Document
- HTML Reports

## Out of Scope

- UI Testing
- Performance Testing
- Load Testing
- Security Testing
- Multi-Region Validation

## Execution Evidence

The following artifacts are generated during execution:

- HTML Test Reports
- Pytest Execution Logs
- Screenshots
- Bug Reports
- RCA Documentation
- Traceability Matrix