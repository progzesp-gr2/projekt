from rest_framework import serializers 
from scrum.models import Task 

class TaskSerializer(serializers.ModelSerializer): # Tworzymy klasę serializatora dziedziczącą po ModelSerializer, która zautomatyzuje konwersję na JSON.
    class Meta: # Wewnętrzna klasa Meta służy do przekazania ustawień konfiguracyjnych dla tego serializatora.
        model = Task # Wskazujemy wprost, że ten serializator ma przetwarzać dane pochodzące z modelu Task.
        fields = '__all__' # Specjalny parametr mówiący DRF, aby uwzględnił absolutnie wszystkie kolumny z tabeli Task w odpowiedzi JSON.
