# 🏋️ Workout Tracker API (Django REST Framework + Dual-DB)

A production-grade RESTful API for managing personal workouts, built with **Django 5.2**, **Django REST Framework (DRF)**, **JWT Authentication**, **OpenAPI/Swagger**, and a **Dual-Database Architecture** combining **Microsoft SQL Server** and **MongoDB**.

---

## 🏗️ Architecture & Key Features

* **RESTful API (DRF):** Full CRUD operations for workouts via `ModelViewSet` and `DefaultRouter`.
* **JWT Authentication (`djangorestframework-simplejwt`):** Stateless user registration, login, and token-based authentication (`Access` & `Refresh` tokens).
* **Dual-Database Persistence (Polyglot Architecture):**
  * **Microsoft SQL Server (`mssql-django`):** Primary relational database storing users and workout records.
  * **MongoDB (`pymongo`):** NoSQL document store automatically recording audit logs (`CREATE`, `UPDATE`, `DELETE`) for every workout change.
* **Event-Driven Audit Logging (`Django Signals`):** `post_save` and `post_delete` receivers automatically synchronize workout actions to MongoDB in real time.
* **Object-Level Permissions (`IsOwnerOrReadOnly`):** Any authenticated user can view workouts, while only the workout owner can update or delete their own records.
* **Dynamic Filtering, Search & Pagination:** Filter by workout type (`?workout_type=Cardio`), search text (`?search=Run`), sort results, and paginate responses (`PAGE_SIZE = 4`).
* **Interactive API Documentation (`drf-spectacular`):** Live Swagger UI at `/api/docs/` with built-in JWT Bearer authorization.
* **Automated Integration Tests:** Full test suite covering permissions, filtering, and SQL-to-MongoDB synchronization.

---

## 🛠️ Tech Stack

* **Backend:** Python 3.10+, Django 5.2.19, Django REST Framework 3.15.1
* **Auth:** SimpleJWT 5.3.1
* **Primary DB:** Microsoft SQL Server (`mssql-django` 2.0.0)
* **Audit Logs DB:** MongoDB (`pymongo` 4.7.2)
* **Docs & Filtering:** `drf-spectacular` 0.27.2, `django-filter` 24.2

---

## ⚙️ Prerequisites (Windows)

1. **Python 3.10+** installed and added to `PATH`.
2. **Microsoft SQL Server** running locally with **TCP/IP enabled** on port `1433` and an empty database named `WorkoutTrackerDB`.
3. **MongoDB Community Server** running locally on `mongodb://localhost:27017/`.

---

## 🚀 Setup & Installation (CMD)

### 1. Clone the repository & create a virtual environment
```cmd
git clone https://github.com/ronelkayam/django_drf_jwt_permissions_filtering_swagger_22_11
cd workout_tracker_project_22_11_26

python -m venv venv
venv\Scripts\activate