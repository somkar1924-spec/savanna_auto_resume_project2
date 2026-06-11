# Traceability Matrix

| Test Case ID | Test Case Description | Automated Test Script |
|-------------|----------------------|----------------------|
| TC01 | Verify Workspace Status API Reachability | test_debug_workspace_status |
| TC02 | Verify Minimum Auto Suspend Configuration | test_tc02_verify_minimum_auto_suspend_time |
| TC03 | Verify Workspace Does Not Suspend Before Configured Time | test_tc03_workspace_should_not_suspend_before_configured_time |
| TC04 | Verify Keep Alive Resets Suspend Timer | test_tc04_keep_alive_should_reset_suspend_timer |
| TC05 | Verify Long Running Query Prevents Suspend | test_tc05_long_running_query_should_prevent_suspend |
| TC06 | Verify Manual Suspend Workspace | test_tc06_manual_suspend_workspace |
| TC07 | Verify Auto Resume From API Request | test_tc07_auto_resume_from_api_request |
| TC08 | Verify Auto Resume Disabled Behavior | test_tc08_auto_resume_disabled_should_not_resume |
| TC09 | Verify Manual Resume Workspace | test_tc09_manual_resume_workspace |
| TC10 | Verify Concurrent Resume Requests | test_tc10_concurrent_resume_requests |
| TC11 | Invalid API Key Validation | test_tc11_invalid_api_key_should_return_unauthorized |
| TC12 | Invalid Workspace ID Validation | test_tc12_invalid_workspace_id_should_return_not_found |
| TC13 | Invalid Auto Suspend Time Below Minimum | test_tc13_invalid_auto_suspend_time_below_minimum |
| TC14 | Invalid Auto Suspend Time Above Maximum | test_tc14_invalid_auto_suspend_time_above_maximum |
| TC15 | Missing Required Query Payload | test_tc15_missing_required_query_payload |
| TC16 | Active To Suspended Transition | test_tc16_active_to_suspended_transition |
| TC17 | Suspended To Active Transition | test_tc17_suspended_to_active_transition |
| TC18 | Resume Request During Suspended State | test_tc18_resume_request_during_suspended_state |
| TC19 | Workspace Should Remain Suspended Without Activity | test_tc19_workspace_should_remain_suspended_without_activity |
| TC20 | Verify Workspace Status API Connectivity | test_debug_workspace_status |