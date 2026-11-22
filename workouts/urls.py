from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import WorkoutViewSet,RegisterView

router = DefaultRouter()
router.register('workouts',WorkoutViewSet,basename='workout')

urlpatterns = [
    path('register/', RegisterView.as_view(),name='auth-register'),
    path('', include(router.urls)),
]