from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from pymongo import MongoClient
from .models import Workout


class WorkoutAPITests(APITestCase):
    def setUp(self):
        """
        פונקציה שרצה לפני כל בדיקה/טסט
        מכינה נתוני התחלה נקיים
        """
        self.user_a = User.objects.create_user(username='moshe', password='pass123!00')
        self.user_b = User.objects.create_user(username='david', password='ILoveDJango!')

        # ניקוי לוגים קודמים ב-Mongo לפני הבדיקה (תואם ל-settings.py ול-signals.py)
        client = MongoClient(settings.MONGO_URI)
        self.mongo_collection = client[settings.MONGO_DATABASE]['audit_logs']
        self.mongo_collection.delete_many({})

        # יצירת אימון של Moshe - יפעיל אוטומטית signal
        self.workout_moshe = Workout.objects.create(
            user=self.user_a,
            title='Morning Run',
            workout_type='Cardio',
            duration_minutes=45,
            calories_burned=400
        )

        # יצירת אימון נוסף למשה שנוכל לסנן את האימונים
        self.workout_moshe_strength = Workout.objects.create(
            user=self.user_a,
            title='Heavy Squats',
            workout_type='Strength',
            duration_minutes=60,
            calories_burned=350
        )

        self.list_url = reverse('workout-list')
        self.detail_url = reverse('workout-detail', kwargs={'pk': self.workout_moshe.id})

    def test_dual_db_sync_on_created_and_delete(self):
        # וידוי שהרישום והמחיקה ל-Mongo מתבצעים
        create_logs = self.mongo_collection.count_documents({'action': 'CREATE'})
        self.assertEqual(create_logs, 2)

        # משה מוחק את האימון הספציפי דרך API (חובה להשתמש ב-detail_url)
        self.client.force_authenticate(user=self.user_a)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # עבור האימון שנמחק וידוא שנכתב לוג ל-mongo
        delete_log = self.mongo_collection.find_one({
            'action': 'DELETE',
            'workout_id': self.workout_moshe.id
        })
        self.assertIsNotNone(delete_log)
        self.assertEqual(delete_log['username'], 'moshe')

    def test_custom_permission_prevent_other_user_delete(self):
        # מוודא שמשתמש אחד לא יכול למחוק לשני אימונים
        self.client.force_authenticate(user=self.user_b)

        # מנסה למחוק את האימון הספציפי של מתאמן 1 (חובה להשתמש ב-detail_url)
        response = self.client.delete(self.detail_url)

        # השרת חייב לחסום עם 403 כי אין הרשאת בעלים
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Workout.objects.filter(id=self.workout_moshe.id).exists())

    def test_filtering_by_workout_type(self):
        # מחזיר רק תוצאות מתאימות בסינון
        self.client.force_authenticate(user=self.user_b)
        response = self.client.get(self.list_url, {'workout_type': 'Cardio'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # בגלל שהפעלנו pagination התוצאות נמצאות תחת המפתח 'results' (ברבים)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Morning Run')
        self.assertEqual(results[0]['workout_type'], 'Cardio')