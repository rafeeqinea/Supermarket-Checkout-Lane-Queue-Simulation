# F2 By Rares Irimescu (Student id: 00 1303304)

import random

class Customer:
    def __init__(self, id):
        # Constructor initializes a Customer with a unique ID
        self.id = id
        # Randomly assign a basket size between 1 and 30
        self.basket = random.randint(1, 30)
        # Determine if the customer gets a lottery ticket based on the basket size
        self.lottery_ticket = self.basket >= 10 and bool(random.getrandbits(1))

    def get_basket_size(self):
        # Method to get the size of the customer's basket
        return self.basket

    def checkout_time(self, till_type):
        # Calculate checkout time based on the type of checkout till
        fixed_time = 4 if till_type == 'cashier' else 6
        return self.basket * fixed_time

    def display_details(self):
        # Display customer details, including basket size, lottery status, and checkout times
        lottery_status = "wins a lottery ticket!"\
            if self.lottery_ticket \
            else "hard luck, no lottery ticket this time!"
        print(f"### Customer details ###")
        print(f"{self.id} -> items in basket: {self.basket}, {lottery_status}")
        print(f"time to process basket at cashier till: {self.checkout_time('cashier')} Secs")
        print(f"time to process basket at self-service till: {self.checkout_time('self-service')} Secs")


class SpecialCustomer(Customer):
    def checkout_time(self, till_type):
        # Override the checkout_time method for SpecialCustomer with faster times
        fixed_time = 2 if till_type == 'cashier' else 3
        return self.basket * fixed_time



customer = Customer("C1")
customer.display_details()

special_customer = SpecialCustomer("SC1")
special_customer.display_details()