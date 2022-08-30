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

    class Meta:
        database = db
        db_table = 'hotel'


def initiate_tables():
    HotelDb.create_table()
    UserDataDb.create_table()
    CommandDataDb.create_table()