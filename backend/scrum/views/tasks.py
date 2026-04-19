from rest_framework import generics 
from rest_framework.permissions import IsAuthenticated 
from scrum.models import Task 
from scrum.serializers.tasks import TaskSerializer 

class TaskListCreateView(generics.ListCreateAPIView): # Tworzymy klasę widoku dziedziczącą po ListCreateAPIView (obsługuje zapytania GET dla listy i POST dla tworzenia).
    queryset = Task.objects.all() # Określamy pulę danych roboczych: widok ma pracować na wszystkich istniejących zadaniach w bazie.
    serializer_class = TaskSerializer # Informujemy widok, jakiego tłumacza (serializatora) ma użyć do formatowania danych wejściowych i wyjściowych.
    permission_classes = [IsAuthenticated] # Zabezpieczamy ten endpoint: jeśli żądanie nie ma poprawnego tokena JWT, serwer zwróci błąd 401 (Brak autoryzacji).
