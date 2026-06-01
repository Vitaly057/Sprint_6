from helpers.date_helpers import future_date

order_data = [
    {
        "button_location": "top",
        "name": "Дмитрий",
        "surname": "Печкунов",
        "address": "ул. Ленина 1",
        "metro": "Третьяковская",
        "phone": "89991234567",
        "date": future_date(1),
        "period": "сутки",
        "color": "черный",
        "comment": "Позвоните за 15 минут",
    },
    {
        "button_location": "bottom",
        "name": "Анна",
        "surname": "Печкунова",
        "address": "Бульвар молодежи 10",
        "metro": "Курская",
        "phone": "89997654321",
        "date": future_date(2),
        "period": "семеро суток",
        "color": "серый",
        "comment": "Домофон #345678",
    },
]
