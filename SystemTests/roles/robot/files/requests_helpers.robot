###############################################################################
*** Settings ***
Documentation     Helper methods for sending HTTP requests.

###############################################################################
*** Keywords ***
Confirm Conflict Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   409

Confirm Not Found Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   404

Confirm Bad Input Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   400

Confirm Ok Response
  [Arguments]   ${response}
  Should Be Equal As Strings    ${response.status_code}   200

Get Response Data
  [Arguments]   ${response}
  [return]    ${response.json()["data"]}

Get Response Data Message
  [Arguments]   ${response}
  [return]    ${response.json()["data"]["message"]}

Json Header
  ${header}=  Create Dictionary   Content-Type=application/json
  [return]    ${header}
