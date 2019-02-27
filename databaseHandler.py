from models import *
from datetime import datetime

#This module handles the database calls to the gui

def create_tables():
    db.connect()
    db.create_tables([Game, MerchandiseItem, SaleRecord])
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
    query = MerchandiseItem.select().where(MerchandiseItem.description == description)
    for row in query:
        row.amount += int(amount)
        return True
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
    merchandiseID = MerchandiseItem.get(MerchandiseItem.description == description).id
    itemAmount = MerchandiseItem.get_by_id(merchandiseID).amount
    SaleRecord.get(SaleRecord.merchandiseID==merchandiseID, SaleRecord.gameID==gameID)
    if amount>itemAmount:
        raise BaseException
    else:
        itemAmount -= amount
        MerchandiseItem.update({MerchandiseItem.amount:itemAmount}).where(MerchandiseItem.id==merchandiseID).execute()
        SaleRecord.update({SaleRecord.amount: SaleRecord.amount + amount}).where((SaleRecord.merchandiseID == merchandiseID)&(SaleRecord.gameID == gameID)).execute()


def create_sale_record(description, venue, amount):
    gameID = Game.get(Game.venue == venue).id
    merchandiseID = MerchandiseItem.get(MerchandiseItem.description == description).id
    itemAmount = MerchandiseItem.get_by_id(merchandiseID).amount
    if int(amount)>itemAmount:
        raise BaseException
    else:
        itemAmount -= int(amount)
        MerchandiseItem.update({MerchandiseItem.amount: itemAmount}).where(MerchandiseItem.id == merchandiseID).execute()
        SaleRecord.create(
        merchandiseID=merchandiseID,
        gameID=gameID,
        amount=amount
    )


def top_sales():
    subquery = SaleRecord.select(SaleRecord.merchandiseID.alias('merchandiseID'), fn.SUM(SaleRecord.amount).alias('total')).group_by(SaleRecord.merchandiseID)
    query = MerchandiseItem.select(MerchandiseItem.description, subquery.c.total).join(subquery, on=(subquery.c.merchandiseID == MerchandiseItem.id)).order_by(subquery.c.total.desc()).execute()
    list = []
    for row in query:
        list.append(row.description + " was sold " + str(row.salerecord.total) + " times")
    return list


def amount_sold(description):
    list = []
    itemID = MerchandiseItem.get(MerchandiseItem.description == description).id
    query = SaleRecord.select(SaleRecord.merchandiseID, fn.Sum(SaleRecord.amount).alias('total')).where(SaleRecord.merchandiseID == itemID).group_by(SaleRecord.merchandiseID).execute()
    for row in query:
        list.append(description + " was sold " + str(row.total) + " times")
    if len(list)==0:
        list.append(description + " was not sold at all.")
    return list