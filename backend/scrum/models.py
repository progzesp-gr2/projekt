from django.db import models 
from django.conf import settings 
from django.utils.translation import gettext_lazy as _ 

class Project(models.Model): # Definiujemy tabelę w bazie danych o nazwie "Project". Dziedziczy z models.Model.
    """
    Represents a main workspace or product being developed. # Krótki opis klasy (Docstring): Reprezentuje główny projekt.
    A project contains multiple sprints and tasks. # Projekt zawiera wiele sprintów i zadań.
    """
    name = models.CharField( 
        max_length=255, 
        help_text="The name of the project" 
    )
    key = models.CharField( # Definiujemy kolumnę 'key' (krótki skrót literowy projektu, np. "PROJ").
        max_length=10, 
        unique=True, # Zabezpieczenie na poziomie bazy: w całym systemie nie mogą istnieć dwa projekty z tym samym kluczem.
        help_text="A short, unique identifier for the project" # Tekst pomocniczy.
    )
    description = models.TextField( # Definiujemy kolumnę 'description' jako długie pole tekstowe bez limitu znaków.
        blank=True, # Parametr blank=True oznacza, że to pole nie jest obowiązkowe do wypełnienia w formularzach (może być puste).
        help_text="Detailed description of the project goals and scope" # Tekst pomocniczy.
    )
    owner = models.ForeignKey( # Definiujemy kolumnę 'owner' jako klucz obcy, tworząc relację (jeden użytkownik może mieć wiele projektów).
        settings.AUTH_USER_MODEL, # Wskazujemy na systemowy model użytkownika z pliku settings.py. To lepsza praktyka niż bezpośredni import User.
        on_delete=models.SET_NULL, # Jeśli usuniemy użytkownika-właściciela z bazy, nie usuwamy projektu, tylko ustawiamy pole owner na NULL (puste).
        null=True, # Parametr null=True pozwala bazie danych zapisać w tej kolumnie wartość NULL (gdy on_delete=SET_NULL zadziała).
        related_name='owned_projects', # Nazwa relacji odwrotnej: ułatwia pobranie projektów użytkownika (np. uzytkownik.owned_projects.all()).
        help_text="The user who created or manages the project" # Tekst pomocniczy.
    )
    created_at = models.DateTimeField(auto_now_add=True) # Automatycznie zapisuje dokładną datę i czas w momencie pierwszego utworzenia (dodania) projektu do bazy.
    updated_at = models.DateTimeField(auto_now=True) # Automatycznie aktualizuje datę i czas przy każdej edycji i zapisie (zmianie) danych tego projektu.

    class Meta: # Wewnętrzna klasa konfiguracyjna Meta dostarcza metadanych o samym modelu.
        ordering = ['-created_at'] 
        verbose_name = "Project" 
        verbose_name_plural = "Projects" 

    def __str__(self):
        return f"{self.key} - {self.name}" 


class Sprint(models.Model): # Definiujemy tabelę "Sprint".
    """
    Represents a iteration (usually 1-4 weeks) during which a specific set of # Docstring.
    tasks is completed. # Docstring c.d.
    """
    class SprintStatus(models.TextChoices): # Wewnętrzna klasa dziedzicząca po TextChoices, to elegancki sposób Django na zdefiniowanie twardej listy opcji (tzw. enumeracji).
        PLANNED = 'PLANNED', _('Planned') # Definiuje status "Zaplanowany". Wartość z lewej to kod zapisywany do bazy, z prawej - tłumaczalny tekst widoczny dla użytkownika.
        ACTIVE = 'ACTIVE', _('Active') 
        COMPLETED = 'COMPLETED', _('Completed')

    name = models.CharField( # Pole przechowujące nazwę sprintu.
        max_length=100, 
        help_text="Name of the sprint"
    )
    project = models.ForeignKey( # Klucz obcy wiążący dany sprint z konkretnym projektem.
        Project, # Wskazujemy model Project, zdefiniowany wyżej w tym pliku.
        on_delete=models.CASCADE, # ZASADA CASCADE: Jeśli projekt zostanie usunięty z bazy, to WSZYSTKIE przypisane do niego sprinty również zostaną z automatu usunięte.
        related_name='sprints', # Nazwa relacji odwrotnej (np. zrobisz projekt.sprints.all() by pobrać listę sprintów w tym projekcie).
        help_text="The project this sprint belongs to" 
    )
    goal = models.TextField( # Pole tekstowe na opisanie głównego celu danego sprintu.
        blank=True,
        help_text="The main objective to be achieved during this sprint" 
    )
    start_date = models.DateField( # Pole na datę rozpoczęcia sprintu (tylko dzień/miesiąc/rok, bez godzin).
        null=True, 
        blank=True, # Formularze akceptują puste pole.
        help_text="The date when the sprint officially starts" 
    )
    end_date = models.DateField( # Pole na datę planowanego zakończenia sprintu.
        null=True, 
        blank=True, # Formularz akceptuje pustkę.
        help_text="The date when the sprint is scheduled to end" 
    )
    status = models.CharField( # Pole tekstowe przechowujące status sprintu.
        max_length=20, 
        choices=SprintStatus.choices, # Ogranicza możliwe wartości TYLKO do tych trzech, które zdefiniowaliśmy wyżej w TextChoices.
        default=SprintStatus.PLANNED, 
        help_text="Current lifecycle state of the sprint"
    )

    class Meta: # Klasa konfiguracyjna dla modelu Sprint.
        ordering = ['start_date', 'name'] # Domyślnie sortuje listę sprintów najpierw według daty startu, a następnie (przy takich samych datach) alfabetycznie po nazwie.
        verbose_name = "Sprint" 
        verbose_name_plural = "Sprints" 

    def __str__(self): # Metoda reprezentacji tekstowej.
        return f"{self.name} ({self.project.key})" # Zwraca np. "Sprint 1 (PROJ)".


