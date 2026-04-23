from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


# to bedzie trzeba zmienić i przechowywać w env.
SECRET_KEY = 'django-insecure-##bw^k*ul)p(x14z1(9r1%@qm8s&#5%q-722f*%9x6l)98l0wf' 


DEBUG = True 

ALLOWED_HOSTS = [] # tylko localhos".



INSTALLED_APPS = [ 
    'django.contrib.admin', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'rest_framework',
    'scrum', 
    'rest_framework_simplejwt',     # potrzebne dla json token
     "corsheaders",                 # cors
]


# Warstwy pośredniczące. To kod wykonywany przy KAŻDYM wejściu użytkownika na stronę i przy KAŻDEJ odpowiedzi serwera.
MIDDLEWARE = [ 
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware', #
    'django.middleware.common.CommonMiddleware', 
    'django.middleware.csrf.CsrfViewMiddleware', 
    'django.contrib.auth.middleware.AuthenticationMiddleware', 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls' 


 # Konfiguracja renderowania szablonów HTML. - my mamy react, nie uzywamy
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates', 
        'DIRS': [], 
        'APP_DIRS': True, 
        'OPTIONS': {
            'context_processors': [ 
                'django.template.context_processors.request', 
                'django.contrib.auth.context_processors.auth', 
                'django.contrib.messages.context_processors.messages', 
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application' 




DATABASES = { 
    'default': { 
        'ENGINE': 'django.db.backends.sqlite3', 
        'NAME': BASE_DIR / 'db.sqlite3', 
    }
}



AUTH_PASSWORD_VALIDATORS = [ 
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', 
        # Blokuje hasła zbyt podobne do np. imienia lub loginu użytkownika.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 
        # Blokuje hasła, które są zbyt krótkie (domyślnie mniej niż 8 znaków).
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
          # Odrzuca hasła znajdujące się na "czarnej liście" tysięcy najpopularniejszych, słabych haseł.
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
          # Uniemożliwia ustawienie hasła składającego się wyłącznie z cyfr (np. '12345678').
    },
]




LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC' 

USE_I18N = True 

USE_TZ = True 


#

STATIC_URL = 'static/' # Prefix ścieżki w przeglądarce, z którego serwowane są pliki (np. localhost:8000/static/style.css).

#

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 
# Django REST Framework

REST_FRAMEWORK = { # Główny słownik z ustawieniami dla naszego biblioteki budującej API.
    'DEFAULT_AUTHENTICATION_CLASSES': ( # Lista mówiąca API, w jaki sposób ma sprawdzać "kim jest ten użytkownik?".
        'rest_framework_simplejwt.authentication.JWTAuthentication', # Informujemy DRF, że użtkownik przedstawi się wysyłając token JWT (SimpleJWT) w nagłówku żądania.
    ),
    'DEFAULT_PERMISSION_CLASSES': ( # Lista mówiąca API, jakie są globalne, domyślne zasady wpuszczania do endpointów.
        'rest_framework.permissions.IsAuthenticated', # Wymagamy, aby z każdego adresu API korzystały TYLKO osoby z poprawnym i aktualnym tokenem (zalogowane).
    ),
}


CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]