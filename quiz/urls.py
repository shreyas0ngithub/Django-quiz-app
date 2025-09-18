from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/result/', views.quiz_result, name='quiz_result'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('history/', views.quiz_history, name='history'),
]