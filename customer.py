from genericpath import exists
import json
import os
from pprint import pprint

__db_location__ = "db"
__customer_folder__ = f"{__db_location__}/customer"
__customer__last_id__ = f"{__db_location__}/customer_id.db"

__user_folder__ = f"{__db_location__}/user.db"

class Customer():
    def __init__(self) :
        if os.path.exists(__customer__last_id__):
            with open(__customer__last_id__, "r") as last_id_f:
                self.last_id = int(last_id_f.readline())
        else:
            self.last_id = 0

    def __repr__(self):
        return f"id:{self.id},name:{self.name},password:{self.password},address:{self.address},contact:{self.contact}"


    def __str__(self):
        return f"id:{self.id},name:{self.name},password:{self.password},address:{self.address},contact:{self.contact}"

    def save(self):
        id = self.last_id+1

        # Save database customer
        _data_ = {
            "id": id,
            "name": self.name,
            "password": self.password,
            "address": self.address,
            "contact": self.contact,
        }
        with open(f"{__customer_folder__}/{id}.db", "w") as customer_file:
            json.dump(_data_, customer_file)
            

        # Save next id
        self.last_id += 1
        with open(__customer__last_id__, "w") as f:
            f.write(str(self.last_id))

    def __get_customer_by_path(customer, path):
        
        with open(path, "r") as customer_file:
            _data_ = json.load(customer_file)
            customer.id = _data_["id"]
            customer.name = _data_["name"]
            customer.password = _data_["password"]
            customer.address = _data_["address"]
            customer.contact = _data_["contact"]
        
    def all_customers(self):
        customer_file_names = os.listdir(__customer_folder__)
        customers = []
        for customer_file_name in customer_file_names:
            customer = Customer()
            Customer.__get_customer_by_path(
                customer, f"{__customer_folder__}/{customer_file_name}")
            customers.append(customer)
        return customers

    def get_by_id(self,id):
        Customer.__get_customer_by_path(self, f"{__customer_folder__}/{id}.db")

    def delete_customer(self,id):
        if os.path.exists(f"{__customer_folder__}/{id}.db"):
            os.remove(f"{__customer_folder__}/{id}.db")
            print("**",id,"deleted","**")
        else:
            print("The customer does not exist")


    def login(self,userName,password):
        USER = "NONE"
        customers = Customer()
        cust = customers.all_customers()
        cust_tuple = tuple(cust)
        if os.path.exists(f"{__user_folder__}"):
            print("** User Allready login..! **")
            USER= "A"
        else:
            for i in range(len(cust)):
                if userName == cust_tuple[i].name and password == cust_tuple[i].password :
                    USER = cust_tuple[i].id
                    write_file(USER)
                    print("** User Loign Success..! **")
                    break
                else :
                    USER="NONE"

        if USER == "NONE":
            print("** Account does not exists..! **")

    def logout(self):
        if os.path.exists(f"{__user_folder__}"):
            os.remove(f"{__user_folder__}")
           
        else:
            print("The order does not exist")

def create_customer(name,password,address,contact):
    customer = Customer()
    customer.name = name
    customer.password = password
    customer.address = address
    customer.contact = contact
    customer.save()
    print("***User created succesfully..!***")
   

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

def login_user(name,password):
    customer = Customer()
    customer.login(name,password)

def logout():
    customer = Customer()
    customer.logout()
    print("** Customer logout success ..! **")

def write_file(id):
    with open(__user_folder__, "w") as f:
        f.write(str(id))
    