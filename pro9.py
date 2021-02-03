import json
import datetime


def get_last_id(dictionary):
    # to find the last id from the dictionary
    # returns the last id
    return list(dictionary.keys())[-1]


class Customer:
    customer_master_data = {}

    def cust_unique_code_generator(self):
        # to generate unique code for the customer
        # returns unique customer code
        temp_code = "CODE_0"    # for unique code structure
        customer_master_data_key_list = list(self.customer_master_data.keys())
        if len(customer_master_data_key_list) > 0:
            temp_code = customer_master_data_key_list[-1]
        index = temp_code.split('_')[-1]
        index = int(index)
        return "CUST_" + str(index + 1)

    def prepare_customer(self):
        # prepares customer data and returns it
        cust_id = self.cust_unique_code_generator()     # cust_id - customer id
        customer_name = input("Enter customer name: ")
        customer_email = input("Enter customer email: ")
        customer_phone = input("Enter customer phone: ")
        customer_address1 = input("Enter customer address1: ")
        customer_address2 = input("Enter customer address2: ")
        customer_city = input("Enter city name: ")
        customer_zipcode = input("Enter zipcode: ")
        customer_state = input("Enter state name: ")
        customer_country = input("Enter country name: ")
        return {
            cust_id: {
                'customer_name': customer_name,
                'customer_email': customer_email,
                'customer_phone': customer_phone,
                'customer_address1': customer_address1,
                'customer_address2': customer_address2,
                'customer_city': customer_city,
                'customer_zipcode': customer_zipcode,
                'customer_state': customer_state,
                'customer_country': customer_country
            }
        }

    def create_customer(self):
        customer_data = self.prepare_customer()
        self.customer_master_data.update(customer_data)
        new_customer_id = get_last_id(self.customer_master_data)
        print("--> New customer created.")
        return new_customer_id


class Product:
    product_master_data = {}

    def product_unique_code_generator(self):
        # to generate unique code for the product
        temp_code = "CODE_0"    # for unique code structure
        product_master_data_key_list = list(self.product_master_data.keys())
        if len(product_master_data_key_list) > 0:
            temp_code = product_master_data_key_list[-1]
        index = temp_code.split('_')[-1]
        index = int(index)
        return "PRD_" + str(index + 1)

    def product_type_list(self):
        while True:
            print(":List of product type:")
            print("[1] Stockable")
            print("[2] Consumable")
            print("[3] Service")
            s = int(input("Select: "))
            if s == 1:
                return "Stockable"
            elif s == 2:
                return "Consumable"
            elif s == 3:
                return "Service"
            print("--> Invalid choice, try again.")

    def prepare_product(self):
        # gather product data
        sku = self.product_unique_code_generator()
        product_name = input("Enter product name: ")
        product_unit_price = float(input("Enter product unit price: "))
        product_cost = float(input("Enter product cost: "))
        product_stock = int(input("Enter product stock: "))
        product_type = self.product_type_list()
        return {
            sku: {
                'product_name': product_name,
                'product_unit_price': product_unit_price,
                'product_cost': product_cost,
                'product_type': product_type,
                'product_stock': product_stock
            }
        }

    def create_product(self):
        product_data = self.prepare_product()
        self.product_master_data.update(product_data)       # putting all data into product master
        new_product_id = get_last_id(self.product_master_data)
        print("--> New product created.")
        return new_product_id

    def show_product_list(self):
        # returns product id and qty
        while True:
            srno = 0     # for serial no.
            print("<<Available products>>")
            print("SRNO.  PRODUCT_ID  PRODUCT_NAME  PRODUCT_STOCK")
            for product_id, dict_val in self.product_master_data.items():
                srno += 1
                print(srno, "     ", product_id, "      ", dict_val.get('product_name'), "       ", dict_val.get('product_stock'))

            product_id = input("Enter product id: ")
            if product_id in self.product_master_data:
                product_qty = int(input("Enter product qty: "))
                return product_id, product_qty

            print("--> Invalid product id, try again.")

    def update_stock(self):
        # to update the stock changes
        while True:
            product_id, product_qty = self.show_product_list()
            if product_id in self.product_master_data:
                old_stock = self.product_master_data[product_id].get('product_stock')
                self.product_master_data[product_id].update({
                    'product_stock': (old_stock + product_qty)
                })
                print("--> {qty_to_add} quantity added".format(qty_to_add=product_qty))
                break

            print("--> Invalid product id, please try again.")


