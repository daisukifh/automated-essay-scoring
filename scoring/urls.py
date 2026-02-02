from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setup/', views.create_question, name='create_question'),
    path('question/<int:question_id>/', views.submit_essay, name='submit_essay'),
    path('result/<int:essay_id>/', views.result, name='result'),
]
