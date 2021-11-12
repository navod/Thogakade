**Login method**

###### mehod name : login_user(\*params)

When users type this command from the terminal, this method checks if the user has already login or not. If the user didn't log in print a message to log in. After login customer creates a user.db file in db folder with customer id.

------------


**Create customer Account method**

###### method name : create_customer(\*params)

If we need a customer account we can use this method. When we use this method creating a customer's file with their input details from user id in the db folder.

------------


**Order place method**

###### method name : place_order(\*params)

When we use this method, the following methods also work.

**1. check_qty(item_id,qty)**
_First, it checks how much from this itemId is present. Order will not be accepted if there is not enough material for the order. If there is enough quantity, the following methods will execute:_

**2. save_order()**
_Save a file from order id._

**3. place_order_details(order.last_id,order.customer_id,itemId,qty,is_qty_available[1])**

_Following methods are execute by this method :_

1. update_qty(items,qty)

   The quantity is updated when the user places an order.

2. save_order_details()
   After changing the quantity, the order details are described by the order ID in the order in the file.

The customer place order is displayed as pending. Once the owner completes the order, it changes the as done.

------------

**Order view method**

Orders can be viewed in two main ways.

1. Customer view orders
Customer can view only their orders. (from order id or all orders)

2. Admin view orders
Admin can view all customers orders.

------------


**Order delete method**
Customers can delete their orders. After deleting the customer's orders quantity will be updated in the item file.
