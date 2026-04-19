"""
Ustawienia Django dla projektu core. # Docstring informujący, że to plik ustawień dla projektu 'core'.

Wygenerowane przez 'django-admin startproject' przy użyciu Django 5.2.12. # Informacja o wersji Django i poleceniu użytym do wygenerowania pliku.

Aby uzyskać więcej informacji o tym pliku, zobacz # Link do oficjalnej dokumentacji dotyczącej struktury ustawień.
https://docs.djangoproject.com/en/5.2/topics/settings/

Aby zobaczyć pełną listę ustawień i ich wartości, zobacz # Link do pełnej listy dostępnych zmiennych konfiguracyjnych w Django.
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

from pathlib import Path 

# Buduj ścieżki wewnątrz projektu w ten sposób: BASE_DIR / 'katalog_podrzędny'.
BASE_DIR = Path(__file__).resolve().parent.parent # Oblicza i zapisuje absolutną ścieżkę do głównego folderu Twojego projektu (tam, gdzie znajduje się manage.py).



SECRET_KEY = 'django-insecure-##bw^k*ul)p(x14z1(9r1%@qm8s&#5%q-722f*%9x6l)98l0wf' # Unikalny, tajny klucz szyfrujący Django. Używany do hashowania sesji, tokenów i haseł. Nie udostępniaj go!

# OSTRZEŻENIE BEZPIECZEŃSTWA: nie uruchamiaj z włączonym debugowaniem na produkcji!
DEBUG = True # Tryb deweloperski. Jeśli jest True, przeglądarka wyświetli szczegółowe błędy kodu. Na serwerze produkcyjnym MUSI być False.

ALLOWED_HOSTS = [] # Lista domen lub adresów IP, pod którymi ten projekt może być uruchomiony. Pusta lista oznacza "tylko localhost".


# Definicja aplikacji

INSTALLED_APPS = [ # Główna lista wszystkich paczek, modułów i aplikacji wchodzących w skład tego projektu.
    'django.contrib.admin', # Wbudowany interfejs panelu administratora bazy danych Django.
    'django.contrib.auth', # Wbudowany system zarządzania użytkownikami, grupami i uprawnieniami.
    'django.contrib.contenttypes', # Wbudowany framework pozwalający na tworzenie generycznych relacji między modelami w bazie.
    'django.contrib.sessions', # Wbudowany mechanizm przechowywania danych sesyjnych użytkowników w bazie lub pamięci.
    'django.contrib.messages', # Wbudowany system tzw. flash messages (komunikatów wyskakujących po akcji, np. "Zapisano zmiany").
    'django.contrib.staticfiles', # Wbudowana aplikacja do serwowania plików statycznych (np. CSS, JavaScript, logo).
    'rest_framework', # Zainstalowana zewnętrzna biblioteka Django REST Framework do budowy API.
    'scrum', # Twoja główna aplikacja zawierająca logikę biznesową projektu, modele i widoki.
]

MIDDLEWARE = [ # Warstwy pośredniczące. To kod wykonywany przy KAŻDYM wejściu użytkownika na stronę i przy KAŻDEJ odpowiedzi serwera.
    'django.middleware.security.SecurityMiddleware', # Zapewnia podstawowe zabezpieczenia (np. wymuszanie HTTPS, nagłówki bezpieczeństwa przeglądarki).
    'django.contrib.sessions.middleware.SessionMiddleware', # Zarządza sesjami, identyfikując użytkownika między różnymi kliknięciami na stronie.
    'django.middleware.common.CommonMiddleware', # Dodaje drobne udogodnienia, np. automatycznie dopisuje ukośnik (/) na końcu adresów URL.
    'django.middleware.csrf.CsrfViewMiddleware', # Zabezpiecza formularze metod POST/PUT przed atakami typu Cross-Site Request Forgery.
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Jeśli w sesji jest zalogowany użytkownik, ten moduł dołącza go jako obiekt request.user do żądania.
    'django.contrib.messages.middleware.MessageMiddleware', # Zarządza wyświetlaniem sesyjnych komunikatów.
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Blokuje możliwość ładowania Twojej strony wewnątrz <iframe> na innych stronach (zabezpieczenie przed clickjackingiem).
]

ROOT_URLCONF = 'core.urls' # Mówi Django, w którym pliku znajduje się główny punkt startowy z trasami URL całego projektu.

TEMPLATES = [ # Konfiguracja systemu renderowania szablonów HTML. W projektach opartych w 100% o React+API używa się go rzadziej (głównie do panelu admina).
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', # Ustawia domyślny silnik renderowania HTML wbudowany w Django.
        'DIRS': [], # Lista opcjonalnych, globalnych folderów z szablonami (tutaj pusta).
        'APP_DIRS': True, # Informuje Django, że ma automatycznie zaglądać do folderu 'templates' wewnątrz każdej aplikacji (np. 'scrum/templates/').
        'OPTIONS': { # Ustawienia dodatkowe dla wybranego silnika renderowania.
            'context_processors': [ # Funkcje, które automatycznie "wstrzykują" zmienne globalne do każdego pliku HTML.
                'django.template.context_processors.request', # Pozwala na dostęp do obiektu 'request' (np. URL, metody GET) w szablonie HTML.
                'django.contrib.auth.context_processors.auth', # Pozwala na dostęp do obiektu {{ user }} (np. nazwy zalogowanego użytkownika) w HTML.
                'django.contrib.messages.context_processors.messages', # Pozwala na iterowanie po powiadomieniach (komunikatach) i wyświetlanie ich na stronie.
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application' # Wskazuje drogę do obiektu aplikacji WSGI (standard używany na serwerach produkcyjnych do komunikacji Pythona z serwerem www).


# Baza danych
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = { # Słownik konfiguracyjny wszystkich połączonych baz danych.
    'default': { # Ustawienia dla głównej bazy danych projektu (najczęściej jest tylko jedna).
        'ENGINE': 'django.db.backends.sqlite3', # Używamy lekkiej, bezserwerowej bazy SQLite, z którą Django domyślnie startuje.
        'NAME': BASE_DIR / 'db.sqlite3', # Określa, że plik z bazą danych będzie się nazywał db.sqlite3 i znajdzie się w głównym folderze projektu (BASE_DIR).
    }
}


# Walidacja hasła
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [ # Lista wtyczek, które weryfikują jakość i siłę hasła podczas rejestracji lub zmiany hasła.
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', # Blokuje hasła zbyt podobne do np. imienia lub loginu użytkownika.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', # Blokuje hasła, które są zbyt krótkie (domyślnie mniej niż 8 znaków).
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', # Odrzuca hasła znajdujące się na "czarnej liście" tysięcy najpopularniejszych, słabych haseł.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', # Uniemożliwia ustawienie hasła składającego się wyłącznie z cyfr (np. '12345678').
    },
]


# Umiędzynarodowienie (Internacjonalizacja)
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us' # Domyślny język aplikacji (amerykański angielski). Gdy zmienisz na 'pl', wbudowane błędy i panel admina będą po polsku.

TIME_ZONE = 'UTC' # Domyślna strefa czasowa. Wszystkie daty w bazie danych zapisywane są według niej. Dla Polski zmienia się ją na 'Europe/Warsaw'.

USE_I18N = True # Skrót od Internationalization (I, 18 liter, N). Włącza wbudowany system tłumaczeń wielojęzycznych.

USE_TZ = True # Włącza obsługę stref czasowych. Dzięki temu w bazie zapisujemy uniwersalny czas UTC, a wyświetlamy czas lokalny.


# Pliki statyczne (CSS, JavaScript, Obrazki)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/' # Prefix ścieżki w przeglądarce, z którego serwowane są pliki (np. localhost:8000/static/style.css).

# Domyślny typ pola klucza głównego
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Od Django 3.2 ustala, że id-ki w bazach danych domyślnie używają dużych liczb całkowitych (Big Integer), by pomieścić więcej wierszy.

# Django REST Framework

REST_FRAMEWORK = { # Główny słownik z ustawieniami dla naszego biblioteki budującej API.
    'DEFAULT_AUTHENTICATION_CLASSES': ( # Lista mówiąca API, w jaki sposób ma sprawdzać "kim jest ten użytkownik?".
        'rest_framework_simplejwt.authentication.JWTAuthentication', # Informujemy DRF, że użtkownik przedstawi się wysyłając token JWT (SimpleJWT) w nagłówku żądania.
    ),
    'DEFAULT_PERMISSION_CLASSES': ( # Lista mówiąca API, jakie są globalne, domyślne zasady wpuszczania do endpointów.
        'rest_framework.permissions.IsAuthenticated', # Wymagamy, aby z każdego adresu API korzystały TYLKO osoby z poprawnym i aktualnym tokenem (zalogowane).
    ),
}
