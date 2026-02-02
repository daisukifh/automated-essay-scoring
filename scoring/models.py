from django.db import models

class Question(models.Model):
    title = models.CharField(max_length=200)
    prompt_text = models.TextField()
    reference_answer = models.TextField(help_text="The model answer to compare against.")
    min_score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Essay(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='essays')
    student_name = models.CharField(max_length=100)
    content = models.TextField()
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.question.title}"
