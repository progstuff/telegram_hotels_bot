import datetime

from config_data.config import TOWNS


def get_complete_town_name(town: str) -> (list, list):
    ltown = town.lower()
    towns_ru = []
    towns_en = []
    total_max_cnt = 10
    cnt = 0
    for town_data in TOWNS:
        if ltown in town_data.get('city_ru').lower() or ltown in town_data.get('city_en').lower():
            towns_ru.append(town_data.get('city_ru'))
            towns_en.append(town_data.get('city_en'))
            cnt += 1
            if cnt >= total_max_cnt:
                break
    if cnt == 0:
        return None, None
    return towns_ru, towns_en


def get_dates_for_low_high_prices() -> (str, str):
    cur_date = datetime.date.today()
    start_day = cur_date + datetime.timedelta(days=1)
    end_day = start_day + datetime.timedelta(days=1)
    start_day_str = start_day.strftime("%Y-%m-%d")
    end_day_str = end_day.strftime("%Y-%m-%d")
    return start_day_str, end_day_str


def translate_date(d):
    if d == 'year':
        return 'год'
    if d == 'day':
        return 'день'
    if d == 'month':
        return 'месяц'