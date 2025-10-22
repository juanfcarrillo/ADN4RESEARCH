
class ProjectService:
    def add_member(self, project, user, role):
        # Implementation to add a member to the project with a specific role
        project.add_member(user, role)

    def open_stage(self, stage, opened_by, due_time):
        # Implementation to open a stage of the project
        stage.status = "OPENED"
        stage.opened_by = opened_by
        stage.due_time = due_time
        stage.save()

    def is_stage_opened(self, stage):
        return stage.status == "OPENED"
    
    def submit_research_question_for_review(self, research_question):
        research_question.status = 'SUGGESTED'
        research_question.save()
    
    def get_project_members(self, project):
        return project.get_members()
    
    def suggest_rejecting_question(self, research_question, suggester , justification):
        research_question.status = 'SUGGEST_REJECT'
        research_question.suggester  = suggester
        research_question.justification = justification
        research_question.save()