class SaleOrder(Product, Customer):
    sale_order_master_data = {}

    def so_unique_code_generator(self):
        # returns - unique sale order
        temp_code = "CODE_0"    # for unique code structure
        sale_order_master_data_key_list = list(self.sale_order_master_data.keys())
        if len(sale_order_master_data_key_list) > 0:
            temp_code = sale_order_master_data_key_list[-1]
        index = temp_code.split('_')[-1]
        index = int(index)
        return "SO_" + str(index + 1)

    def get_product_unit_price(self, product_id):
        # returns - product unit price
        product_unit_price = self.product_master_data[product_id]['product_unit_price']
        return product_unit_price

    def customer_list(self):
        # returns customer id
        # to display existed customer list
        while True:
            srno = 0
            print("<<Available customers>>")
            print("SRNO.  CUSTOMER_ID  CUSTOMER_NAME")
            for customer_id, dict_val in self.customer_master_data.items():
                srno += 1
                print(srno, "     ", customer_id, "      ", dict_val.get('customer_name'))

            customer_id = input("Enter customer id: ")
            if customer_id in self.customer_master_data:
                return customer_id

            print("--> Invalid customer id, try again.")

    def update_product_master_data(self, product_id, product_qty):
        # returns -
        # to update the master data of the product
        available_stock = self.product_master_data[product_id]['product_stock']
        if available_stock > product_qty:
            self.product_master_data[product_id].update({
                'product_stock': (available_stock - product_qty)
            })
        elif available_stock == product_qty:
            del self.product_master_data[product_id]
        else:
            print("--> Product stock is not enough")

    def prepare_sale_order(self):
        # prepares and returns sale product data which is to be created
        so_id = self.so_unique_code_generator()
        customer_id = self.customer_list()
        total_of_subtotal = 0       # to store the total of subtotal
        sale_product_data = {
            so_id: {
                'cust_code': customer_id,
                'order_date': str(datetime.date.today()),
                'order_line': [],
                'total': 0,
                'state': 'Draft'
            }
        }

        while True:
            product_id, product_qty = self.show_product_list()
            product_unit_price = self.get_product_unit_price(product_id)
            subtotal = product_qty * product_unit_price
            total_of_subtotal += subtotal

            if len(sale_product_data[so_id]['order_line']) == 0:
                sale_product_data[so_id]['order_line'].append({
                    'product_id': product_id,
                    'product_qty': product_qty,
                    'product_unit_price': product_unit_price,
                    'product_subtotal': subtotal,
                    'state': 'Draft'
                })
                self.update_product_master_data(product_id, product_qty)
            else:
                for index in range(len(sale_product_data[so_id]['order_line'])):
                    if product_id != sale_product_data[so_id]['order_line'][index].get('product_id'):
                        sale_product_data[so_id]['order_line'].append({
                            'product_id': product_id,
                            'product_qty': product_qty,
                            'product_unit_price': product_unit_price,
                            'product_subtotal': subtotal,
                            'state': 'Draft'
                        })
                        break
                    else:
                        # fetching old data and doing required process to update the old data
                        old_qty = sale_product_data[so_id]['order_line'][index].get('product_qty')
                        new_qty = old_qty + product_qty
                        new_subtotal = new_qty * product_unit_price
                        sale_product_data[so_id]['order_line'][index].update({
                            'product_qty': new_qty,
                            'product_subtotal': new_subtotal
                        })
                        break
                self.update_product_master_data(product_id, product_qty)
            c = input("Do you want to add more (y/n): ")
            if c == 'n':
                break
        sale_product_data[so_id].update({'total': total_of_subtotal})
        return sale_product_data

    def create_sale_order(self):
        sale_order_data = self.prepare_sale_order()
        self.sale_order_master_data.update(sale_order_data)
        last_id = get_last_id(self.sale_order_master_data)
        return last_id

    def get_customer_details(self, order_id):
        # returns customer id and customer info like name and address
        cust_id = self.sale_order_master_data[order_id].get('cust_code')
        return {
            'cust_code': cust_id,
            'cust_info': self.customer_master_data[cust_id]
        }

    def show_sale_order_list(self):
        # displays sale order list and returns selected order id
        while True:
            srno = 0
            print("<<Available sale orders>>")
            print("SRNO.  ORDER_ID  CUSTOMER_NAME  STATE")
            print("--------------------------------------")
            for order_id, dict_val in self.sale_order_master_data.items():
                srno += 1
                customer_name = self.customer_master_data[dict_val.get('cust_code')].get('customer_name')
                print(srno, "     ", order_id, "     ", customer_name, "      ", dict_val.get('state'))

            order_id = input("Enter order id: ")
            if order_id in self.sale_order_master_data:
                return order_id

            print("--> Invalid order id, try again.")

    def display_sale_order(self):
        # to display selected sale order info in proper format
        order_id = self.show_sale_order_list()
        customer_details = self.get_customer_details(order_id)
        order_date = self.sale_order_master_data[order_id].get('order_date')
        print("Order No: {order_id:<28} Order Date: {order_date}".format(order_id=order_id, order_date=order_date))
        print("Order Status: {status}".format(status=self.sale_order_master_data[order_id].get('status')))
        print("Customer:", customer_details['cust_code'], end=", ")
        print(customer_details['cust_info']['customer_name'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_address1'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_address2'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_city'], ",", customer_details['cust_info']['customer_state'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_zipcode'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_country'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_phone'])
        print("{space:>8}".format(space=""), customer_details['cust_info']['customer_email'])
        print("")
        print("PRODUCT NAME     PRODUCT_PRICE     PRODUCT_QTY     SUBTOTAL")
        print("=============================================================")

        for dict_val in self.sale_order_master_data[order_id]['order_line']:
            product_id = dict_val['product_id']
            print("{product_name:<20}".format(product_name=self.product_master_data[product_id].get('product_name')), end="")
            print("{unit_price:<20}".format(unit_price=dict_val['product_unit_price']), end="")
            print("{product_qty:<12}".format(product_qty=dict_val['product_qty']), end="")
            print("{product_subtotal}".format(product_subtotal=dict_val['product_subtotal']))
            print("")
        print("{space:>40}Total order: {order_total}".format(order_total=self.sale_order_master_data[order_id]['total'], space=""))

    def show_state_info(self):
        # to display order details like order id, customer name and order state
        # returns order state and order id
        order_id = self.show_sale_order_list()
        return order_id

    def confirm_order(self, order_state, order_id):
        # sets the ordered product state and order state to confirm
        # returns -
        if order_state == 'Draft':
            for each_product in self.sale_order_master_data[order_id]['order_line']:
                each_product.update({'state': 'Confirm'})

            self.sale_order_master_data[order_id].update({'state': 'Confirm'})
            print("--> Order state changed: Draft -> Confirm ")
        elif order_state == 'Confirm':
            print("--> Already in 'Confirm' state.")
        elif order_state == 'Cancel':
            print("--> State must be 'Draft' to Confirm.")
        else:
            print("--> Can not modify 'Done' state.")

    def cancel_order(self, order_state, order_id):
        # sets the ordered product state and order state to cancel and revert the product qty
        # returns -
        if order_state == 'Draft' or order_state == 'Confirm':
            for each_product in self.sale_order_master_data[order_id]['order_line']:
                each_product.update({'state': 'Cancel'})
                # below lines are to restore the product qty
                product_id = each_product.get('product_id')
                product_qty = each_product.get('product_qty')
                old_product_qty = self.product_master_data[product_id].get('product_stock')
                self.product_master_data[product_id].update({'product_stock': (old_product_qty + product_qty)})

            self.sale_order_master_data[order_id].update({'state': 'Cancel'})
            print("--> Order state changed: {current_state} -> Cancel".format(current_state=order_state))
        elif order_state == 'Cancel':
            print("--> Already in 'Cancel' state.")
        else:
            print("--> Can not modify 'Done' state.")

    def set_to_draft(self, order_state, order_id):
        # sets the ordered product state and order state to draft
        # returns -
        if order_state == 'Confirm' or order_state == 'Cancel':
            for each_product in self.sale_order_master_data[order_id]['order_line']:
                each_product.update({'state': 'Draft'})
                # below lines are to deduct the product qty as per the qty available in the order line
                product_id = each_product.get('product_id')
                product_qty = each_product.get('product_qty')
                old_product_qty = self.product_master_data[product_id].get('product_stock')
                self.product_master_data[product_id].update({'product_stock': (old_product_qty - product_qty)})

            self.sale_order_master_data[order_id].update({'state': 'Draft'})
            print("--> Order state changed: {current_state} -> Draft".format(current_state=order_state))
        elif order_state == 'Draft':
            print("--> Already in 'Draft' state.")
        else:
            print("--> Can not modify 'Done' state.")

    def set_to_done(self, order_state, order_id):
        # sets the ordered product state and order state to done
        # returns -
        if order_state == 'Confirm':
            for each_product in self.sale_order_master_data[order_id]['order_line']:
                each_product.update({'state': 'Done'})

            self.sale_order_master_data[order_id].update({'state': 'Done'})
            print("--> Order state changed: {current_state} -> Done".format(current_state=order_state))
        elif order_state == 'Cancel' or order_state == 'Draft':
            print("--> State must be 'Confirm' to 'Done'.")
        else:
            print("--> Can not modify 'Done' state.")

    def change_order_state(self):
        # allows to change order state if possible
        # returns -
        order_id = self.show_state_info()
        while True:
            print("[1] Confirm Order")
            print("[2] Cancel Order")
            print("[3] Set to Draft")
            print("[4] Set to Done")
            print("[5] Go Back")
            n = int(input("Select: "))

            if n == 1:
                order_state = self.sale_order_master_data[order_id].get('state')
                self.confirm_order(order_state, order_id)
            elif n == 2:
                order_state = self.sale_order_master_data[order_id].get('state')
                self.cancel_order(order_state, order_id)
            elif n == 3:
                order_state = self.sale_order_master_data[order_id].get('state')
                self.set_to_draft(order_state, order_id)
            elif n == 4:
                order_state = self.sale_order_master_data[order_id].get('state')
                self.set_to_done(order_state, order_id)
            elif n == 5:
                break
            else:
                print("--> Invalid choice, try again.")

    def prepared_order_lines(self):
        # to display all products from order line
        # returns -
        order_id = self.show_sale_order_list()
        for order_line in self.sale_order_master_data[order_id]['order_line']:
            print(json.dumps(order_line, indent=2))


sale_order = SaleOrder()

while True:
    print("[1] Create product")
    print("[2] Update stock")
    print("[3] Create customer")
    print("[4] Create sales order")
    print("[5] Change order state")
    print("[6] Display sales order")
    print("[7] Display all products")
    print("[8] Display all customers")
    print("[9] Display all sale orders")
    print("[10] Display prepared order lines")
    print("[0] Exit")
    ch = int(input("Select:"))
    if ch == 1:
        sale_order.create_product()
    elif ch == 2:
        sale_order.update_stock()
    elif ch == 3:
        sale_order.create_customer()
    elif ch == 4:
        sale_order.create_sale_order()
    elif ch == 5:
        sale_order.change_order_state()
    elif ch == 6:
        sale_order.display_sale_order()
    elif ch == 7:
        print(json.dumps(sale_order.product_master_data, indent=2))
    elif ch == 8:
        print(json.dumps(sale_order.customer_master_data, indent=2))
    elif ch == 9:
        print(json.dumps(sale_order.sale_order_master_data, indent=2))
    elif ch == 10:
        sale_order.prepared_order_lines()
    elif ch == 0:
        exit()
    else:
        print("--> Invalid choice, try again.")
