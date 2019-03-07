###############################################################################
*** Settings ***
Documentation     Test resources for interacting with the Kubernetes cluster.
Library           RequestsLibrary
Resource          requests_helpers.robot

###############################################################################
*** Variables ***
${K8S_ENDPOINT}     http://host-172-16-113-146.nubes.stfc.ac.uk:31924

###############################################################################
*** Keywords ***
Delete Request With Json Body
    [Arguments]   ${route}    ${body}
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Delete Request   k8s   ${route}    headers=${headers}    json=${body}
    [return]  ${response}

Delete Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}   namespace=default
    ${response}=  Delete Request With Json Body   /piezo/deletejob    ${body}
    [return]    ${response}

Get Driver Name
    [Arguments]   ${job_name}
    ${driver_name}=   Catenate    SEPARATOR=    ${job_name}   -driver
    [return]    ${driver_name}

Get Logs For Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}   namespace=default
    ${response}=  Get Request With Json Body   /piezo/getlogs    ${body}
    [return]    ${response}

Get Request From Route
    [Arguments]   ${route}
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Get Request   k8s   ${route}
    [return]  ${response}

Get Request With Json Body
    [Arguments]   ${route}    ${body}
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Get Request   k8s   ${route}    headers=${headers}    json=${body}
    [return]  ${response}

Get Status Of Spark Job
    [Arguments]   ${job_name}
    ${body}=    Create Dictionary   job_name=${job_name}   namespace=default
    ${response}=  Get Request With Json Body   /piezo/jobstatus    ${body}
    [return]    ${response}

Post Request With Json Body
    [Arguments]   ${route}    ${body}
    ${headers}=   Json Header
    Create Session    k8s   ${K8S_ENDPOINT}
    ${response}=  Post Request   k8s   ${route}    headers=${headers}    json=${body}
    [return]  ${response}

Submit SparkPi Job
    [Arguments]   ${job_name}
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Scala   main_class=org.apache.spark.examples.SparkPi    path_to_main_app_file=local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar    label=systemTest
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Submit SparkGroupByTest Job With Arguments
    [Arguments]   ${job_name}
    ${arguments}=   Create List   10  670  1300   3
    ${submitbody}=    Create Dictionary   name=${job_name}   language=Scala   main_class=org.apache.spark.examples.GroupByTest    path_to_main_app_file=local:///opt/spark/examples/jars/spark-examples_2.11-2.4.0.jar      label=systemTest      arguments=${arguments}
    ${response}=    Post Request With Json Body   /piezo/submitjob    ${submitbody}
    [return]  ${response}

Wait For Spark Job To Finish
    [Arguments]    ${job_name}
    :For    ${i}    IN RANGE   0    24
    \   Sleep     5 seconds
    \   ${response}=   Get Status Of Spark Job   ${job_name}
    \   ${message}=  Get Response Data Message     ${response}
    \   ${finished}=    Set Variable If     '${message}'=='COMPLETED'   ${True}     ${False}
    \   Exit For Loop If    ${finished}
    [return]    ${finished}
