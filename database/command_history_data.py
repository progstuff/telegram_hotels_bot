from peewee import *

db = SqliteDatabase('bot_data.db')


class UserDataDb(Model):
    id = AutoField()
    user_id = IntegerField()
    date_in = DateTimeField()
    date_out = DateTimeField()
    town_ru = CharField()
    town_en = CharField()

    class Meta:
        database = db
        db_table = 'users'


class CommandDataDb(Model):
    id = AutoField()
    user = ForeignKeyField(UserDataDb, backref='pets')
    command_name = CharField()
    invoke_time = DateTimeField()

    def get_str_view(self) -> str:
        day = self.invoke_time.day
        day_str = ''
        if day < 10:
            day_str = '0'
        day_str += str(day)

        month = self.invoke_time.month
        month_str = ''
        if month < 10:
            month_str = '0'
        month_str += str(month)

        date_str = '-'.join([day_str,
                             month_str,
                             str(self.invoke_time.year)])

        data = ' '.join([self.command_name, date_str])
        return data

    class Meta:
        database = db
        db_table = 'comand_data'


class HotelDb(Model):
    id = AutoField()
    command_data = ForeignKeyField(CommandDataDb, backref='pets')
    name = CharField()
    address = CharField()
    distance_to_center = CharField()
    one_day_price = CharField()
    days_cnt = IntegerField()
    total_price = FloatField()
    url = CharField()

    def get_str_view(self) -> str:
        rez = '\n'.join(["    отель: {}".format(self.name),
                         "    адрес: {}".format(self.address),
                         "    расстояние до центра: {}".format(self.distance_to_center),
                         "    цена за ночь: {}".format(self.one_day_price),
                         "    число ночей: {}".format(self.days_cnt),
                         "    суммарная стоимость: {0}$".format(int(round(self.total_price))),
                         "    страница отеля: {}".format(self.url),])
        return rez


    class Meta:
        database = db
        db_table = 'hotel'


def initiate_tables():
    HotelDb.create_table()
    UserDataDb.create_table()
    CommandDataDb.create_table()