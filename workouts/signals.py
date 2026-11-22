from datetime import datetime, timezone
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pymongo import MongoClient
from .models import Workout


def get_mongo_collection():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DATABASE]  # תוקן מ-MONGO_DBATABASE
    return db['audit_logs']  # שם ה-Collection בתוך מסד הנתונים workout_tracker_log


@receiver(post_save, sender=Workout)
def log_workout_save(sender, instance, created, **kwargs):
    """
    מופעל אוטומטית מיד לאחר שאימון נשמר ב-SQL Server.
    created=True אומר שזו רשומה חדשה (CREATE), אחרת זה עדכון (UPDATE).
    """
    action = 'CREATE' if created else 'UPDATE'
    collection = get_mongo_collection()

    log_document = {
        'action': action,
        'workout_id': instance.id,
        'username': instance.user.username,
        'workout_title': instance.title,
        'workout_type': instance.workout_type,
        'duration_minutes': instance.duration_minutes,
        'timestamp': datetime.now(timezone.utc),
    }
    collection.insert_one(log_document)


@receiver(post_delete, sender=Workout)
def log_workout_delete(sender, instance, **kwargs):
    """
    מופעל אוטומטית מיד לאחר שאימון נמחק מ-SQL Server.
    """
    collection = get_mongo_collection()
    log_document = {
        'action': 'DELETE',
        'workout_id': instance.id,
        'username': instance.user.username,
        'workout_title': instance.title,
        'timestamp': datetime.now(timezone.utc),
    }
    collection.insert_one(log_document)