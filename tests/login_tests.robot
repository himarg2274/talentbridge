*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${URL}         http://localhost:5000/login
${EMP_EMAIL}   employee@test.com
${EMP_PASS}    1234
${HR_EMAIL}    hr@test.com
${HR_PASS}     1234

*** Test Cases ***
Valid Employee Login
    Open Browser    ${URL}    chrome
    Input Text    id=email    ${EMP_EMAIL}
    Input Text    id=password    ${EMP_PASS}
    Click Button    id=login-btn
    Page Should Contain    Employee Dashboard
    Close Browser

Valid HR Login
    Open Browser    ${URL}    chrome
    Input Text    id=email    ${HR_EMAIL}
    Input Text    id=password    ${HR_PASS}
    Click Button    id=login-btn
    Page Should Contain    Post a New Job
    Close Browser

Invalid Login - Wrong Password
    Open Browser    ${URL}    chrome
    Input Text    id=email    ${EMP_EMAIL}
    Input Text    id=password    wrongpass
    Click Button    id=login-btn
    Page Should Contain    Incorrect password
    Close Browser
