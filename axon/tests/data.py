import random

num = random.randint(1000, 99999999)
num_next = random.randint(1000, 99999999)

data = [
    {
        "СтатусЗакрытия": False,
        "ПредставлениеЗаданияНаСмену": f"Задание на тестовую смену {num}",
        "Линия": f"Линия {num}",
        "Смена": f"Смена {num}",
        "Бригада": f"Бригада {num}",
        "НомерПартии": num,
        "ДатаПартии": "2024-02-15",
        "Номенклатура": f"№ {num}",
        "КодЕКН": "654651",
        "ИдентификаторРЦ": "6553661",
        "ДатаВремяНачалаСмены": "2024-02-15T20:00:00+05:00",
        "ДатаВремяОкончанияСмены": "2024-02-15T08:00:00+05:00"
    },
    {
        "СтатусЗакрытия": False,
        "ПредставлениеЗаданияНаСмену": f"Задание на тестовую смену {num_next}",
        "Линия": f"Линия {num_next}",
        "Смена": f"Смена {num_next}",
        "Бригада": f"Бригада {num_next}",
        "НомерПартии": num_next,
        "ДатаПартии": "2024-02-15",
        "Номенклатура": f"№ {num_next}",
        "КодЕКН": "654651",
        "ИдентификаторРЦ": "6553661",
        "ДатаВремяНачалаСмены": "2024-02-15T20:00:00+05:00",
        "ДатаВремяОкончанияСмены": "2024-02-15T08:00:00+05:00"
    },
]

update = {
    "СтатусЗакрытия": False,
    "ПредставлениеЗаданияНаСмену": f"Задание на тестовую смену {num}",
    "Линия": f"Линия {num}",
    "Смена": f"Смена {num}",
    "Бригада": f"Бригада {num}",
    "Номенклатура": f"№ {num}",
    "КодЕКН": "654651",
    "ИдентификаторРЦ": "6553661"
}

data_product = [
    {
        "УникальныйКодПродукта": "string",
        "НомерПартии": 24472756,
        "ДатаПартии": "2024-02-15"
    }
]

aggregate = {
    "task_id": 1,
    "product_code": "st232ring"
}
