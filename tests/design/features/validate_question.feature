Feature: Validate the researchers research question
    As an owner of the research project
    I want to maintain control over the research questions of my project
    So that I can ensure a proper validation of them and keep traceability.

    # este escenario puede contener mas cosas como un suggested_reject, suggested, union suggested, etc
    Scenario Outline: Research owner approves a state of the research question
        Given the "Suggest Research Question" stage of the project is opened
        And there are research question versions with status <question_status> awaiting validation
        When the owner approves the question with the justification <justification>
        Then the question status should to "APPROVED"
        And a history record should be created with approver, justification, and date
        And all members of the research project should receive a notification of the approval

        Examples:
            | question_status | justification |
            | SUGGEST_REJECT  | BABABA        |
            | SUGGESTED       | BABABA        |


