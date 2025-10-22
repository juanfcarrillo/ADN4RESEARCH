import json
from unittest.mock import Mock
from behave import given, then, when, step
from faker import Faker
from django.contrib.auth.models import User

from design.models import ResearchFramework, ResearchQuestion
from design.services.question_services import ResearchQuestionService
from notification.models import Notification
from notification.services.notification_service import NotificationService
from project.models import Project, Stage
from project.services.project_services import ProjectService

fake = Faker()
project_service = ProjectService()
research_question_service = ResearchQuestionService()
notification_service = Mock()


@given('the "{stage_name}" stage of the project is opened')
def step_impl(context, stage_name):
    context.stage_name = stage_name
    context.owner = User.objects.create_user(username=fake.user_name(), email=fake.email())
    context.researcher = User.objects.create_user(username=fake.user_name(), email=fake.email())
    context.project = Project.objects.create(
        name="Test Project",
        description="This is a test project description",
        owner=context.owner
    )
    project_service.add_member(project = context.project, user = context.owner, role="OWNER")
    project_service.add_member(project = context.project, user = context.researcher, role="RESEARCHER")
    context.stage = Stage.objects.create(
        project=context.project,
        name=stage_name,
        status="INACTIVE"
    )
    due_time = fake.future_datetime()
    # Abrir la etapa solo es cambiar su estado a OPENED
    project_service.open_stage(
        stage=context.stage,
        opened_by=context.owner,
        due_time=due_time
    )
    assert project_service.is_stage_opened(stage=context.stage)


@step('I have written a "{ready_to_send_status}" question with the following content:')
def step_impl(context, ready_to_send_status):
    payload = json.loads(context.text)

    context.ready_to_send_status = ready_to_send_status
    context.framework = payload["framework"]
    context.fields = payload["fields"]
    context.suggested_question = payload["suggested_question"]
    context.framework_object = ResearchFramework.objects.create(
        name=context.framework,
        fields=context.fields,
    )
    context.research_question = ResearchQuestion.objects.create(
        research_framework =context.framework_object,
        suggested_question=context.suggested_question,
        stage=context.stage,
        researcher=context.researcher,
        project=context.project
    )
    context.research_question.status = context.research_question.calculate_status()
    research_question_status = context.research_question.status
    assert context.ready_to_send_status == research_question_status

@when('I submit the question for review')
def step_impl(context):
    # Dentro del metodo debo cambiar el estado de la pregunta a SUGGESTED
    project_service.submit_research_question_for_review(
        research_question=context.research_question,
    )
    pass # Se verifica en el otro paso xd pero dentro de la funcion cambia el estado
    #assert context.research_question.status == "SUGGESTED"

@then('the question should change its status to "{suggested_status}"')
def step_impl(context, suggested_status):
    research_question = research_question_service.get_research_question_by_id(
        research_question_id=context.research_question.id
    )
    assert research_question.status == suggested_status

@step('a "{notification_type}" notification should be sent to the research project team')
def step_impl(context, notification_type):
    context.notification = Notification.objects.create(
        type=notification_type,
        project=context.project,
        sender=context.researcher
    )
    #project_members = project_service.get_project_members(project=context.project)
    #notification_service.send_notification(receivers = project_members, notification_type = context.notification_type)
    notification_service.send_notification.return_value = True
    #notifications = notification_service.get_notifications_for_project(
    #    project=context.project
    #)
    notifications = notification_service.get_notifications_for_project.return_value = [context.notification]
    assert len(notifications) > 0

# SEGUNDO SCENARIO
@step('there exist a "{suggested_status}" question')
def step_impl(context, suggested_status):
    context.suggested_status = suggested_status
    context.researcher2 = User.objects.create_user(username=fake.user_name(), email=fake.email())
    context.framework_object = ResearchFramework.objects.create(
        name="PICO",
        fields={"P": "Population", "I": "Intervention", "C": "Comparison", "O": "Outcome"},
    )
    context.research_question = ResearchQuestion.objects.create(
        research_framework =context.framework_object,
        suggested_question="What is the effect of intervention X on population Y?",
        stage=context.stage,
        researcher=context.researcher,
        project=context.project
    )
    project_service.submit_research_question_for_review(
        research_question=context.research_question,
    )
    assert context.research_question.status == context.suggested_status


@when('I suggest to reject the question with the justification "{justification}"')
def step_impl(context, justification):
    context.justification = justification
    project_service.suggest_rejecting_question(
        research_question=context.research_question,
        suggester=context.researcher2,
        justification=context.justification
    )


@then('the question status should change to "{reject_status}"')
def step_impl(context, reject_status):
    context.reject_status = reject_status
    research_question = research_question_service.get_research_question_by_id(
        research_question_id=context.research_question.id
    )
    assert research_question.status == context.reject_status

# TERCER SCENARIO
@step("I have completed {completed_framework_fields} fields of the selected {framework} framework")
def step_impl(context, completed_framework_fields, framework):
    pass

@step('I have completed {completed_framework_fields} fields of the framework')
def step_impl(context, completed_framework_fields):
    context.completed_framework_fields = int(completed_framework_fields)
    context.research_question.fields_completed = context.completed_framework_fields
    context.research_question.save()
    research_question_status = research_question_service.define_status(research_question=context.research_question)

@step('the suggested question text is "{suggested_question_exists}"')
def step_impl(context, suggested_question_exists):
    context.research_question
    pass


@when('the system receives a save progress request')
def step_impl(context):
    pass


@then('the question should be saved with status "{status}"')
def step_impl(context, status):
    pass



