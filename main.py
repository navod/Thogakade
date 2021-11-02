import click
import sys
from customer import *
import os
from item import *
from order import place_order

# folders 
__db_location__ = "db"
__item_folder__ = f"{__db_location__}/item"
__customer_folder__ = f"{__db_location__}/customer"
__order_folder__ = f"{__db_location__}/order"
__order_detail_folder__ = f"{__db_location__}/order_detail"

def init(arguments):

    def db():
        os.makedirs(__customer_folder__)
        os.makedirs(__item_folder__)
        os.makedirs(__order_folder__)
        os.makedirs(__order_detail_folder__)

    section = arguments[0]
    if section == "init":
        command = arguments[1]
        if command == "db":
            db()

if __name__ == '__main__':
    arguments = sys.argv[1:]
    

    init(arguments)

    section = arguments[0]
    command = arguments[1]
    params = arguments[2:]

    if section == "item":
        if command == "create":
            create_item(*params)
        elif command == "all":
            get_all_items()
        elif command == "view":
            item_view_by_id(*params)
        elif command == "delete":
            item_delete(*params)
    elif section == "customer":
        if command == "create":
            create_customer(*params)
        elif command == "all":
            get_all_customers()
        elif command == "view":
            customer_view_by_id(*params)
        elif command == "delete":
            customer_delete(*params)
    elif section == "order":
        if command == "place":
            place_order(*params)
