"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from core.views import root_view, SignupView, ProjectView, AddMemberView, TaskView, DashboardView

urlpatterns = [
    path('', root_view, name='root'),
    path('api/token/', TokenObtainPairView.as_view()),  # login
    path('api/signup/', SignupView.as_view()),
    path('api/projects/', ProjectView.as_view()),
    path('api/projects/<int:project_id>/add-member/', AddMemberView.as_view()),
    path('api/tasks/', TaskView.as_view()),
    path('api/dashboard/', DashboardView.as_view()),
]