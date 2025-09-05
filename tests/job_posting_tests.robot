*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}       http://localhost:5000/login
${HR_EMAIL}  hr@test.com
${HR_PASS}   1234

*** Test Cases ***
HR Can Post New Job
    Open Browser    ${URL}    chrome
    Input Text    id=email    ${HR_EMAIL}
    Input Text    id=password    ${HR_PASS}
    Click Button    id=login-btn
    Click Button    id=post-job-btn
    Input Text    id=title       Software Engineer
    Input Text    id=location    Bangalore
    Click Button    id=submit
    Page Should Contain    Job posted successfully
    Close Browser
