*** Test Cases ***
Example Test Case
    Log To Console    shrek
    Some Example Keywords    csao    megint

*** Keywords ***
Some Example Keywords
    [Arguments]    ${first_arg}    ${second_arg}
    Log To Console    csao
    Sleep    5s
    Log To Console    csao megint
