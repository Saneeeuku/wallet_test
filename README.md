# Запуск:
#### 1) Переименовать .example.env в .env
#### 2) Docker compose
```bash
docker compose up -d
```
# Для тестирования (после запуска docker) 
#### 1) установить Poetry
```bash
pip install poetry==2.2.1
```
#### 2) Установить зависимости
```bash
poetry install --no-root
```
#### 3) Запустить Pytest
```bash
pytest
```