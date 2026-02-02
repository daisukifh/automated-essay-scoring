from django import forms
from .models import Question, Essay

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'prompt_text', 'reference_answer', 'min_score', 'max_score']
        widgets = {
            'prompt_text': forms.Textarea(attrs={'rows': 4}),
            'reference_answer': forms.Textarea(attrs={'rows': 6}),
        }

class EssayForm(forms.ModelForm):
    class Meta:
        model = Essay
        fields = ['student_name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write your essay here...'}),
        }
