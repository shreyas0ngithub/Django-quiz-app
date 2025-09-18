from django.contrib import admin

# Register your models here.
from .models import Quiz, Question, Answer, UserQuizResult, UserAnswer

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    max_num = 4

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    show_change_link = True

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'question_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    inlines = [QuestionInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new quiz
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['question_text']
    inlines = [AnswerInline]
    list_editable = ['order']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['answer_text']

@admin.register(UserQuizResult)
class UserQuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'total_questions', 'percentage', 'passed', 'completed_at']
    list_filter = ['quiz', 'completed_at']
    search_fields = ['user__username', 'quiz__title']
    readonly_fields = ['percentage', 'passed']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']
    search_fields = ['user__username']