# Projekt Programowania Zespołowego

## Technologie
| Dział projektu | Technologia | Odpowiedzialni |
| --------  | ------- | ------- |
| Backend   |  Django | Harrypotter, Dinolek |
| Frontend  |  React  | xmedo1, dieselP273 |
| FullStack |  -      | lukasz-malec |
| DevOps    |  -      | j-markiewicz |
| Tester    |  -      | 26d4 |


## Informacje o Rolach w projekcie

Product Owner:

- tworzy projekty
- dodaje ludzi
- zarządza backlogiem
- może wybrać Scrum Mastera

Scrum Master:

- zarządza sprintami
- tworzy / przypisuje zadania
- pilnuje pracy zespołu

Programmer:

- widzi swój projekt
- widzi swoje zadania
- widzi członków zespołu


## Testy
### Backend
#### Wprowadzenie

Testy Backendu są realizowane przez mechanizmy wbudowane w Django.

Podstawą uruchamiania testów jest komenda
```
python3 manage.py test
```
uruchamiana wewnątrz katalogu `backend/`.
Wyszukuje on testy w plikach o nazwach zaczynających się od `test`.

#### Ustawienia

Powyższa komenda uruchamia *wszystkie* testy. Zakres testowania można
zawęzić do pliku z testami, klasy (TestCase), lub pojedynczego testu:
```
python3 manage.py test scrum.tests.{plik}.{klasa}.{test}
```
Przykłady:
```
# Jeden plik
python3 manage.py test scrum.tests.test_auth
# Jedna klasa
python3 manage.py test scrum.tests.test_auth.ApiAuthTestCase
# Jeden test
python3 manage.py test scrum.tests.test_auth.ApiAuthTestCase.test_me
```
<small>Możliwe też jest zawężanie do modułu i pakietu, ale w tym
projekcie jest tylko po jednym.</small>

Wybrane opcje:

- `--failfast`: Pierwszy niezaliczony test zatrzymuje testowanie
- `--shuffle [ziarno]`: Losowa kolejność wykonywania testów (opcjonalnie
  wedle podanego ziarna)
- `-r`, `--reverse`: Odwrotna kolejność wykonywania testów
- `--parallel [N]`: Uruchamianie testów równolegle na N procesorach (lub
  na wszystkich dostępnych, gdy N niepodane)
- `--durations N`: Wypisanie czasów trwania N najwolniejszych testów,
  wszystkich przy N=0
- `--verbosity N`, `-v N`: Poziom szczegółowości wypisywanych
  komunikatów: 0 = nic, 1 = domyślny, 2 = szczegółowy,
  3 = bardziej szczegółowy

#### Komunikaty

Testerka wypisuje informacje o przygotowaniach,
przebiegu testów oraz podsumowanie.

Komunikaty z przebiegu testów zwykle wyglądają w ten sposób:
```
Found 35 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...................................
----------------------------------------------------------------------
Ran 35 tests in 3.282s

OK
Destroying test database for alias 'default'...
```

W przypadku, gdy część testów nie zostanie zaliczona, przebieg testów
wskaże niepowodzenia i zostanie wypisana lokalizacja ich wystąpienia:
```
Found 35 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.....F.......F.....................
======================================================================
FAIL: test_me (scrum.tests.test_auth.ApiAuthTestCase.test_me)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "(...)/projekt/backend/scrum/tests/test_auth.py", line 57, in test_me
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

======================================================================
FAIL: test_get_list (scrum.tests.test_projects.ApiProjectListTestCase.test_get_list)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "(...)/projekt/backend/scrum/tests/test_projects.py", line 116, in test_get_list
    self.assertEqual(response.status_code, 200)
AssertionError: 403 != 200

----------------------------------------------------------------------
Ran 35 tests in 3.031s

FAILED (failures=2)
Destroying test database for alias 'default'...
```
<small>Ścieżki w powyższym przykładzie są przycięte</small>

#### Więcej szczegółów

- https://docs.djangoproject.com/en/6.0/topics/testing/overview/#running-tests
- https://docs.djangoproject.com/en/6.0/ref/django-admin/#test