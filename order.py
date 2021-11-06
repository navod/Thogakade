import json
import os
from pprint import pprint
import datetime
from customer import USER

from order_details import place_order_details

__db_location__ = "db"
__order_folder__ = f"{__db_location__}/order"
__order__last_id__ = f"{__db_location__}/order_id.db"
__user_id__ = f"{__db_location__}/user.db"

class Order():
    def __init__(self) :
        if os.path.exists(__order__last_id__):
            with open(__order__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},customerId:{self.customer_id},date:{self.date}"


    def __str__(self):
        return f"id:{self.id},customerId:{self.customer_id},date:{self.date}"

    def save_order(self):
        id = self.last_id+1

        # Save database orders
        _data_ = {
            "id": id,
            "customer_id": self.customer_id,
            "date": self.date,
        }
        with open(f"{__order_folder__}/{id}.db", "w") as item_file:
            json.dump(_data_, item_file)

        # Save next id
        self.last_id += 1
        with open(__order__last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_order_by_path(order, path):
        
        with open(path, "r") as item_file:
            _data_ = json.load(item_file)
            order.id = _data_["id"]
            order.customer_id = _data_["customerId"]
            order.date = _data_["date"]


    def _get_user_by_path():
        if os.path.exists(__user_id__):
            with open(__user_id__, "r") as last_id_f:
                return last_id_f.readline()
            

    def all_orders(self):
        order_file_names = os.listdir(__order_folder__)
        orders = []
        for order_file_name in order_file_names:
            order = Order()
            order.__get_order_by_path(
                order, f"{__order_folder__}/{order_file_name}")
            orders.append(order)
        return orders


    def get_by_id(self,id):
        Order.__get_order_by_path(self, f"{__order_folder__}/{id}.db")

    def delete_item(self,id):
        if os.path.exists(f"{__order_folder__}/{id}.db"):
            os.remove(f"{__order_folder__}/{id}.db")
            print("**",id,"deleted","**")
        else:
            print("The order does not exist")



def place_order(itemId,qty):
    try:
        order = Order()
        order.customer_id = Order._get_user_by_path()
        order.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_qty_available = check_qty(itemId,qty)
    
        if is_qty_available[0] :
            order.save_order()
            is_place = place_order_details(order.last_id,USER,itemId,qty,is_qty_available[1])
            if  is_place:
                print("Your order placed..!")
    except:
        print("** Could not match item id..! **")
   
   

def check_qty(itemId,qty):
   
    a = Order._get_user_by_path()
    
    if a is not None:
        with open("db/item/"f"{itemId}.db", "r") as jsonFile:
                data = json.load(jsonFile)


        have_qty = int(data["qty"])
        if int(have_qty) > int(qty):
            return True,float(data["sellingPrice"])
        else:
            print("** Sorry we have only "f"{have_qty} ..! **")
            return False,-1
    else:
        print("** Please login..! **")
        return False,-1

# def get_all_items():
#     item = Item()
#     items = item.all_items()
#     pprint(items)

# def item_view_by_id(id):
#     item = Item()
#     item.id = id
#     item.get_by_id(id)
#     print(item.id, item.name, item.price, item.selling_price)

# def item_delete(id):
#     item = Item()
#     item.id = id
#     item.delete_item(id)
    