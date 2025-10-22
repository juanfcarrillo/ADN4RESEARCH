from django.db import models

# Create your models here.
class ResearchQuestion(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('READY_TO_SEND', 'Ready to Send'),
        ('SUGGESTED', 'Suggested'),
        ('SUGGEST_REJECT', 'Suggest Reject'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    research_framework = models.ForeignKey('ResearchFramework', on_delete=models.CASCADE, related_name='research_questions')
    suggested_question = models.TextField(blank=True)
    motivation = models.TextField(blank=True)
    project = models.ForeignKey(
        'project.Project', 
        on_delete=models.CASCADE, 
        related_name='research_questions'
    )
    stage = models.ForeignKey('project.Stage', on_delete=models.CASCADE, related_name='research_questions')
    researcher = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='research_questions',
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT'
    )
    suggester = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        related_name='suggested_questions',
        null=True,
        blank=True
    )
    justification = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    @property
    def has_question_text(self):
        return bool(self.suggested_question and self.suggested_question.strip())
    
    @property
    def has_motivation(self):
        return bool(self.motivation and self.motivation.strip())
    
    @property
    def is_framework_complete(self):
        """Returns True if all framework fields are filled."""
        return self.research_framework.is_complete

    def calculate_status(self):
        if self.is_framework_complete and self.has_question_text and self.has_motivation:
            return 'READY_TO_SEND'
        return 'DRAFT'
    
    def __str__(self):
        return f"RQ-{self.id} ({self.status}) - {self.research_framework.name}"

class ResearchFramework(models.Model):
    FRAMEWORK_CHOICES = [
        ('PICO', 'PICO'),
        ('PEO', 'PEO'),
        ('PCC', 'PCC'),
    ]
    
    FRAMEWORK_REQUIRED_FIELDS = {
        'PICO': 4,
        'PEO': 3,
        'PCC': 3,
    }
    
    name = models.CharField(
        max_length=10, 
        choices=FRAMEWORK_CHOICES,
        unique=True
    )
    
    fields = models.JSONField(default=dict)
    
    @property
    def fields_completed(self):
        count = 0
        for field in self.fields.values():
            count += 1 if field and str(field).strip() else 0
        return count
    
    @property
    def total_required_fields(self):
        return self.FRAMEWORK_REQUIRED_FIELDS.get(self.name, 0)
    
    @property
    def is_complete(self):
        return self.fields_completed == self.total_required_fields