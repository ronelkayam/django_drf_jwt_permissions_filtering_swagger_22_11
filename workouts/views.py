from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Workout
from .serializers import WorkoutSerializer, RegisterSerializer
from .permissions import IsOwnerOrReadOnly


class RegisterView(generics.CreateAPIView):
    """
    נקודת קצה להרשמת משתמש חדש
    פתוחה לכולם כי בנוקדה הזאת למשתמש עדיין אין TOKEN
    """
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    נקודצת קצה מלאה לניהול אימונים CRUD
    כוללת:
    הרששאת בעלות +JWT אימות
    סינון לפי שדות וחיפוש טקטואלי (workout_type)
    חלוקה לעמודים (מוגדרת בsettings.py)
    """

    queryset = Workout.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = WorkoutSerializer

    # הגדרת מנועי הסינון חיפוש ומיון
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['workout_type']
    search_fields = ['title', 'notes']
    ordering_fields = ['duration_minutes', 'calories_burned', 'created_at']

    def perform_create(self, serializer):
        """
        בעת יצירת אימון חדש תקשר אותו אוטומטית למשתמש המחובר
        מתוך JWT!!!
        """
        serializer.save(user=self.request.user)
