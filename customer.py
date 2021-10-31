import json
import os
from pprint import pprint


__db_location__ = "db"
__customer_folder__ = f"{__db_location__}/customer"
__customer__last_id__ = f"{__db_location__}/customer_id.db"



class Customer():
    def __init__(self) :
        if os.path.exists(__customer__last_id__):
            with open(__customer__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},name:{self.name},address:{self.address},contact:{self.contact}"


    def __str__(self):
        return f"id:{self.id},name:{self.name},address:{self.address},contact:{self.contact}"

    def save(self):
        id = self.last_id+1

        # Save database item
        _data_ = {
            "id": id,
            "name": self.name,
            "address": self.address,
            "contact": self.contact,
        }
        with open(f"{__customer_folder__}/{id}.db", "w") as customer_file:
            json.dump(_data_, customer_file)

        # Save next id
        self.last_id += 1
        with open(__customer__last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_item_by_path(customer, path):
        
        with open(path, "r") as customer_file:
            _data_ = json.load(customer_file)
            customer.id = _data_["id"]
            customer.name = _data_["name"]
            customer.address = _data_["address"]
            customer.contact = _data_["contact"]
        
    def all_customers(self):
        customer_file_names = os.listdir(__customer_folder__)
        customers = []
        for customer_file_name in customer_file_names:
            customer = Customer()
            Customer.__get_item_by_path(
                customer, f"{__customer_folder__}/{customer_file_name}")
            customers.append(customer)
        return customers

    def get_by_id(self,id):
        Customer.__get_item_by_path(self, f"{__customer_folder__}/{id}.db")

    def delete_customer(self,id):
        if os.path.exists(f"{__customer_folder__}/{id}.db"):
            os.remove(f"{__customer_folder__}/{id}.db")
            print("**",id,"deleted","**")
        else:
            print("The customer does not exist")



def create_customer(name,address,contact):
    customer = Customer()
    customer.name = name
    customer.address = address
    customer.contact = contact
    print(name)
    print(address)
    print(contact)
    customer.save()

def get_all_customers():
    customer = Customer()
    customers = customer.all_customers()
    pprint(customers)

def customer_view_by_id(id):
    customer = Customer()
    customer.id = id
    customer.get_by_id(id)
    print(customer.id, customer.name, customer.address, customer.contact)

def customer_delete(id):
    item = Customer()
    item.id = id
    item.delete_customer(id)
    