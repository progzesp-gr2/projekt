from rest_framework import serializers # Importujemy główny moduł serializers z biblioteki Django REST Framework.
from scrum.models import Task # Importujemy model Task z głównego pliku models.py w aplikacji scrum.

class TaskSerializer(serializers.ModelSerializer): # Tworzymy klasę serializatora dziedziczącą po ModelSerializer, która zautomatyzuje konwersję na JSON.
    class Meta: # Wewnętrzna klasa Meta służy do przekazania ustawień konfiguracyjnych dla tego serializatora.
        model = Task # Wskazujemy wprost, że ten serializator ma przetwarzać dane pochodzące z modelu Task.
        fields = '__all__' # Specjalny parametr mówiący DRF, aby uwzględnił absolutnie wszystkie kolumny z tabeli Task w odpowiedzi JSON.