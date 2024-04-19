*** Test Cases ***
Example Test Case
    Log To Console    shrek
    Sleep    4s
    Some Example Keywords    csao    megint

*** Keywords ***
Some Example Keywords
    [Arguments]    ${first_arg}    ${second_arg}
    Log To Console    csao
    Sleep    2s
    Log To Console    csao megint
