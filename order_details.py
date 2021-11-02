import json
import os
from pprint import pprint
import datetime

from item import Item, item_view_by_id

__db_location__ = "db"
__order_detail_folder__ = f"{__db_location__}/order_detail"
__order_detail_last_id__ = f"{__db_location__}/order_detail_id.db"


class OrderDetails():
    def __init__(self) :
        if os.path.exists(__order_detail_last_id__):
            with open(__order_detail_last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},orderId:{self.order_id},customerId:{self.customer_id},itemId:{self.item_id},qty:{self.qty},price:{self.price}"


    def __str__(self):
        return f"id:{self.id},orderId:{self.order_id},customerId:{self.customer_id},itemId:{self.item_id},qty:{self.qty},price:{self.price},"

    def save_order_details(self):
        id = self.last_id+1

        # Save database item
        _data_ = {
            "id": id,
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "itemId": self.item_id,
            "qty":self.qty,
            "price":self.price
        }
        with open(f"{__order_detail_folder__}/{id}.db", "w") as order_detail_file:
            json.dump(_data_, order_detail_file)

        # Save next id
        self.last_id += 1
        with open(__order_detail_last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_order_by_path(order_detail, path):
        
        with open(path, "r") as order_detail_file:
            _data_ = json.load(order_detail_file)
            order_detail.id = _data_["id"]
            order_detail.order_id = _data_["orderId"]
            order_detail.customer_id = _data_["customerId"]
            order_detail.item_id = _data_["itemId"]
            order_detail.qty = _data_["qty"]
            order_detail.price = _data_["price"]
        
    def all_orders(self):
        order_detail_file_names = os.listdir(__order_detail_folder__)
        orderDetails = []
        for order_det_file_name in order_detail_file_names:
            order = OrderDetails()
            order.__get_order_by_path(
                order, f"{__order_detail_folder__}/{order_det_file_name}")
            orderDetails.append(order)
        return orderDetails

    def get_by_id(self,id):
        OrderDetails.__get_order_by_path(self, f"{__order_detail_folder__}/{id}.db")

    def delete_item(self,id):
        if os.path.exists(f"{__order_detail_folder__}/{id}.db"):
            os.remove(f"{__order_detail_folder__}/{id}.db")
            print("**",id,"deleted","**")
        else:
            print("The order does not exist")



def place_order_details(orderId,customerId,itemId,qty,price):
    order_details = OrderDetails()
    order_details.order_id = orderId
    order_details.customer_id = customerId
    order_details.item_id = itemId
    order_details.qty = qty
    order_details.price = float(price) * float(qty)
    

    
    order_details.save_order_details()
    print(itemId)

    items = item_view_by_id(itemId)

    print(type(items))
    print(items)
    # print("Hello")

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
    