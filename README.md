Kaltoum Trading Journal

Этот проект — простое приложение дневника трейдов на Flask.
Позволяет добавлять записи о сделках через REST API, которые логируются в файл.
Логи собираются и отправляются в Loki через Promtail, визуализация происходит в Grafana.
Все сервисы запускаются вместе с помощью Docker Compose.
Что требовалось сделать

    Создать приложение дневника трейдов, принимающее данные и логирующее их.

    Настроить Loki и Promtail для сбора и передачи логов.

    Использовать Grafana для запроса и визуализации логов сделок.

    Продемонстрировать систему, добавив сделки, запросив логи и сделав скриншоты:

        Запущенных контейнеров Docker

        Успешного добавления сделки

        Логов, записанных в файл

        Логов, полученных из Loki

        Дашборда Grafana с отображением логов

Как использовать

    Собрать и запустить сервисы командой:

docker compose up --build

Добавить сделку через терминал с помощью curl:

curl -X POST http://localhost:8080/add_trade \
  -H "Content-Type: application/json" \
  -d '{"pair": "ETHUSD", "side": "long", "result": 150, "tags": "test"}'

Проверить файл логов, чтобы убедиться, что сделка записана:

cat trading_app/logs/trades.log

Запросить логи из Loki:

    curl -G http://localhost:3100/loki/api/v1/query --data-urlencode 'query={job="trading_journal"}'

    Открыть Grafana по адресу http://localhost:3000, войти и создать запросы для визуализации логов трейдов.

Kaltoum Trading Journal

This project is a simple trading journal application built with Flask.
It allows you to add trade entries via a REST API, which are logged into a file.
The logs are collected and sent to Loki using Promtail, and you can visualize them with Grafana.
All components run together using Docker Compose.
What the Task Asked

    Build the trading journal app to accept trade data and log it.

    Set up Loki and Promtail to collect and forward logs.

    Use Grafana to query and visualize the logged trades.

    Demonstrate the system by adding trades, querying logs, and showing screenshots of:

        Running Docker containers

        Successful trade addition

        Logs stored in the file

        Logs queried from Loki

        Grafana dashboard displaying the logs

How to Use

    Build and start the services with Docker Compose:

docker compose up --build

Add trades using curl commands in the terminal:

curl -X POST http://localhost:8080/add_trade \
  -H "Content-Type: application/json" \
  -d '{"pair": "ETHUSD", "side": "long", "result": 150, "tags": "test"}'

Check the logs file to confirm trades are recorded:

cat trading_app/logs/trades.log

Query Loki to see collected logs:

curl -G http://localhost:3100/loki/api/v1/query --data-urlencode 'query={job="trading_journal"}'

Open Grafana dashboard at http://localhost:3000, log in, and create queries to visualize your trading logs.
