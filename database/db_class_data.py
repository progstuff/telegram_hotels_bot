from peewee import (AutoField, BigIntegerField, BooleanField, CharField,
                    DateTimeField, FloatField, ForeignKeyField, IntegerField,
                    Model, SmallIntegerField, SqliteDatabase)
from datetime import date

db = SqliteDatabase('bot_data.db')


class CurrentUserStateDb(Model):
    command_name = CharField(default='lowprice')
    city_en = CharField(default='')
    city_ru = CharField(default='')
    min_price = FloatField(default=0)
    max_price = FloatField(default=0)
    image_choose = BooleanField(default=False)
    cur_image_index = SmallIntegerField(default=1)
    max_image_index = SmallIntegerField(default=3)
    cur_page_index = SmallIntegerField(default=1)
    max_page_index = SmallIntegerField(default=5)
    photo_message_id = BigIntegerField(default=0)
    text_message_id = BigIntegerField(default=0)
    image_choose_keyboard_message_id = BigIntegerField(default=0)
    image_cnt_choose_keyboard_message_id = BigIntegerField(default=0)
    town_keyboard_message_id = BigIntegerField(default=0)
    price_keyboard_message_id = BigIntegerField(default=0)
    distance_keyboard_message_id = BigIntegerField(default=0)
    pages_cnt_keyboard_message_id = BigIntegerField(default=0)
    date_in = DateTimeField()
    date_out = DateTimeField()

    class Meta:
        database = db
        db_table = 'current_user_state'


class CommandDataDb(Model):
    id = AutoField(primary_key=True)
    user_id = BigIntegerField()
    command_name = CharField()
    invoke_time = DateTimeField()
    date_in = DateTimeField()
    date_out = DateTimeField()
    town_ru = CharField()
    town_en = CharField()

    def convert_date_to_str(self, date):
        day = date.day
        day_str = ''
        if day < 10:
            day_str = '0'
        day_str += str(day)

        month = date.month
        month_str = ''
        if month < 10:
            month_str = '0'
        month_str += str(month)

        date_str = '-'.join([day_str,
                             month_str,
                             str(date.year)])
        return date_str

    def get_str_view(self) -> str:
        date_str = self.convert_date_to_str(self.invoke_time)
        data = ' '.join([' '*20, self.command_name, date_str])
        result = '\n'.join(['='*32,
                            data,
                            '  город {}'.format(self.town_ru),
                            '   дата заселения {}'.format(self.convert_date_to_str(self.date_in)),
                            '   дата выселения {}'.format(self.convert_date_to_str(self.date_out)),
                            '='*32])
        return result

    class Meta:
        database = db
        db_table = 'comand_data'


class HotelDb(Model):
    hotel_id = BigIntegerField(primary_key=True)
    name = CharField()
    address = CharField()
    distance_to_center = CharField()
    one_day_price = FloatField()
    days_cnt = IntegerField()
    total_price = FloatField()
    url = CharField()

    def get_str_view(self) -> str:
        rez = '\n'.join(["отель: {}".format(self.name),
                         "адрес: {}".format(self.address),
                         "расстояние до центра: {}".format(self.distance_to_center),
                         "цена за ночь: {}$".format(int(round(self.one_day_price))),
                         "число ночей: {}".format(self.days_cnt),
                         "суммарная стоимость: {0}$".format(int(round(self.total_price))),
                         "страница отеля: {}".format(self.url)])
        return rez

    def update_total_price(self, date_in, date_out):
        d1 = date(date_in.year, date_in.month, date_in.day)
        d2 = date(date_out.year, date_out.month, date_out.day)
        days = (d2 - d1).days
        self.days_cnt = days
        self.total_price = self.one_day_price*days

    class Meta:
        database = db
        db_table = 'hotel'


class HotelImageLinkDb(Model):
    url = CharField(primary_key=True)
    hotel_id = ForeignKeyField(HotelDb)

    class Meta:
        database = db
        db_table = 'hotel_images_url'


class CommandHotelsDb(Model):
    command_data = ForeignKeyField(CommandDataDb)
    hotel_id = ForeignKeyField(HotelDb)

    class Meta:
        database = db
        db_table = 'comand_hotels'


def convert_datetime_field_to_date(date_time_field: DateTimeField):
    return date(date_time_field.year, date_time_field.month, date_time_field.day)


def initiate_tables():
    HotelDb.create_table()
    HotelImageLinkDb.create_table()
    CommandHotelsDb.create_table()
    CommandDataDb.create_table()