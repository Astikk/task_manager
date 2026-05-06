# 🚀 Team Task Manager (Full-Stack Backend)

A simple yet powerful backend system built with **Django REST Framework + PostgreSQL** that allows users to manage projects, assign tasks, and track progress with role-based access.

---

# 📌 Features

* 🔐 JWT Authentication (Signup/Login)
* 📁 Project Management
* 👥 Team Member Management (Admin / Member roles)
* ✅ Task Creation & Assignment
* 📊 Dashboard (task stats + overdue tracking)
* 🔒 Role-Based Access Control

---

# 🛠️ Tech Stack

* Backend: Django, Django REST Framework
* Database: PostgreSQL
* Auth: JWT (`djangorestframework-simplejwt`)
* Deployment: Railway

---

# ⚙️ Setup Instructions (Local)

## 1. Clone repo

```bash
git clone <your-repo-url>
cd task_manager
```

---

## 2. Create virtual env

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Setup environment variables

Create `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True
postgresPassword=your_postgres_password
```

---

## 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 6. Run server

```bash
python manage.py runserver
```

---

# 🔐 Authentication APIs

## Signup

```http
POST /api/signup/
```

```json
{
  "username": "user1",
  "email": "user1@gmail.com",
  "password": "123456"
}
```

---

## Login (Get Token)

```http
POST /api/token/
```

```json
{
  "username": "user1",
  "password": "123456"
}
```

### Response:

```json
{
  "access": "your_access_token",
  "refresh": "your_refresh_token"
}
```

---

## 🔑 Use Token in Headers

```http
Authorization: Bearer <access_token>
```

---

# 📁 Project APIs

## Create Project

```http
POST /api/projects/
```

```json
{
  "name": "Project A",
  "description": "Test project"
}
```

👉 Creator becomes **ADMIN automatically**

---

## Get User Projects

```http
GET /api/projects/
```

👉 Returns only projects where user is a member

---

# 👥 Member Management

## Add Member (Admin Only)

```http
POST /api/projects/<project_id>/add-member/
```

```json
{
  "user_id": 2,
  "role": "MEMBER"
}
```

### Rules:

* Only ADMIN can add members
* Duplicate members not allowed

---

# ✅ Task APIs

## Create Task

```http
POST /api/tasks/
```

```json
{
  "title": "Fix Bug",
  "description": "API issue",
  "project": 1,
  "assigned_to": 2,
  "status": "TODO",
  "due_date": "2026-05-10"
}
```

### Rules:

* User must belong to project
* Assigned user must be a project member

---

## Get Tasks

```http
GET /api/tasks/
```

👉 Returns tasks from user's projects only

---

# 📊 Dashboard API

## Get Task Summary

```http
GET /api/dashboard/
```

### Response:

```json
{
  "total_tasks": 10,
  "completed_tasks": 4,
  "pending_tasks": 6,
  "overdue_tasks": 2
}
```

---

# 🚀 Deployment (Railway)

## Steps:

1. Push code to GitHub
2. Go to Railway → Create Project
3. Deploy from GitHub
4. Add environment variables:

```env
SECRET_KEY=your_secret
DEBUG=False
DATABASE_URL=your_railway_postgres_url
ALLOWED_HOSTS=your-app.up.railway.app
```

---

## Procfile

```
web: gunicorn task_manager.wsgi
```

---

## Install required packages

```bash
pip install gunicorn dj-database-url psycopg2-binary
```

---

# 📦 Important Notes

* Do NOT use `localhost` in production DB
* Always use JWT token for protected APIs
* Admin role controls team management
* Data is isolated per user/project

---

# 🎥 Demo Checklist

Make sure your demo video shows:

* Signup & Login
* Create Project
* Add Member
* Create Task
* Dashboard

---

# 👨‍💻 Author

Built as part of a full-stack assignment using Django REST Framework.

---
