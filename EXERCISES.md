# 🏋️ Lab Exercises: Workout Tracker API

The goal of these exercises is to practice extending a production-grade backend system using **Django ORM**, **DRF Serializers**, **Custom Actions**, **MongoDB**, and **Automated Tests**.

> **Guidelines:**
> * Complete the tasks in order (Basic -> Intermediate -> Advanced).
> * After each exercise, test your changes interactively via Swagger UI at `http://127.0.0.1:8000/api/docs/`.
> * Make sure all existing and new automated tests pass by running `python manage.py test`.

---

## 🟢 Exercise 1 (Basic): Model Extension, Filtering & Business Validation

**Goal:** Add workout completion tracking and prevent invalid data from being saved to the database.

1. **Update the Database Model (`workouts/models.py`):**
   * Add a new boolean field named `is_completed` to the `Workout` model with a default value of `False`.
   * Generate a new migration file and apply it to SQL Server (`makemigrations` and `migrate`).
2. **Extend Filtering (`workouts/views.py`):**
   * Update `filterset_fields` inside `WorkoutViewSet` so clients can filter workouts by completion status via URL query parameters (e.g., `GET /api/workouts/?is_completed=true`).
3. **Add Serializer Validation (`workouts/serializers.py`):**
   * Implement a `validate_calories_burned(self, value)` method inside `WorkoutSerializer`.
   * If `calories_burned` exceeds `5000`, raise a `serializers.ValidationError` with a clear error message.
4. **Verify in Swagger UI:**
   * Try creating a workout with `6000` calories via Swagger and verify that the server returns a `400 Bad Request` error.
   * Create a valid workout, mark it as `is_completed: true`, and verify that filtering on `GET /api/workouts/` returns only that record.

---

## 🟡 Exercise 2 (Intermediate): Custom Statistics Endpoint (`@action`)

**Goal:** Build a dedicated endpoint that computes database-level aggregations for the currently authenticated user only.

1. **Create a Custom Action (`workouts/views.py`):**
   * Import `action` from `rest_framework.decorators` and `Response` from `rest_framework.response`.
   * Inside `WorkoutViewSet`, add a new method decorated with `@action(detail=False, methods=['get'])` named `my_stats`.
   * This will automatically expose the endpoint: `GET /api/workouts/my_stats/`.
2. **Compute User Aggregations (`workouts/views.py`):**
   * Filter workouts belonging strictly to the requesting user (`Workout.objects.filter(user=request.user)`).
   * Return a JSON response with the following structure:
     ```json
     {
       "username": "moshe",
       "total_workouts": 5,
       "total_minutes": 210,
       "total_calories": 1850
     }
     ```
   * *(Hint: Use `aggregate(Sum('duration_minutes'), Sum('calories_burned'))` from `django.db.models`. Note that if a user has zero workouts, `Sum` returns `None` — handle this gracefully using `or 0`)*.
3. **Verify in Swagger UI:**
   * Log in with two different users, create separate workouts for each, and verify that `/api/workouts/my_stats/` displays only each user's personal summary.

---

## 🔴 Exercise 3 (Advanced): Exposing MongoDB Audit Logs via API

**Goal:** Complete the read side of the Dual-DB architecture by allowing authenticated users to query their own action history directly from MongoDB.

1. **Create an Audit Log View (`workouts/views.py`):**
   * Create a new class inheriting from `APIView` (from `rest_framework.views`) named `UserAuditLogView`.
   * Restrict access to authenticated users only (`permission_classes = [permissions.IsAuthenticated]`).
   * Inside the `get(self, request)` method, connect to the `audit_logs` collection inside `settings.MONGO_DATABASE` (you can reuse `get_mongo_collection()` from `signals.py`).
   * Query MongoDB for the **last 20 actions** performed by the logged-in user (`{'username': request.user.username}`), sorted from newest to oldest (`sort('timestamp', -1).limit(20)`).
   * **Important:** Exclude MongoDB's internal `_id` ObjectId field in your query projection (`{'_id': 0}`), otherwise JSON serialization will fail!
2. **Register the URL Route (`workouts/urls.py`):**
   * Wire the new view to `api/audit-logs/` (in `workouts/urls.py`, add `path('audit-logs/', UserAuditLogView.as_view(), name='audit-logs')`).
3. **Document in Swagger (`drf-spectacular`):**
   * Decorate the `get` method with `@extend_schema(responses={200: dict})` (from `drf_spectacular.utils`) so the endpoint appears cleanly in Swagger UI without schema warnings.

---

## 🧪 Exercise 4 (Bonus): Automated Integration Tests (`workouts/tests.py`)

**Goal:** Ensure the new features are protected against regressions.

1. Add a new test method named `test_user_stats_and_audit_logs_endpoints` inside `WorkoutAPITests`.
2. The test should:
   * Authenticate as `moshe` and send a `GET` request to `/api/workouts/my_stats/`.
   * Assert that `total_minutes` equals `105` (`45 + 60`) and `total_calories` equals `750` (`400 + 350`).
   * Send a `GET` request to `/api/audit-logs/` and assert that exactly 2 audit logs are returned for `moshe`, while another user (`david`) receives an empty list (`[]`).