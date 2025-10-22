Feature: Managing the lifecycle of research questions
    As a researcher
    I want to maintain control over the evolution of my research questions
    So that I can ensure their proper validation throughout the systematic review.

    Scenario: Submit a suggested research question for review
        Given the "Suggest Research Question" stage of the project is opened
        And I have written a question with the following content:
            """
            {
                "framework": "PICO",
                "fields": {
                    "Population": "Students",
                    "Intervention": "Gamification",
                    "Context": "Online courses",
                    "Outcome": "Motivation"
                },
                "suggested_question": "PREGUNTA EJEMPLO",
                "motivation": "MOTIVACION TEXTO EJEMPLO"
            }
            """
        And the question is on a "READY_TO_SEND" status
        When I submit the question for review
        Then the question should change its status to "SUGGESTED"
        And a "RESEARCH_QUESTION_SUBMITTED_FOR_REVIEW" notification should be sent to the research project team

    Scenario: Propose to reject a suggested research question
        Given the "Research Question Discusion" stage of the project is opened
        And there exist a "SUGGESTED" question
        When I suggest to reject the question with the justification "No aligned with project objectives"
        Then the question status should change to "SUGGEST_REJECT"
        And a "SUGGESTION_QUESTION_REJECT" notification should be sent to the research project team
        
'''
    Scenario Outline: Autosave a research question
        Given I chose the <framework> framework
        When I have completed <completed_framework_fields>
        And I write a <suggested_question> text
        And I write a <motivation> for the question
        Then the question status should be <status>
        Examples:
            | framework | completed_framework_fields | suggested_question | motivation | status        |
            | PICO      | 4                          | Example            | abc        | READY_TO_SEND |
            | PICO      | 3                          | Example2           | ass        | DRAFT         |
            | PEO       | 3                          |                    |            | DRAFT         |
            | PEO       | 2                          |                    |            | DRAFT         |
            | PCC       | 1                          |                    |            | DRAFT         |
            | PCC       | 3                          | Example3           | abc        | READY_TO_SEND |
            | PCC       | 0                          |                    |            | DRAFT         |
    
    Scenario Outline: Autosave a research question
        Given the "Suggested Research Question" stage of the project is opened
        And I have completed <completed_framework_fields> fields of the selected <framework> framework
        And the suggested question text is "<suggested_question>"
        When the system receives a save progress request
        Then the question should be saved with status "<status>"
        Examples:
            | framework | completed_framework_fields | suggested_question | status        |
            | PICO      | 4                          | Example            | READY_TO_SEND |
            | PICO      | 3                          | Example2           | DRAFT         |
            | PEO       | 3                          |                    | DRAFT         |
            | PEO       | 2                          |                    | DRAFT         |
            | PCC       | 1                          |                    | DRAFT         |
            | PCC       | 3                          | Example3           | READY_TO_SEND |
            | PCC       | 0                          |                    | DRAFT         |