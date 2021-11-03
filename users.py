import json
import os
from pprint import pprint

__db_location__ = "db"
__item_folder__ = f"{__db_location__}/user"
__item__last_id__ = f"{__db_location__}/user_id.db"


class Item():
    def __init__(self) :
        if os.path.exists(__item__last_id__):
            with open(__item__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},name:{self.name},price:{self.price},sellingPrice:{self.selling_price},qty:{self.qty}"


    def __str__(self):
        return f"id:{self.id},name:{self.name},price:{self.price},sellingPrice:{self.selling_price},qty:{self.qty}"

    
    def save(self):
        id = self.last_id+1

        # Save database item
        _data_ = {
            "id": id,
            "name": self.name,
            "price": self.price,
            "sellingPrice": self.selling_price,
            "qty":self.qty
        }
        with open(f"{__item_folder__}/{id}.db", "w") as item_file:
            json.dump(_data_, item_file)

        # Save next id
        self.last_id += 1
        with open(__item__last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_item_by_path(item, path):
        
        with open(path, "r") as item_file:
            _data_ = json.load(item_file)
            item.id = _data_["id"]
            item.name = _data_["name"]
            item.price = _data_["price"]
            item.selling_price = _data_["sellingPrice"]
            item.qty = _data_["qty"]
        
    def all_items(self):
        item_file_names = os.listdir(__item_folder__)
        items = []
        for item_file_name in item_file_names:
            item = Item()
            Item.__get_item_by_path(
                item, f"{__item_folder__}/{item_file_name}")
            items.append(item)
        return items

    def get_by_item_id(self,id):
        Item.__get_item_by_path(self, f"{__item_folder__}/{id}.db")

    def delete_item(self,id):
        if os.path.exists(f"{__item_folder__}/{id}.db"):
            os.remove(f"{__item_folder__}/{id}.db")
            print("**",id,"deleted","**")
        else:
            print("The item does not exist")



def create_item(name,price,selling_price,qty):
    item = Item()
    item.name = name
    item.price = price
    item.selling_price = selling_price
    item.qty = qty
    item.save()

def get_all_items():
    item = Item()
    items = item.all_items()
    pprint(items)

def item_view_by_id(id):
    item = Item()
    item.id = id
    item.get_by_item_id(id)
    print(item.id, item.name, item.price, item.selling_price, item.qty)
    return item

def item_delete(id):
    item = Item()
    item.id = id
    item.delete_item(id)
    