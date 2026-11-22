from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Workout


class RegisterSerializer(serializers.ModelSerializer):
    """
    מערכת להרשמת משתמש חדש
    מבטיח שהסיסמא תישמור מוצפנת ולא כטקסט גלוי
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        # sql_server ידאג להצפין את הסיסמא אוטומטית בcreate_user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data('email', ''),
            password=validated_data['password']
        )
        return user

class WorkoutSerializer(serializers.ModelSerializer):
    """
    ניהול אובייקש של אימון
    """
    owner_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Workout
        fields = [
            'id',
            'owner_username',
            'title',
            'workout_type',
            'duration_minutes',
            'calories_burned',
            'notes',
            'created_at',
            'updated_at',
        ]
        #השדות האלה מנוהלים ע"י השרת והמשתמש לא יכול לזייף אותם
        read_only_fields = ['id', 'owner_username', 'created_at', 'updated_at']

    def validate_duration_minutes(self, value):
        """
        בדיקה תקינות עסקית
        אימון חייב להיות לפחות מעל דקה
        """
        if value <= 0:
            raise serializers.ValidationError("Error! Duration minutes must be >=1!")
        return value