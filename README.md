# api_test
Тестовое задание на DRF 


### Запуск проекта

#### Cоздание вертуального окружения:

```bash
python3 -m venv env
```

Запуск вертуального окружения:
```bash
source env/bin/activate
```

#### Создать .env  в репозитории добавить SECRET_KEY:

#### Установить зависимости

```bash
pip install -r requirements.txt
```
#### Провести миграции

```bash
python manage.py migrate
```

#### Загрузить фикстуру

```bash
python manage.py loaddata service
```