import json
import os

__db_location__ = "db"
__item_folder__ = f"{__db_location__}/item"
__item__last_id__ = f"{__db_location__}/item_id.db"

def init(arguments):

    def db():
        os.makedirs(__item_folder__)

    section = arguments[0]
    if section == "init":
        command = arguments[1]
        if command == "db":
            db()

class Item():
    def __init__(self) :
        if os.path.exists(__item__last_id__):
            with open(__item__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0


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

def create_item(name,price,selling_price,qty):
    print(name)
    print(price)
    print(selling_price)
    print(qty)
    item = Item()
    item.name = name
    item.price = price
    item.selling_price = selling_price
    item.qty = qty
    item.save()