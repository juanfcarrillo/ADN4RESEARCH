
from design.models.research_question_models import ResearchFramework, ResearchQuestion
from config.events import bus
from django.db.models import Q
from django.contrib.auth import get_user_model

# Obtén el modelo de Usuario activo en tu proyecto
User = get_user_model()

class ResearchQuestionService:
    def define_status(self, research_question):
        if research_question.status in ['SUGGESTED', 'APPROVED', 'REJECTED', 'SUGGEST_REJECT']:
            return research_question.status
        calculated_status = research_question.calculate_status()
        if research_question.status != calculated_status:
            research_question.status = calculated_status
            research_question.save(update_fields=['status', 'modified_at'])
        return calculated_status
    
    def get_research_question_by_id(self, research_question_id):
        return ResearchQuestion.objects.get(id=research_question_id)
    
    def get_framework_by_id(self, framework_id):
        return ResearchFramework.objects.get(id=framework_id)
    
    def submit_research_question_for_review(self, research_question):
        if self.can_submit_for_review(research_question):
            research_question.status = 'SUGGESTED'
            suggested_question_text = research_question.suggested_question
            bus.publish("research_question_submitted", {"question": suggested_question_text})
            research_question.save()
        return print("No puede subir")
        
    def can_submit_for_review(self, research_question):
        return research_question.status == 'READY_TO_SEND'
        
    def suggest_rejecting_question(self, research_question, suggester , justification):
        research_question.status = 'SUGGEST_REJECT'
        research_question.suggester  = suggester
        research_question.justification = justification
        research_question.save()
        
    def autosave_question(self, data, user):
        question_id = data.get('id') or None
        framework_id = data.get('research_framework')
        # OJITOOOOOO QUITARRRR
        hardcoded_user = User.objects.get(id=1)
        researcher_instance = hardcoded_user if hardcoded_user else None
        framework = self.get_framework_by_id(framework_id)
        framework_fields_data = {
            key.replace('framework_fields[', '').replace(']', ''): value
            for key, value in data.items() if key.startswith('framework_fields[')
        }
        if question_id:
            question = ResearchQuestion.objects.get(id=question_id)
            question.research_framework = framework
            question.researcher = researcher_instance
            question.motivation = data.get('motivation', '')
            question.framework_fields = framework_fields_data
            question.suggested_question = data.get('suggested_question', '')
            question.save()
        else: 
            question = ResearchQuestion.objects.create(
                research_framework=framework,
                suggested_question=data.get('suggested_question', ''),
                motivation=data.get('motivation', ''),
                researcher=researcher_instance,
                framework_fields=framework_fields_data,
                
            )
        return question
    
    def get_question_by_id(self, question_id):
        return ResearchQuestion.objects.get(id=question_id)
    
    def get_all_questions_by_user(self, user):
        return ResearchQuestion.objects.filter(researcher=user).order_by('-modified_at')
    
    def get_frameworks(self, request):
        frameworks = ResearchFramework.objects.filter(Q(is_global=True) | Q(created_by=request.user))
        return frameworks