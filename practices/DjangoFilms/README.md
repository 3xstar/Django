# DjangoFilms

Учебный каталог фильмов DjangoFilms с режиссёрами, жанрами, фильтрацией и сортировкой.

## Запуск

Из каталога `DjangoFilms` выполните:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Django
python manage.py migrate
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`.

## Возможности

- Добавление фильмов, режиссёров и жанров через формы.
- Фильтрация каталога по жанру и режиссёру, поиск по названию.
- Сортировка по названию, году, рейтингу и длительности.
Модель фильма связана с режиссёром (`CASCADE`) и жанром (`PROTECT`).
