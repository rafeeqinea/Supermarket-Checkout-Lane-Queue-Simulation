# F1 By Mohammed Rafeeq Faraaz Shaik (Student id: 00 1306025)
# Importing necessary libraries
import random
from datetime import datetime
import time
import threading

# Product class
class Product:
    def __init__(self, name):
        self.name = name  # Each product has a name

# Basket class
class Basket:
    def __init__(self):
        self.products = []  # Basket starts empty

    def add_product(self, product):
        self.products.append(product)  # Adds a product to the basket

# Customer class
class Customer:
    def __init__(self, id):
        self.id = id  # Each customer has an id
        self.basket = Basket()  # Each customer has a basket

    def add_product_to_basket(self, product):
        self.basket.add_product(product)  # Adds a product to the customer's basket

# Lane class
class Lane:
    def __init__(self, capacity, lane_type, num_tills):
        self.customers = []  # Lane starts empty
        self.capacity = capacity  # Maximum number of customers in the lane
        self.status = "closed"  # Lane starts closed
        self.lane_type = lane_type  # Type of lane (Regular or Self-Service)
        self.num_tills = num_tills  # Number of tills in the lane

    def add_customer(self, customer):
        # Adding customers to the lane if it's not full
        if len(self.customers) < self.capacity:
            self.customers.append(customer)
            self.status = "open"
        else:
            print("Lane is full, please wait for sometime")

    def remove_customer(self):
        # Removing a customer from the lane
        if self.customers:
            self.customers.pop(0)
        # If the lane is empty after removing the customer, closing the lane
        if len(self.customers) == 0:
            self.status = "closed"

    def is_full(self):
        # Checking if the lane is full
        return len(self.customers) == self.capacity

    def is_empty(self):
        # Checking if the lane is empty
        return len(self.customers) == 0

# RegularLane class, inheriting from  Lane class
class RegularLane(Lane):
    def __init__(self):
        super().__init__(5, "Reg", 1)  # Capacity and Number of tills for the Regular Lane

# SelfServiceLane class, inheriting from the Lane class
class SelfServiceLane(Lane):
    def __init__(self):
        super().__init__(15, "Slf", 8)  # Self-service lane has a capacity of 15 and 8 tills

# Supermarket class
class Supermarket:
    def __init__(self, num_customers):
        # Initializing the supermarket with a certain number of customers
        self.customers = [Customer(i+1) for i in range(num_customers)]
        # Initializing the lanes in the supermarket
        self.lanes = [RegularLane() for _ in range(5)] + [SelfServiceLane()]
        # Initializing the products in the supermarket
        self.products = [Product(f"Product {i}") for i in range(100)]
        # Assigning each customer to a lane and assigning products to each customer
        for customer in self.customers:
            self.assign_customer_to_lane(customer)
            self.assign_products_to_customer(customer)
        # Initially, only two lanes are open
        self.lanes[0].status = "open"
        self.lanes[5].status = "open"

    def assign_products_to_customer(self, customer):
        # Assigning a random number of products to a customer
        num_products = random.randint(1, 30)
        for _ in range(num_products):
            product = random.choice(self.products)
            customer.add_product_to_basket(product)

    def assign_customer_to_lane(self, customer):
        # If the customer's basket has less than 10 items and the self-service lane is not full, assign them to the self-service lane
        if len(customer.basket.products) < 10 and not self.lanes[5].is_full():
            self.lanes[5].add_customer(customer)
        else:
            # Find the regular lane with the shortest queue that is not full using a lambda function
            not_full_lane = next((lane for lane in sorted(self.lanes[:5], key=lambda x: len(x.customers)) if not lane.is_full()), None)
            if not_full_lane:
                not_full_lane.add_customer(customer)

    def manage_lanes(self):
        # Opening a new lane if all open lanes are full
        if all(lane.is_full() for lane in self.lanes if lane.status == "open"):
            for lane in self.lanes:
                if lane.status == "closed":
                    lane.status = "open"
                    break
        # Closing a lane if it's empty and there's more than two lanes open
        elif sum(lane.status == "open" for lane in self.lanes) > 2:
            for lane in self.lanes:
                if lane.is_empty():
                    lane.status = "closed"
                    break
        # Redistribute customers from self-service lane to regular lanes if they are not full
        else:
            self_service_lane = self.lanes[5]
            regular_lanes = self.lanes[:5]
            for customer in self_service_lane.customers[:]:
                for lane in regular_lanes:
                    if not lane.is_full():
                        lane.add_customer(customer)
                        self_service_lane.remove_customer()
                        break
    def display_lane_status(self):
        current_time = datetime.now().strftime('%H:%M')
        print("Lane status at", current_time)
        total_customers = sum(len(lane.customers) for lane in self.lanes)
        print(f"Total number of customers waiting to check out at {current_time} is: {total_customers}")
        for i, lane in enumerate(self.lanes):
            if lane.status == "closed":
                print(f"L{i + 1}({lane.lane_type}) -> closed")
            else:
                customer_ids = ' '.join([f"C{customer.id}" for customer in lane.customers])
                print(f"L{i + 1}({lane.lane_type}) -> {customer_ids}")
        print()

    def generate_customers(self):
        # Continuous generate of new customers
        while True:
            num_new_customers = random.randint(0, 10)  # Generates a number between 1 and 10 (customers
            for _ in range(num_new_customers):
                new_customer = Customer(len(self.customers) + 1)
                self.customers.append(new_customer)
                self.assign_customer_to_lane(new_customer)
                self.assign_products_to_customer(new_customer)
            time.sleep(30) # New customers are generated every 30 seconds

    def simulate_checkout(self):
        # Simulating the checkout process
        customer_generation_thread = threading.Thread(target=self.generate_customers)
        customer_generation_thread.start()
        while True:
            self.manage_lanes()
            self.display_lane_status()
            for lane in self.lanes:
                if lane.status == "open" and not lane.is_empty():
                    if len(lane.customers[0].basket.products) > 0:
                        lane.customers[0].basket.products.pop(0)
                    if len(lane.customers[0].basket.products) == 0:
                        lane.remove_customer()
            time.sleep(1)

# Creating a supermarket with 10 customers and starting the simulation
supermarket = Supermarket(10)
supermarket.simulate_checkout()