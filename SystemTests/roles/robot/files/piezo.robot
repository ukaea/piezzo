###############################################################################
*** Settings ***
Documentation     A test suite with for the Piezo system.
Library           Collections
Library           String
Resource          k8s_methods.robot
Resource          requests_helpers.robot
Resource          s3methods.robot

###############################################################################
*** Test Cases ***
Grafana Returns Ok Response
    ${response}=  Get Request From Route   /
    Confirm Ok Response  ${response}

Prometheus Returns Ok Response
    ${response}=  Get Request From Route   /prometheus/graph
    Confirm Ok Response  ${response}

Piezo Heartbeat Returns Ok Response
    ${response}=  Get Request From Route   /piezo/
    Confirm Ok Response  ${response}
    ${data}=    Get Response Data   ${response}
    ${expected}=    Create Dictionary   running=true
    Dictionaries Should Be Equal    ${data}   ${expected}

Get Logs Of Non Job Returns Not Found Response
    ${response}=  Get Logs For Spark Job    dummy
    Confirm Not Found Response  ${response}

Get Status Of Non Job Returns Not Found Response
    ${response}=  Get Status Of Spark Job    dummy
    Confirm Not Found Response  ${response}

Delete Job Of Non Job Returns Not Found Response
    ${response}=    Delete Spark Job    dummy
    Confirm Not Found Response  ${response}

Submit Spark Pi Job Returns Ok Response
    ${response}=    Submit SparkPi Job    spark-pi
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Should Match Regexp   ${job_name}   spark-pi-[a-z0-9]{5}
    ${message}=   Get Response Data Message   ${response}
    Should Be Equal As Strings    ${message}    Job driver created successfully

Submit Two Jobs With Same Name Returns Ok Responses
    ${response1}=   Submit SparkPi Job    twin-job
    ${response2}=   Submit SparkPi Job    twin-job
    Confirm Ok Response  ${response1}
    Confirm Ok Response  ${response2}

Submit Job With 57 Character Name Runs Successfully
    ${response}=    Submit SparkPi Job    abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefg
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}     5 seconds
    Should Be True      ${finished}

Submit Job With 58 Character Name Fails
    ${response}=    Submit SparkPi Job    abcdefghijklmnopqrstuvwxyabcdefghijklmnopqrstuvwxyabcdefgh
    Confirm Bad Input Response  ${response}
    ${error}=   Get Response Data     ${response}
    Should Be Equal As Strings    ${error}    The following errors were found:\n\"name\" input has a maximum length of 57 characters\n

Submit GroupByTest Spark Job With Arguments Returns Ok Response
    ${response}=    Submit SparkGroupByTest Job With Arguments   spark-group-by-test
    Confirm Ok Response  ${response}
    ${job_name}=    Get Response Job Name   ${response}
    Should Match Regexp   ${job_name}   spark-group-by-test-[a-z0-9]{5}
    ${message}=   Get Response Data Message   ${response}
    Should Be Equal As Strings    ${message}    Job driver created successfully

Can Get Logs Of Submitted Spark Job
    ${job_name}=     Set Variable   spark-pi
    ${response}=    Submit SparkPi Job    ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}     5 seconds
    Should Be True      ${finished}
    ${response}=  Get Logs For Spark Job    ${job_name}
    ${joblog}=    Get Response Data Message   ${response}
    ${pi_lines}=    Get Lines Containing String   ${joblog}   Pi is roughly 3
    ${num_pi_lines}=    Get Line Count    ${pi_lines}
    Should Be Equal As Integers   ${num_pi_lines}   1

Arguments Have Been Read And Appear In Logs
    ${job_name}=  Set Variable  spark-group-by-test
    ${response}=    Submit SparkGroupByTest Job With Arguments   ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    Confirm Ok Response  ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}     5 seconds
    Should Be True      ${finished}
    ${logresponse}=  Get Logs For Spark Job    ${job_name}
    ${joblog}=  Get Response Data Message   ${logresponse}
    ${arg_1_lines}=    Get Lines Containing String   ${joblog}   Adding task set 0.0 with 10 tasks
    ${arg_4_lines}=    Get Lines Containing String   ${joblog}   Adding task set 2.0 with 3 tasks
    ${num_arg_1_lines}=    Get Line Count    ${arg_1_lines}
    ${num_arg_4_lines}=    Get Line Count    ${arg_4_lines}
    Should Be Equal As Integers   ${num_arg_1_lines}   1
    Should Be Equal As Integers   ${num_arg_4_lines}   1

Can Delete Submitted Spark Job
    ${job_name}=    Set Variable        spark-pi
    ${response}=    Submit SparkPi Job   ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${job_name}     5 seconds
    Should Be True    ${finished}
    ${response}=  Delete Spark Job    ${job_name}
    Confirm Ok Response   ${response}

Can Get Status Of Submitted Spark Job
    ${job_name}=     Set Variable       spark-pi
    ${response}=    Submit SparkPi Job    ${job_name}
    ${job_name}=    Get Response Job Name   ${response}
    Sleep       5 seconds
    ${response}=  Get Status Of Spark Job   ${job_name}
    Confirm Ok Response     ${response}

Job Can Use Data And Code On S3 And Write Back Results
    ${job_name}=    Set Variable      wordcount
    Directory Should Not Exist In S3 Bucket   kubernetes    outputs/${job_name}
    ${response}=    Submit Wordcount On Minio Job   ${job_name}
    Confirm Ok Response  ${response}
    ${new_job_name}=    Get Response Job Name   ${response}
    ${finished}=    Wait For Spark Job To Finish        ${new_job_name}     15 seconds
    Should Be True    ${finished}
    Directory Should Exist In S3 Bucket   kubernetes    outputs/${job_name}
    Directory Should Not Be Empty In S3 bucket  kubernetes    outputs/${job_name}
    File Should Exist In S3 Bucket    kubernetes      outputs/${job_name}/_SUCCESS
