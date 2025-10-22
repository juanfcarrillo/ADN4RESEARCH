
from design.models import ResearchQuestion


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