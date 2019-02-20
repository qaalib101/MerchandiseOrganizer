from peewee import*

db = SqliteDatabase('merchandise.db')

class BaseModel(Model):
    class Meta:
        database = db

class Game(BaseModel):
    venue = CharField()
    date = DateField()

class MerchandiseItem(BaseModel):
    type = CharField()
    description = CharField(unique=True)
    amount: IntegerField()
    price = DecimalField()


class SaleRecord(BaseModel):
    gameID = ForeignKeyField(Game)
    merchandiseID = ForeignKeyField(MerchandiseItem)
    amountSold = IntegerField()

