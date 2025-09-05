*** Settings ***
Documentation     End-to-end flow: HR posts job, Employee applies
Library           SeleniumLibrary

*** Variables ***
${BROWSER}        Chrome
${URL}            http://localhost:5000
${HR_EMAIL}       hr@test.com
${HR_PASSWORD}    1234
${EMP_EMAIL}      employee@test.com
${EMP_PASSWORD}   1234
${JOB_TITLE}      Python Developer
${JOB_DESC}       Looking for an experienced Python developer.
${JOB_LOCATION}   Bangalore

*** Test Cases ***
HR Can Post A Job
    [Documentation]    HR logs in and posts a new job
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Input Text    name=email    ${HR_EMAIL}
    Input Text    name=password    ${HR_PASSWORD}
    Click Button    xpath=//button[text()='Login']
    Page Should Contain    HR Dashboard
    Click Link    xpath=//a[text()='Post a New Job']
    Input Text    name=title    ${JOB_TITLE}
    Input Text    name=description    ${JOB_DESC}
    Input Text    name=location    ${JOB_LOCATION}
    Click Button    xpath=//button[text()='Submit']
    Page Should Contain    Job posted successfully
    Close Browser

Employee Can Apply For Job
    [Documentation]    Employee logs in and applies for the job
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Input Text    name=email    ${EMP_EMAIL}
    Input Text    name=password    ${EMP_PASSWORD}
    Click Button    xpath=//button[text()='Login']
    Page Should Contain    Employee Dashboard
    Click Link    xpath=//a[text()='View Jobs']
    Page Should Contain    ${JOB_TITLE}
    Click Link    xpath=//a[contains(text(),'Apply')]
    Page Should Contain    Application submitted successfully
    Close Browser
