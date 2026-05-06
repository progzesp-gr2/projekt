from django.urls import path

from . import views

urlpatterns = [
    path('api/auth/register', views.RegisterView.as_view(), name='auth-register'),
    path('api/auth/login', views.LoginView.as_view(), name='auth-login'),
    path('api/auth/logout', views.LogoutView.as_view(), name='auth-logout'),
    path('api/auth/me', views.MeView.as_view(), name='auth-me'),

    path('api/projects/', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('api/projects/<int:pk>', views.ProjectDetailView.as_view(), name='project-detail'),
    path('api/tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>', views.TaskDetailView.as_view(), name='task-detail'),
    path('api/sprints/', views.SprintListCreateView.as_view(), name='sprint-list-create'),
    path('api/sprints/<int:pk>', views.SprintDetailView.as_view(), name='sprint-detail'),
]
