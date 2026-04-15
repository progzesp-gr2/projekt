from django.urls import path # Importujemy funkcję definiującą ścieżki.
from . import views # Importujemy widoki z lokalnego pakietu.

urlpatterns = [ # Lista ścieżek specyficznych dla modułu Scrum.
    # Usunęliśmy 'api/' z początku, bo zostanie ono dodane automatycznie przez plik główny.
    # Dodaliśmy '/' na końcu każdego adresu dla spójności.
    
    
    # --- ENDPOINTY AUTORYZACJI ---
    path('auth/register/', views.RegisterView.as_view(), name='auth-register'), # Rejestracja.
    path('auth/login/', views.LoginView.as_view(), name='auth-login'), # Logowanie.
    path('auth/logout/', views.LogoutView.as_view(), name='auth-logout'), # Wylogowanie.
    path('auth/me/', views.MeView.as_view(), name='auth-me'), # Dane profilowe.


    # --- ENDPOINTY ZARZĄDZANIA PROJEKTEM I ZADANIAMI ---
    path('projects/', views.ProjectListCreateView.as_view(), name='project-list-create'), # Projekty.
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'), # Zadania (Lista/Tworzenie).
    path('tasks/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'), # Konkretne zadanie (Edycja).
    path('sprints/', views.SprintListCreateView.as_view(), name='sprint-list-create'), # Sprinty.
]

















from django.urls import path # Importujemy funkcję definiującą ścieżki.
from . import views # Importujemy widoki z lokalnego pakietu.

urlpatterns = [ # Lista ścieżek specyficznych dla modułu Scrum.
    # Usunęliśmy 'api/' z początku, bo zostanie ono dodane automatycznie przez plik główny.
    # Dodaliśmy '/' na końcu każdego adresu dla spójności.
    


    path('projects/', views.ProjectListCreateView.as_view(), name='project-list-create'), # Projekty.
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'), # Zadania (Lista/Tworzenie).
    path('tasks/<int:pk>/', views.TaskUpdateView.as_view(), name='task-update'), # Konkretne zadanie (Edycja).
    path('sprints/', views.SprintListCreateView.as_view(), name='sprint-list-create'), # Sprinty.
]