from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Essay
from .forms import QuestionForm, EssayForm
from .logic import calculate_score

def index(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'scoring/index.html', {'questions': questions})

def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuestionForm()
    return render(request, 'scoring/create_question.html', {'form': form})

def submit_essay(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    if request.method == 'POST':
        form = EssayForm(request.POST)
        if form.is_valid():
            essay = form.save(commit=False)
            essay.question = question
            # Calculate score
            essay.score = calculate_score(essay.content, question.reference_answer, question.min_score, question.max_score)
            essay.save()
            return redirect('result', essay_id=essay.id)
    else:
        form = EssayForm()
    return render(request, 'scoring/submit_essay.html', {'form': form, 'question': question})

def result(request, essay_id):
    essay = get_object_or_404(Essay, id=essay_id)
    return render(request, 'scoring/result.html', {'essay': essay})
