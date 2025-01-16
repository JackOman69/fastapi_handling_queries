# FastAPI Проект для обработки заявок

Надежная система обработки приложений, созданная на основе `FastAPI`, которая обрабатывает и хранит приложения, а также интегрируется с `Kafka` для потоковой передачи событий.

## Технологии

- `FastAPI`
- `SQLAlchemy (Async)`
- `Alembic`
- `Kafka (aiokafka)`
- `PostgreSQL`
- `Docker`
- `Pytest`

## Особенности

- Создание новых заявок
- Получение заявок списком
- Фильтрация заявок используя *user_name*
- Асинхронная работа с базой данных через SQLAlchemy
- Потоковая обработка заявок через Kafka
- Логгирование системы в отдельный лог файл
- Базовые unit тесты для покрытия основного функционала

## API Endpoints

### Создание заявки
```http
POST /application

{
    "user_name": "Джон Уик",
    "description": "Заявка на покупку денег"
}
```

```http
200 OK
{
    "id": 1,
    "user_name": "Джон Уик",
    "description": "Заявка на покупку денег",
    "created_at": "2025-01-15T12:39:20.330961+00:00"
}
```

### Получение заявок
```http
GET /application?user_name=Джон%20Уик&page=1&size=10
```

```http
200 OK
{
    "id": 1,
    "user_name": "Джон Уик",
    "description": "Заявка на покупку денег",
    "created_at": "2025-01-15T12:39:20.330961+00:00"
}
```
## Запуск приложения

### Клонируйте репозиторий:

```console
git clone https://github.com/JackOman69/fastapi_handling_queries.git
```

### Установка .env:

* Создайте файл `.env` в корневой директории и вложите туда переменные (приведен пример):

```python
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=postgres
PG_DB=applications_db
KAFKA_BOOTSTRAP_SERVERS = "kafka:9092"
KAFKA_TOPIC = "applications"
```

### Запуск через Docker:

* Запускать проект нужно с помощью следующих команд:

```console
docker-compose up -d
```

### Инициализация топика Kafka:

* Для создания топика Kafka выполните следующую команду:

```console
 docker exec -it fastapi_handling_queries-kafka-1 echo "/usr/bin/kafka-topics --create --partitions 1 --replication-factor 1 --topic applications --bootstrap-server localhost:9092"
 ```

* С помощью данной команды выполнится создание топика Kafka с именем "applications" внутри докер контейнера.

### Запуск тестов:

* Для запуска тестов нужно зайти внутрь контейнера `fastapi_backend-1` и выполнить команду:

```console
pytest src/unit_tests/crud_operations_tests.py -v
```

### Проверка данных внутри топика Kafka:

* Для проверки данных внутри топика Kafka можно использовать следующую команду:

```console
 /usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic applications --from-beginning
 ```