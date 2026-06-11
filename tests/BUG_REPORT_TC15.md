Bug Title: T15 - API returns 500 Internal Server Error for missing required query payload

Module:
 Negative Validation

Severity:
Medium

Priority:
High

Environment:
Savanna Auto Suspend Test Environment

Steps to Reproduce:
1. Send query execution API request with missing/empty payload.
2. Observe the API response status code.

Test Data:
Payload: empty / missing required query payload

Expected Result:
API should return a proper client-side validation error such as 400 Bad Request or 422 Unprocessable Entity with a meaningful error message.

Actual Result:
API returns 500 Internal Server Error.

Impact:
Invalid client input is not handled properly. Server returns internal error instead of validation response, which can confuse API consumers and hide input validation issues.

RCA:
The request reaches the server successfully, but the backend does not handle missing/empty query payload validation properly. Instead of returning a structured 4xx validation error, it throws a 500 server error.

Recommendation / Solution:
Add proper request payload validation on the backend and return 400/422 with a clear error message when required query payload is missing.

Status:
Open