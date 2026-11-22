from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Workout(models.Model):
    WORKOUT_TYPES = [
        ('Strength', 'אימון כוח'),
        ('Cardio', 'אימון אירובי'),
        ('Flexibility', 'גמישות ומתיחות'),
        ('HIIT', 'אימון אינטרוולי עצים'),
    ]

    """
    קשר יחיד לרבים
    כל משתמש הרבה אימונים
    cascade - אם משתמש נמחק ימחקו האימונים שלו
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='workout',
                             verbose_name='מתאמן')
    title = models.CharField(max_length=50, verbose_name='כותרת האימון')
    workout_type = models.CharField(
        max_length=20,
        choices=WORKOUT_TYPES,
        default='Strength',
        verbose_name='סוג אימון')
    duration_minutes = models.PositiveIntegerField(default=30, verbose_name='משך בדקות')
    calories_burned = models.PositiveIntegerField(default=0, verbose_name='קלוריות שנשרפו')
    notes = models.TextField(blank=True, null=True, verbose_name='הערות')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='תאריך יצירה')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='תאריך עדכון אחרון')


    class Meta:
        #האימונים החדשים יופיעו ראשונים (חשוב לpagintation)
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title}"