from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, UserQuizResult
from django.db.models import Avg, Count, F

# Create your views here.

def home(request):
    """Home page view"""
    return render(request, 'quiz/home.html')

@login_required
def quiz_list(request):
    """Display list of available quizzes"""
    quizzes = Quiz.objects.filter(is_active=True)
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    """Handle quiz taking"""
    quiz = get_object_or_404(Quiz, id=quiz_id, is_active=True)
    questions = quiz.questions.all()
    
    if request.method == 'POST':
        # Process quiz submission
        score = 0
        total_questions = questions.count()
        
        for question in questions:
            selected_answer_id = request.POST.get(f'question_{question.id}')
            if selected_answer_id:
                selected_answer = get_object_or_404(Answer, id=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1
        
        # Save result
        result, created = UserQuizResult.objects.get_or_create(
            user=request.user,
            quiz=quiz,
            defaults={'score': score, 'total_questions': total_questions}
        )
        if not created:
            result.score = score
            result.save()
        
        return redirect('quiz:quiz_result', quiz_id=quiz.id)
    
    return render(request, 'quiz/take_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def quiz_result(request, quiz_id):
    """Display quiz results"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    result = get_object_or_404(UserQuizResult, user=request.user, quiz=quiz)
    
    percentage = (result.score / result.total_questions) * 100 if result.total_questions > 0 else 0
    
    return render(request, 'quiz/quiz_result.html', {
        'quiz': quiz,
        'result': result,
        'percentage': percentage
    })

# Add these new views
@login_required
def user_dashboard(request):
    """User dashboard with statistics and recent activity"""
    user_results = UserQuizResult.objects.filter(user=request.user)
    
    stats = {
        'total_quizzes': user_results.count(),
        'passed_quizzes': user_results.filter(score__gte = F('total_questions') * 0.6).count(),
        'average_score': user_results.aggregate(avg=Avg('score'))['avg'] or 0,
        'total_questions_answered': sum(result.total_questions for result in user_results),
    }
    
    recent_results = user_results[:5]
    available_quizzes = Quiz.objects.filter(is_active=True).exclude(
        id__in=user_results.values_list('quiz_id', flat=True)
    )[:3]
    
    return render(request, 'quiz/dashboard.html', {
        'stats': stats,
        'recent_results': recent_results,
        'available_quizzes': available_quizzes,
    })

@login_required
def quiz_history(request):
    """Show user's quiz history with filtering"""
    results = UserQuizResult.objects.filter(user=request.user).select_related('quiz')
    return render(request, 'quiz/history.html', {'results': results})