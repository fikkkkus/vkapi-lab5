
# VK API Lab5

VK API Lab5 — это проект на Python для работы с данными из социальной сети ВКонтакте с использованием базы данных Neo4j.

## Установка и Запуск Проекта

### Шаг 1: Установка Neo4j Community Edition

Для установки **Neo4j Community Edition** на сервер Ubuntu следуйте инструкциям по [ссылке](https://www.techrepublic.com/article/how-to-install-neo4j-ubuntu-server/).

### Шаг 2: Клонирование Репозитория

1. Склонируйте репозиторий проекта:

   ```bash
   git clone https://github.com/fikkkkus/vkapi-lab5
   ```

2. Перейдите в директорию проекта:

   ```bash
   cd vkapi-lab5
   ```

### Шаг 3: Создание и Активация Виртуального Окружения

1. Создайте виртуальное окружение:

   ```bash
   python3 -m venv venv
   ```

2. Активируйте виртуальное окружение:
     ```bash
     source venv/bin/activate
     ```

### Шаг 4: Установка Зависимостей

Установите все зависимости проекта, используя команду:

```bash
pip install -r requirements.txt
```

### Шаг 5: Настройка PYTHONPATH

Убедитесь, что переменная окружения `PYTHONPATH` настроена корректно:

```bash
export PYTHONPATH=$(pwd)
```

### Шаг 6: Загрузка Базы Данных в Neo4j

1. Остановите текущий процесс Neo4j:

   ```bash
   neo4j stop
   ```

2. Загрузите базу данных в Neo4j из текущей директории. Бэкап базы данных был выполнен в формате **aligned**:

   ```bash
   neo4j-admin database load neo4j --from-path="." --overwrite-destination=true
   ```

### Шаг 7: Запуск Neo4j

После того как база данных загружена, запустите Neo4j:

```bash
neo4j start
```

### Шаг 8: Запуск Тестов

Для запуска тестов используйте команду **pytest**, будут проведены тесты для модели данных и тесты на каждую точку доступа:

```bash
pytest
```

## Документация для точек доступа

### 1. Получение всех узлов

#### HTTP-метод: `GET`

**URL**: `/nodes/`

**Описание**: Получить все узлы в базе данных.

**Пример запроса**:
```bash
curl -X GET "http://127.0.0.1:8000/nodes/"
```

### 2. Получение узла по ID с его связями

#### HTTP-метод: `GET`

**URL**: `/nodes/{node_id}`

**Описание**: Получить узел по указанному ID с его связями.

**Пример запроса**:
```bash
curl -X GET "http://127.0.0.1:8000/nodes/1"
```

### 3. Добавление новых узлов

#### HTTP-метод: `POST`

**URL**: `/add/nodes/`

**Описание**: Добавить новые узлы и их связи в базу данных.

**Пример запроса**:
```bash
curl -X POST "http://127.0.0.1:8000/add/nodes/" -H "Authorization: Bearer token" -H "Content-Type: application/json" -d "{"users": [{"id": "1"}, {"id": "2"}], "groups": [{"id": "3"}], "relations": [{"start_id": "1", "end_id": "2", "type": "follow"}, {"start_id": "2", "end_id": "3", "type": "subscribe"}]}"
```

### 4. Удаление узлов

#### HTTP-метод: `DELETE`

**URL**: `/delete/nodes/`

**Описание**: Удалить узлы по указанным ID.

**Пример запроса**:
```bash
curl -X DELETE "http://127.0.0.1:8000/delete/nodes/" -H "Authorization: Bearer token" -H "Content-Type: application/json" -d "["1", "2", "3"]"
```
