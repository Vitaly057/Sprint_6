from datetime import datetime, timedelta


def future_date(days_ahead):
    return (datetime.now() + timedelta(days=days_ahead)).strftime("%d.%m.%Y")


def to_data_day(date_str: str) -> str:
    day, month, year = date_str.split(".")
    return f"{int(day)}.{int(month)}.{year}"
