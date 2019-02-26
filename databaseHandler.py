from models import *
from datetime import datetime

#This module handles the database calls to the gui

def create_tables():
    db.connect()
    db.create_tables([Game, MerchandiseItem, SaleRecord])

def add_default_data():
    add_merchandise_data()
    add_game_data()
    add_sale_record_data()

def add_merchandise_data():
    MerchandiseItem.create(
        type = "Clothing",
        description = "Jersey",
        amount = 200,
        price = 30.00
    )
    MerchandiseItem.create(
        type = "Appliances",
        description = "Thermos",
        amount = 100,
        price = 20.00
    )
    MerchandiseItem.create(
        type = "Clothing",
        description = "Sweater",
        amount = 100,
        price = 25.00
    )
def add_game_data():
    Game.create(
        venue = "Madison Square Garden",
        date = datetime(2019, 1, 5)
    )
    Game.create(
        venue = "US Bank Stadium",
        date = datetime(2019, 1, 10)
    )
    Game.create(
        venue = "Metro Stadium",
        date = datetime(2019, 1, 15)
    )
def add_sale_record_data():
    SaleRecord.create(
        merchandiseID = MerchandiseItem.get_by_id(2),
        gameID = MerchandiseItem.get_by_id(1),
        amount = 50
    )


def get_all_games():
    list = []
    query = Game.select()
    for row in query:
        list.append(row.venue)
    comboList = tuple(list)
    return comboList


def get_all_items():
    list = []
    query = MerchandiseItem.select()
    for row in query:
        list.append(row.description)
    comboList = tuple(list)
    return comboList


def add_item(type, description, amount, price):
    MerchandiseItem.create(
        type=type,
        description=description,
        amount=amount,
        price=price
    )
def add_venue(venue, date):
    Game.create(
        venue=venue,
        date=date
    )
def add_sale_item(description, venue, amount):
    gameID = Game.get(Game.venue == venue).id
    merchandiseID = MerchandiseItem.get(MerchandiseItem.description==description).id
    SaleRecord.create(
        merchandiseID=merchandiseID,
        gameID=gameID,
        amount=amount
    )
