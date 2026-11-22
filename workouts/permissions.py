from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    הרשאה מותאמת אישית:
    בקשות קריאה GET/HEAD/OPTIONS - מותרת לכל משתמש
    בקשות שינוי/מחיקה PUT/DELETE/PATCH  - מותרות רק לבעל האימון (בעל הרשאה מתאימה)
    """

    def has_object_permission(self, request, view, obj):
        #GET/HEAD/OPTIONS מתודות שלא משנות כלום נקראות SAFE_MOTHODS
        if request.method in permissions.SAFE_METHODS:
            return True

        #בודק אם המתשמש ששלח את הבקשה עבור כתיבה/מחיקה הוא בעל הרשאה
        return obj.user == request.user