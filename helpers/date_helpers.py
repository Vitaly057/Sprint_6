from datetime import datetime, timedelta


def future_date(days_ahead):
    return (datetime.now() + timedelta(days=days_ahead)).strftime("%d.%m.%Y")
