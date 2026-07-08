### Hexlet tests and linter status:
[![Actions Status](https://github.com/unlaudd/middle-python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/unlaudd/middle-python-project-83/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=unlaudd_middle-python-project-83&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=unlaudd_middle-python-project-83)

# Page Analyzer

Анализатор страниц — веб-приложение для SEO-анализа URL-адресов.

## Демо

https://middle-python-project-83-12h7.onrender.com

## Возможности

- Добавление URL для анализа
- Проверка доступности сайта (HTTP-запрос)
- Извлечение SEO-метаданных: title, h1, meta description
- История проверок для каждого URL
- Валидация URL-адресов
- Отображение кодов ответа сервера

## Технологии

- Python 3.12
- Flask
- PostgreSQL
- psycopg
- BeautifulSoup4
- requests
- Bootstrap 5
- Gunicorn
- uv (package manager)

## Установка

```bash
git clone https://github.com/unlaudd/middle-python-project-83.git
cd middle-python-project-83
make install
```

## Использование

### Переменные окружения
Создайте файл .env в корне проекта:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/page_analyzer
```

## Запуск
Локальная разработка:

```bash
make dev
```

Приложение доступно по адресу: `http://localhost:8000`

## Проверка кода

```bash
make lint
```

## Структура проекта

```
.
├── page_analyzer/
│   ├── __init__.py
│   ├── app.py
│   ├── checker.py
│   ├── db.py
│   ├── models.py
│   ├── validators_ext.py
│   └── templates/
├── database.sql
├── Makefile
├── pyproject.toml
└── README.md
```