# Сервис контроля заданий на выпуск продукции

## Локальный запуск:

1. Создать .env файл из темплейта
```bash
make env
```

<details> <summary> Шаблон наполнения .env </summary>

```
Example of filling a file .env:

DRIVER=postgresql+asyncpg
DB_HOST=postgres
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres

OTEL=true
```

</details>

2. Адаптировать его под свои нужды
3. Сбилдить:

```bash
make build
```

4. Поднять приложение, бд, opentelemetry, prometheus, jaeger, loki, grafana


```bash
make up
```


## Запуск тестов:

```bash
make tests
```
