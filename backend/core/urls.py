"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin # Importujemy wbudowany panel administracyjny Django.
from django.urls import include, path # Importujemy 'include' do podpinania innych plików urls.py oraz 'path' do definiowania tras.
from rest_framework_simplejwt.views import TokenRefreshView # Importujemy gotowy widok do odświeżania tokenów JWT.

urlpatterns = [ # Lista wzorców URL, które Django sprawdza od góry do dołu.
    path('admin/', admin.site.urls), # Trasa do panelu administratora (np. localhost:8000/admin/).

    # Endpoint do odświeżania tokena JWT. 
    # React będzie go potrzebował, gdy główny token dostępowy wygaśnie.
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # Definiujemy adres do odświeżania tokenów.

    # Podpięcie wszystkich tras z aplikacji 'scrum'.
    # Ponieważ używamy pustego stringa '', Django "dokleja" trasy ze 'scrum/urls.py' bezpośrednio do adresu głównego.
    path('api/', include('scrum.urls')), # DOBRZE # Przekierowanie ruchu do pliku urls.py wewnątrz aplikacji scrum.
]