import datetime
from config_data.config import TOWNS


def get_complete_town_name(town):
    ltown = town.lower()
    for town_data in TOWNS:
        if ltown in town_data.get('city_ru').lower():
            return town_data.get('city_ru')
        elif ltown in town_data.get('city_en').lower():
            return town_data.get('city_en')
    return None


def get_dates_for_low_high_prices() -> (str, str):
    cur_date = datetime.date.today()
    start_day = cur_date + datetime.timedelta(days=1)
    end_day = start_day + datetime.timedelta(days=1)
    start_day_str = start_day.strftime("%Y-%m-%d")
    end_day_str = end_day.strftime("%Y-%m-%d")
    return start_day_str, end_day_str
