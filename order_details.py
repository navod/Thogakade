import json
import os
from pprint import pprint
import datetime
from collections import namedtuple
from item import Item, item_get_by_id, item_update, item_view_by_id
import order

__db_location__ = "db"
__order_detail_folder__ = f"{__db_location__}/order_detail"
__order_detail_last_id__ = f"{__db_location__}/order_detail_id.db"
__user_id__ = f"{__db_location__}/user.db"

class OrderDetails():
    def __init__(self) :
        if os.path.exists(__order_detail_last_id__):
            with open(__order_detail_last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},orderId:{self.order_id},customerId:{self.customer_id},itemId:{self.item_id},name:{self.item_name},qty:{self.qty},price:{self.price}"


    def __str__(self):
        return f"id:{self.id},orderId:{self.order_id},customerId:{self.customer_id},itemId:{self.item_id},name:{self.item_name},qty:{self.qty},price:{self.price}"

    def save_order_details(self):
        id = self.last_id+1

        # Save database item
        _data_ = {
            "id": id,
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "itemId": self.item_id,
            "name": self.item_name,
            "qty":self.qty,
            "price":self.price
        }
        with open(f"{__order_detail_folder__}/{id}.db", "w") as order_detail_file:
            json.dump(_data_, order_detail_file)

        # Save next id
        self.last_id += 1
        with open(__order_detail_last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_order_by_path(self,order_detail, path):
        
        with open(path, "r") as order_detail_file:
            _data_ = json.load(order_detail_file)
            order_detail.id = _data_["id"]
            order_detail.order_id = _data_["order_id"]
            order_detail.customer_id = _data_["customer_id"]
            order_detail.item_id = _data_["itemId"]
            order_detail.item_name = _data_["name"]
            order_detail.qty = _data_["qty"]
            order_detail.price = _data_["price"]
           
        
    def all_orders(self):
        order_detail_file_names = os.listdir(__order_detail_folder__)
        orderDetails = []
        for order_det_file_name in order_detail_file_names:
            order_detail = OrderDetails()
            order_detail.__get_order_by_path(
                order_detail, f"{__order_detail_folder__}/{order_det_file_name}")
            orderDetails.append(order_detail)
        return orderDetails

    def get_by_id(self,id):
        order_details = OrderDetails()
        order_details.__get_order_by_path(order_details, f"{__order_detail_folder__}/{id}.db")
        return order_details

    def delete(self,id,item_id,qty):
        if os.path.exists(f"{__order_detail_folder__}/{id}.db"):
            os.remove(f"{__order_detail_folder__}/{id}.db")
            if os.path.exists("db/order/"f"{id}.db"):
                os.remove("db/order/"f"{id}.db")
                item_update(item_id,qty)
                print("** order ",id,"deleted","**")
        else:
            print("The order does not exist")

    def _get_user_by_path(self):
        if os.path.exists(__user_id__):
            with open(__user_id__, "r") as last_id_f:
                return last_id_f.readline()


def place_order_details(orderId,customerId,itemId,qty,price):
    items = item_get_by_id(itemId)
    order_details = OrderDetails()
    order_details.order_id = orderId
    order_details.customer_id = customerId
    order_details.item_id = itemId
    order_details.qty = qty
    order_details.price = float(price) * float(qty)
    order_details.item_name = items.name
    
    
    is_update_qty = update_qty(items,qty)
    
    if is_update_qty:
        order_details.save_order_details()
        return True
    
    else:
        return False

def update_qty(items,qty):
    item_dict = vars(items)
    new_qty = str(int(item_dict["qty"]) - int(qty))

    with open("db/item/"f"{items.id}.db", "r") as jsonFile:
        data = json.load(jsonFile)

    data["qty"] = new_qty

    with open("db/item/"f"{items.id}.db", "w") as jsonFile:
        json.dump(data, jsonFile)
        return True
    
def update_order():
    old_item_id = input('What item do you want to change? (enter id) :')
    new_item_id = input("what item do you want? (enter id) :")
    new_qty = input("How many qty do you want ? :")

    order_detail = OrderDetails()
    order_details = order_detail.all_orders()
    order_cust_id = order_detail._get_user_by_path()
    orders_tuple = tuple(order_details)

    cust_orders =[]

    # check customer have an order and get their orders
    for i in range(len(order_details)):
        if old_item_id == orders_tuple[i].item_id and order_cust_id == orders_tuple[i].customer_id :
            cust_orders.append(orders_tuple[i].order_id)


    if len(cust_orders) > 1:
        print("You have ordered same items (order id's : "f"{cust_orders}")
        order_id = input("Select your order id : ")
        update_order_details(order_id,new_item_id,new_qty,old_item_id)

    elif len(cust_orders) == 0:
        print("** Sorry order does not match..! **")
    else:
       update_order_details(cust_orders[0],new_item_id,new_qty,old_item_id)

  
def update_order_details(order_id,new_item_id,qty,old_item_id):
    
    order_detail = OrderDetails()
    order_details = order_detail.get_by_id(order_id) 
    new_items = item_get_by_id(new_item_id)
    
    is_update_qty = update_qty(new_items,qty)

    # new order update
    if is_update_qty:
           if update_new_order(order_id,new_item_id,qty,new_items.name,new_items.selling_price):
                if update_old_qty(old_item_id,order_details.qty):
                    print("** Order Updated..! **")
           

def update_old_qty(old_item_id,qty):
    old_items = item_get_by_id(old_item_id)
    item_dict = vars(old_items)
    new_qty = str(int(item_dict["qty"]) + int(qty))

    with open("db/item/"f"{old_items.id}.db", "r") as jsonFile:
        data = json.load(jsonFile)

    data["qty"] = new_qty

    with open("db/item/"f"{old_items.id}.db", "w") as jsonFile:
        json.dump(data, jsonFile)
        return True
     
def update_new_order(order_id,new_item_id,qty,name,price):
    # old_orders = order_view_by_id(order_id)
    # order_dict = vars(old_orders)

    with open("db/order_detail/"f"{order_id}.db", "r") as jsonFile:
        data = json.load(jsonFile)

    data["qty"] = qty
    data["itemId"] = new_item_id
    data["name"] = name
    data["price"] = str(float(price) * int(qty))

    with open("db/order_detail/"f"{order_id}.db", "w") as jsonFile:
        json.dump(data, jsonFile)
        return True

def get_all_orders():
    order_detail = OrderDetails()
    items = order_detail.all_orders()
    print('----------------------------------------------------------------------------------------------------------------------')
    print('|                                                        orders                                                       |')
    print('----------------------------------------------------------------------------------------------------------------------')
    pprint(items)
    print('----------------------------------------------------------------------------------------------------------------------')

def order_view_by_id(id):
    order_detail = OrderDetails()
    order_detail.id = id
    order_details = order_detail.get_by_id(id)
    print('----------------------------------------------------------------------------------------------------------------------')
    print('|                                                        orders                                                       |')
    print('----------------------------------------------------------------------------------------------------------------------')
    pprint(order_details)
    print('----------------------------------------------------------------------------------------------------------------------')
def order_delete(id):
    order_detail = OrderDetails()
    order_details = order_detail.all_orders()
    orders_tuple = tuple(order_details)
    order_cust_id = order.Order._get_user_by_path()
    cust_orders =[]
  
    # check customer have an order and get their orders
    for i in range(len(order_details)):
        if int(id) == int(orders_tuple[i].order_id) and int(order_cust_id) == int(orders_tuple[i].customer_id) :
            cust_orders.append(orders_tuple[i].order_id)
            order_detail.id = id
            order_detail.delete(id,orders_tuple[i].item_id,orders_tuple[i].qty)
    if len(cust_orders) == 0:
        print("** User did not place order ..! **")