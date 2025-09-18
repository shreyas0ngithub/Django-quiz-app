from django.db import models

from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('quiz:take_quiz', kwargs={'quiz_id': self.pk})
    
    @property
    def question_count(self):
        return self.questions.count()
    
class Question(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
    ]
    
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.quiz.title} - {self.question_text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.answer_text} ({'Correct' if self.is_correct else 'Incorrect'})"
    

class UserQuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'quiz']
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_questions}"
    
    @property
    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round((self.score / self.total_questions) * 100, 2)
    
    @property
    def passed(self):
        return self.percentage >= 60  # 60% passing grade

class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'question']
    
    def __str__(self):
        return f"{self.user.username} - {self.question.question_text[:30]}..."