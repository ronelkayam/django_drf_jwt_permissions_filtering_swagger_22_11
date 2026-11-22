from django.contrib import admin
from .models import Workout

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'workout_type','duration_minutes','user','created_at')
    list_filter = ('workout_type','created_at')
    search_fields = ('title','user__username')

