from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import peewee
import databaseHandler
from datetime import datetime

window = Tk()
window.title("Sports Merchandise Application")

def add_sale(item, venue, amount):
    try:
        databaseHandler.add_sale_item(item.get(), venue.get(), amount.get())
    except ValueError:
        show_message("Enter a correct value")
    except peewee.DoesNotExist:
        create_sale(item, venue, amount)
    except BaseException:
        show_message('Amount entered is bigger than in stock')
    amount.delete(0, END)


def create_sale(item, venue, amount):
    try:
        databaseHandler.create_sale_record(item.get(), venue.get(), amount.get())
    except BaseException:
        show_message('Amount entered is bigger than in stock')
    amount.delete(0, END)


def add_venue(location, day, month, year):
    try:
        date = datetime(int(year.get()), int(month.get()), int(day.get()))
        databaseHandler.add_venue(location.get(), date)
        update_venue()
    except ValueError as e:
        show_message(e)
    except TypeError as e:
        show_message(e)
    location.delete(0, END)
def add_item(type, description, amount, price):
    try:
        databaseHandler.add_item(type.get(), description.get(), amount.get(), price.get())
        update_item()
    except ValueError:
        show_message("Input correct values")
    except peewee.IntegrityError:
        show_message("Cannot add another")
    description.delete(0, END)
    amount.delete(0, END)
    price.delete(0, END)

def init_gui(items, games):
    init_add_item()
    init_add_venue()
    init_add_sale(items, games)
    init_add_analysis()
    window.mainloop()
def init_add_item():
    typelabel = Label(window, text="Type")
    typelabel.grid(column=0, row=0)
    description = Label(window, text="Description")
    description.grid(column=1, row=0)
    amount = Label(window, text="Amount")
    amount.grid(column=2, row=0)
    price = Label(window, text="Price")
    price.grid(column=3, row=0)
    itemTypeComboBox = ttk.Combobox(window, width=15)
    itemTypeComboBox['values'] = ('Clothing', 'Condiments', 'Appliances')
    itemTypeComboBox.current(1)
    itemTypeComboBox.grid(column=0, row=1)
    itemDescription = Entry(window, width=10)
    itemDescription.grid(column=1, row=1)
    itemAmount = Entry(window, width=10)
    itemAmount.grid(column=2, row=1)
    itemPrice = Entry(window, width=10)
    itemPrice.grid(column=3, row=1)
    itemButton = Button(window, text="Add a sale item", command=lambda: add_item(itemTypeComboBox, itemDescription, itemAmount, itemPrice))
    itemButton.grid(column=4, row=1)
def init_add_venue():
    venueLabel = Label(window, text="Venue Location")
    venueLabel.grid(column=0, row=2)
    month = Label(window, text="Month")
    month.grid(column=1, row=2)
    day = Label(window, text="Day")
    day.grid(column=2, row=2)
    year = Label(window, text="Year")
    year.grid(column=3, row=2)

    venueLocation = Entry(window, width=10)
    venueLocation.grid(column=0, row=3)
    venueDay = ttk.Combobox(window, width=2)
    venueDay['values'] = tuple([d for d in range(1, 32, 1)])
    venueDay.current(1)
    venueDay.grid(column=2, row=3)

    venueMonth = ttk.Combobox(window, width=2)
    venueMonth['values'] = tuple([m for m in range(1, 13, 1)])
    venueMonth.current(1)
    venueMonth.grid(column=1, row=3)

    venueYear = ttk.Combobox(window, width=4)
    venueYear['values'] = tuple([y for y in range(2000, 2025, 1)])
    venueYear.current(1)
    venueYear.grid(column=3, row=3)

    venueButton = Button(window, text="Add a venue", command=lambda: add_venue(venueLocation, venueDay, venueMonth, venueYear))
    venueButton.grid(column=4, row=3)


def init_add_sale(saleItems, saleVenues):
    itemLabel = Label(window, text="Item")
    itemLabel.grid(column=0, row=4)
    venue = Label(window, text="Location")
    venue.grid(column=2, row=4)
    amount = Label(window, text="Amount")
    amount.grid(column=2, row=4)

    saleItem = ttk.Combobox(window, width=15)
    saleItem['values'] = saleItems
    saleItem.current(1)
    saleItem.grid(column=0, row=5)

    saleVenue = ttk.Combobox(window, width=15)
    saleVenue['values'] = saleVenues
    saleVenue.current(1)
    saleVenue.grid(column=1, row=5)

    saleAmount = Entry(window, width=10)
    saleAmount.grid(column=2, row=5)
    saleButton = Button(window, text="Add a sale", command=lambda: add_sale(saleItem, saleVenue, saleAmount))
    saleButton.grid(column=4, row=5)


def init_add_analysis():
    analysisListBox = Listbox(window, width=20)
    analysisListBox.grid(column=1, row=7, padx=5, pady=5)
    topSalesButton = Button(window, text="Top Items Sold", command=lambda: get_top_sales(analysisListBox))
    topSalesButton.grid(column=0, row=6)
    itemComboBox = ttk.Combobox(window, width=15)
    itemComboBox['values'] = databaseHandler.get_all_items()
    itemComboBox.current(0)
    itemComboBox.grid(column=1, row=6)
    amountSoldButton= Button(window, text="Amount Sold", command=lambda: get_amount_sold(analysisListBox, itemComboBox))
    amountSoldButton.grid(column=2, row=6)


def show_message(message):
    messagebox.showinfo("Alert", message)

def update_item():
    saleItem = ttk.Combobox(window, width=15)
    saleItem['values'] = databaseHandler.get_all_items()
    saleItem.current(0)
    saleItem.grid(column=0, row=5)

def update_venue():
    saleVenue = ttk.Combobox(window, width=15)
    saleVenue['values'] = databaseHandler.get_all_games()
    saleVenue.current(0)
    saleVenue.grid(column=1, row=5)
def get_top_sales(listBox):
    listBox.delete(0, END)
    list = databaseHandler.top_sales()
    for item in list:
        listBox.insert(END, item)

def get_amount_sold(listBox, comboBox):
    listBox.delete(0, END)
    list = databaseHandler.amount_sold(comboBox.get())
    for item in list:
        listBox.insert(END, item)