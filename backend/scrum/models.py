from django.db import models # Importujemy wbudowany moduł Django do definiowania struktury bazy danych.
from django.conf import settings # Importujemy ustawienia projektu, aby bezpiecznie odwołać się do modelu użytkownika (AUTH_USER_MODEL).
from django.utils.translation import gettext_lazy as _ # Importujemy funkcję do tłumaczeń (oznaczoną zazwyczaj jako '_'), aby teksty mogły być wielojęzyczne.


class Project(models.Model): # Definiujemy tabelę w bazie danych o nazwie "Project". Dziedziczy z models.Model.
    """
    Represents a main workspace or product being developed. # Krótki opis klasy (Docstring): Reprezentuje główny projekt.
    A project contains multiple sprints and tasks. # Projekt zawiera wiele sprintów i zadań.
    """
    name = models.CharField( # Definiujemy kolumnę 'name' jako krótkie pole tekstowe (varchar w SQL).
        max_length=255, # Maksymalna długość nazwy to 255 znaków.
        help_text="The name of the project" # Tekst pomocniczy, który wyświetli się w formularzach (np. w panelu admina).
    )
    key = models.CharField( # Definiujemy kolumnę 'key' (krótki skrót literowy projektu, np. "PROJ").
        max_length=10, # Maksymalna długość to 10 znaków.
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
        ordering = ['-created_at'] # Określa domyślne sortowanie przy pobieraniu list. Znak '-' oznacza malejąco, więc od najnowszych do najstarszych.
        verbose_name = "Project" # Czytelna dla człowieka nazwa pojedynczego obiektu w liczbie pojedynczej (używana w adminie).
        verbose_name_plural = "Projects" # Czytelna dla człowieka nazwa w liczbie mnogiej.

    def __str__(self): # Wbudowana metoda Pythona decydująca o reprezentacji tekstowej obiektu.
        return f"{self.key} - {self.name}" # Kiedy "wydrukujesz" obiekt projektu, wyświetli się np. "PROJ - Aplikacja webowa".


class Sprint(models.Model): # Definiujemy tabelę "Sprint".
    """
    Represents a iteration (usually 1-4 weeks) during which a specific set of # Docstring.
    tasks is completed. # Docstring c.d.
    """
    class SprintStatus(models.TextChoices): # Wewnętrzna klasa dziedzicząca po TextChoices, to elegancki sposób Django na zdefiniowanie twardej listy opcji (tzw. enumeracji).
        PLANNED = 'PLANNED', _('Planned') # Definiuje status "Zaplanowany". Wartość z lewej to kod zapisywany do bazy, z prawej - tłumaczalny tekst widoczny dla użytkownika.
        ACTIVE = 'ACTIVE', _('Active') # Definiuje status "Aktywny".
        COMPLETED = 'COMPLETED', _('Completed') # Definiuje status "Zakończony".

    name = models.CharField( # Pole przechowujące nazwę sprintu.
        max_length=100, # Maksymalnie 100 znaków.
        help_text="Name of the sprint" # Tekst pomocniczy.
    )
    project = models.ForeignKey( # Klucz obcy wiążący dany sprint z konkretnym projektem.
        Project, # Wskazujemy model Project, zdefiniowany wyżej w tym pliku.
        on_delete=models.CASCADE, # ZASADA CASCADE: Jeśli projekt zostanie usunięty z bazy, to WSZYSTKIE przypisane do niego sprinty również zostaną z automatu usunięte.
        related_name='sprints', # Nazwa relacji odwrotnej (np. zrobisz projekt.sprints.all() by pobrać listę sprintów w tym projekcie).
        help_text="The project this sprint belongs to" # Tekst pomocniczy.
    )
    goal = models.TextField( # Pole tekstowe na opisanie głównego celu danego sprintu.
        blank=True, # Pole może pozostać puste w formularzu.
        help_text="The main objective to be achieved during this sprint" # Tekst pomocniczy.
    )
    start_date = models.DateField( # Pole na datę rozpoczęcia sprintu (tylko dzień/miesiąc/rok, bez godzin).
        null=True, # Baza danych akceptuje wartość NULL (puste).
        blank=True, # Formularze akceptują puste pole.
        help_text="The date when the sprint officially starts" # Tekst pomocniczy.
    )
    end_date = models.DateField( # Pole na datę planowanego zakończenia sprintu.
        null=True, # Baza akceptuje NULL.
        blank=True, # Formularz akceptuje pustkę.
        help_text="The date when the sprint is scheduled to end" # Tekst pomocniczy.
    )
    status = models.CharField( # Pole tekstowe przechowujące status sprintu.
        max_length=20, # Max 20 znaków wystarczy na zapamiętanie słowa ze słownika SprintStatus.
        choices=SprintStatus.choices, # Ogranicza możliwe wartości TYLKO do tych trzech, które zdefiniowaliśmy wyżej w TextChoices.
        default=SprintStatus.PLANNED, # Jeśli przy tworzeniu nie podamy statusu, domyślnie będzie "Zaplanowany".
        help_text="Current lifecycle state of the sprint" # Tekst pomocniczy.
    )

    class Meta: # Klasa konfiguracyjna dla modelu Sprint.
        ordering = ['start_date', 'name'] # Domyślnie sortuje listę sprintów najpierw według daty startu, a następnie (przy takich samych datach) alfabetycznie po nazwie.
        verbose_name = "Sprint" # Nazwa czytelna w l. poj.
        verbose_name_plural = "Sprints" # Nazwa czytelna w l. mn.

    def __str__(self): # Metoda reprezentacji tekstowej.
        return f"{self.name} ({self.project.key})" # Zwraca np. "Sprint 1 (PROJ)".


class Task(models.Model): # Definiujemy tabelę "Task" (Zadanie).
    """
    Represents a single unit of work in the Scrum. # Docstring.
    It can be a user story, a bug, or a general task. # Docstring c.d.
    """
    class TaskType(models.TextChoices): # Lista do wyboru dla TYPU zadania.
        STORY = 'STORY', _('User Story') # Historia użytkownika (wymaganie biznesowe).
        TASK = 'TASK', _('Task') # Zwykłe zadanie.
        BUG = 'BUG', _('Bug') # Błąd do naprawy.

    class TaskStatus(models.TextChoices): # Lista do wyboru dla STATUSU zadania (bardzo ważne dla tablicy Kanban z Twojej specyfikacji).
        BACKLOG = 'BACKLOG', _('Backlog') # Zadanie leży na kupce i czeka.
        TODO = 'TODO', _('To do') # Do zrobienia w obecnym sprincie.
        IN_PROGRESS = 'IN_PROGRESS', _('In progress') # Ktoś nad tym właśnie pracuje.
        IN_REVIEW = 'IN_REVIEW', _('In review') # Oczekuje na weryfikację kodu (Code Review).
        DONE = 'DONE', _('Done') # Zadanie wykonane[cite: 23].

    class TaskPriority(models.TextChoices): # Lista do wyboru dla PRIORYTETU zadania[cite: 18].
        LOW = 'LOW', _('Low') # Niski.
        MEDIUM = 'MEDIUM', _('Medium') # Średni.
        HIGH = 'HIGH', _('High') # Wysoki.
        CRITICAL = 'CRITICAL', _('Critical') # Krytyczny[cite: 18].

    title = models.CharField( # Tytuł pojedynczego zadania.
        max_length=255, # Max 255 znaków.
        help_text="A concise summary of the task" # Tekst pomocniczy.
    )
    description = models.TextField( # Szczegółowy opis, kryteria akceptacji itp.
        blank=True, # Może być puste.
        help_text="Detailed description, acceptance criteria or steps to reproduce (for bugs)." # Tekst pomocniczy.
    )
    task_type = models.CharField( # Pole przypisujące zadaniu jeden z typów.
        max_length=10, 
        choices=TaskType.choices, # Pobieramy wybór z klasy TaskType zdefiniowanej wyżej[cite: 18].
        default=TaskType.STORY, # Domyślny typ to User Story.
        help_text="The nature of the work item" # Tekst pomocniczy.
    )
    status = models.CharField( # Pole przypisujące zadaniu status Kanban.
        max_length=20,
        choices=TaskStatus.choices, # Ogranicza wybór do puli ze zdefiniowanego wyżej TaskStatus.
        default=TaskStatus.BACKLOG, # Nowe zadania trafiają domyślnie na stertę (Backlog)[cite: 1, 9].
        help_text="Current position in workflow" # Tekst pomocniczy.
    )
    priority = models.CharField( # Pole priorytetu zadania.
        max_length=10,
        choices=TaskPriority.choices, # Ogranicza wybór.
        default=TaskPriority.MEDIUM, # Domyślnie priorytet jest średni.
        help_text="Importance and urgency of the task" # Tekst pomocniczy.
    )
    story_points = models.PositiveIntegerField( # Pole na punkty wyceny zadania (dodatnia liczba całkowita).
        null=True, # Baza akceptuje puste wartości.
        blank=True, # Formularz akceptuje puste wartości (zadanie może być niewycenione).
        help_text="An estimate of the effort required to implement this task" # Tekst pomocniczy.
    )

    # Relacje (Klucze obce)
    project = models.ForeignKey( # Powiązanie zadania z głównym projektem.
        Project, # Model docelowy.
        on_delete=models.CASCADE, # ZASADA CASCADE: usunięcie projektu usunie również wszystkie jego zadania[cite: 35].
        related_name='tasks', # Odwrotna ścieżka (projekt.tasks.all()).
        help_text="The project to which this task belongs" # Tekst pomocniczy.
    )
    sprint = models.ForeignKey( # Opcjonalne powiązanie zadania z konkretnym iteracyjnym sprintem.
        Sprint,
        on_delete=models.SET_NULL, # Jeśli usuniemy z bazy sprint, to zadanie ma PRZETRWAĆ, tylko to powiązanie stanie się puste.
        null=True, # Baza zezwala na puste pole.
        blank=True, # Zadanie nie musi od razu należeć do sprintu (może leżeć w Backlogu)[cite: 9, 10, 16].
        related_name='tasks', # Odwrotna ścieżka (sprint.tasks.all()).
        help_text="The sprint during which this task is planned to be executed" # Tekst pomocniczy.
    )
    assignee = models.ForeignKey( # Powiązanie z użytkownikiem, KTÓRY WYKONUJE TO ZADANIE (Programista).
        settings.AUTH_USER_MODEL, # Podpinamy wbudowany model użytkowników Django[cite: 38].
        on_delete=models.SET_NULL, # Jeśli pracownik odejdzie z firmy (usuną mu konto), zadanie zostanie, tylko nie będzie miało wykonawcy[cite: 38].
        null=True, # Baza zezwala na puste pole[cite: 38].
        blank=True, # Zadanie może być utworzone, ale jeszcze komuś nieprzypisane.
        related_name='assigned_tasks', # Odwrotna ścieżka pobierająca zadania przypisane do danego pracownika (user.assigned_tasks.all()).
        help_text="The user responsible for completing the task" # Tekst pomocniczy.
    )
    reporter = models.ForeignKey( # Powiązanie z użytkownikiem, KTÓRY ZGŁOSIŁ ZADANIE (lub błąd).
        settings.AUTH_USER_MODEL, # Podpinamy wbudowany model użytkowników Django[cite: 38].
        on_delete=models.SET_NULL, # Jeśli zgłaszający zostanie usunięty, zadanie zostaje[cite: 38].
        null=True, # Zezwalamy na puste pole[cite: 38].
        related_name='reported_tasks', # Odwrotna ścieżka dla zadań zgłoszonych przez daną osobę (user.reported_tasks.all()).
        help_text="The user who created or reported this task" # Tekst pomocniczy.
    )

    # Pola czasowe
    created_at = models.DateTimeField(auto_now_add=True) # Zapisuje moment, w którym zadanie weszło do bazy[cite: 38].
    updated_at = models.DateTimeField(auto_now=True) # Aktualizuje się przy każdym przesunięciu zadania lub zmianie opisu[cite: 38].

    class Meta: # Konfiguracja modelu.
        ordering = ['-created_at'] # Sortuj zadania od najnowszych.
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self): # Reprezentacja tekstowa zadania.
        return f"[{self.project.key}-{self.pk}] {self.title}" # Zwraca czytelną dla człowieka nazwę jak w Jirze, np. "[PROJ-15] Naprawić panel logowania". self.pk to unikalny identyfikator (ID) w bazie.