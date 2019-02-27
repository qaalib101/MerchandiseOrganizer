from MerchandiseGUI import *
from databaseHandler import *

def main():
    create_tables()
    saleItems = get_all_items()
    games = get_all_games()
    init_gui(saleItems, games)


if __name__ == "__main__":
    main()