class Task(models.Model): # Definiujemy tabelę "Task" (Zadanie).
    """
    Represents a single unit of work in the Scrum. # Docstring.
    It can be a user story, a bug, or a general task. # Docstring c.d.
    """
    class TaskType(models.TextChoices): # Lista do wyboru dla TYPU zadania.
        STORY = 'STORY', _('User Story')
        TASK = 'TASK', _('Task')
        BUG = 'BUG', _('Bug') 

    class TaskStatus(models.TextChoices): # Lista do wyboru dla STATUSU zadania (bardzo ważne dla tablicy Kanban z Twojej specyfikacji).
        BACKLOG = 'BACKLOG', _('Backlog')
        TODO = 'TODO', _('To do')
        IN_PROGRESS = 'IN_PROGRESS', _('In progress') 
        IN_REVIEW = 'IN_REVIEW', _('In review') 
        DONE = 'DONE', _('Done') 

    class TaskPriority(models.TextChoices): # Lista do wyboru dla PRIORYTETU zadania[cite: 18].
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium') 
        HIGH = 'HIGH', _('High')
        CRITICAL = 'CRITICAL', _('Critical') 

    title = models.CharField( # Tytuł pojedynczego zadania.
        max_length=255, 
        help_text="A concise summary of the task" 
    )
    description = models.TextField( # Szczegółowy opis, kryteria akceptacji itp.
        blank=True, 
        help_text="Detailed description, acceptance criteria or steps to reproduce (for bugs)." 
    )
    task_type = models.CharField( # Pole przypisujące zadaniu jeden z typów.
        max_length=10, 
        choices=TaskType.choices, # Pobieramy wybór z klasy TaskType zdefiniowanej wyżej
        default=TaskType.STORY, # Domyślny typ to User Story.
        help_text="The nature of the work item" # Tekst pomocniczy.
    )
    status = models.CharField( # Pole przypisujące zadaniu status Kanban.
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.BACKLOG, 
        help_text="Current position in workflow"
    )
    priority = models.CharField( # Pole priorytetu zadania.
        max_length=10,
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM, 
        help_text="Importance and urgency of the task"
    )
    story_points = models.PositiveIntegerField( # Pole na punkty wyceny zadania (dodatnia liczba całkowita).
        null=True, 
        blank=True,
        help_text="An estimate of the effort required to implement this task" 
    )

    # Relacje (Klucze obce)
    project = models.ForeignKey( # Powiązanie zadania z głównym projektem.
        Project, # Model docelowy.
        on_delete=models.CASCADE, # ZASADA CASCADE: usunięcie projektu usunie również wszystkie jego zadania
        related_name='tasks', # Odwrotna ścieżka (projekt.tasks.all()).
        help_text="The project to which this task belongs"
    )
    sprint = models.ForeignKey( # Opcjonalne powiązanie zadania z konkretnym iteracyjnym sprintem.
        Sprint,
        on_delete=models.SET_NULL, # Jeśli usuniemy z bazy sprint, to zadanie ma PRZETRWAĆ, tylko to powiązanie stanie się puste.
        null=True,
        blank=True, # Zadanie nie musi od razu należeć do sprintu (może leżeć w Backlogu)[cite: 9, 10, 16].
        related_name='tasks', # Odwrotna ścieżka (sprint.tasks.all()).
        help_text="The sprint during which this task is planned to be executed"
    )
    assignee = models.ForeignKey( # Powiązanie z użytkownikiem, KTÓRY WYKONUJE TO ZADANIE (Programista).
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_tasks',
        help_text="The user responsible for completing the task" 
    )
    reporter = models.ForeignKey( # Powiązanie z użytkownikiem, KTÓRY ZGŁOSIŁ ZADANIE (lub błąd).
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='reported_tasks', 
        help_text="The user who created or reported this task" 
    )

    # Pola czasowe
    created_at = models.DateTimeField(auto_now_add=True) # Zapisuje moment, w którym zadanie weszło do bazy
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta: # Konfiguracja modelu.
        ordering = ['-created_at'] # Sortuj zadania od najnowszych.
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self): # Reprezentacja tekstowa zadania.
        return f"[{self.project.key}-{self.pk}] {self.title}" # Zwraca czytelną dla człowieka nazwę jak w Jirze, np. "[PROJ-15] Naprawić panel logowania". self.pk to unikalny identyfikator (ID) w bazie.
