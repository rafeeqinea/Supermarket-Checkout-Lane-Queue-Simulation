import tkinter as tk
from threading import Thread
import random
from datetime import datetime
import time
import threading

class GUI:
    def __init__(self, root, supermarket):
        self.root = root
        self.supermarket = supermarket
        self.simulation_thread = None
        self.running = False

        self.root.geometry("500x200")

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.run_subfeature_button = tk.Button(self.root, text="Run Sub-Feature v", command=self.run_subfeature)
        self.run_subfeature_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit)
        self.exit_button.pack()

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.simulation_thread = Thread(target=self.supermarket.simulate_checkout, args=(60,))
            self.simulation_thread.start()


    def run_subfeature(self):
        current_time = datetime.now().strftime('%H:%M')
        print("Lane status at", current_time)
        for i, lane in enumerate(self.supermarket.lanes):
            print(f"L{i + 1}({lane.lane_type}) -> {lane.status}")
        print()

    def stop_simulation(self):
        if self.running:
            self.running = False
            self.supermarket.stop_simulation()

    def exit(self):
        self.root.destroy()

root = tk.Tk()
# Customer class from F2.py
class Customer:
    def __init__(self, id):  # Initializing a Customer with a unique ID
        self.id = id  # Each customer has an id
        self.basket = random.randint(1, 30)  # Each customer has a basket with a random number of items
        self.lottery_ticket = self.basket >= 10 and bool(random.getrandbits(1))  # Each customer may have a lottery ticket

    def checkout_time(self, till_type):  # Calculation checkout time based on the type of checkout till
        fixed_time = 4 if till_type == 'cashier' else 6
        return self.basket * fixed_time

    def display_details(self):  # Display customer of details, including basket size, lottery status, and checkout times
        lottery_status = "wins a lottery ticket!" if self.lottery_ticket else "hard luck, no lottery ticket this time!"
        print(f"### Customer details ###")
        print(f"{self.id} -> items in basket: {self.basket}, {lottery_status}")
        print(f"time to process basket at cashier till: {self.checkout_time('cashier')} Secs")
        print(f"time to process basket at self-service till: {self.checkout_time('self-service')} Secs")

# Lane class from F1.py
class Lane:
    def __init__(self, capacity, lane_type):  # Initializing a Lane with a capacity and type
        self.capacity = capacity  # Maximum number of customers in the lane
        self.customers = []  # Lane starts empty
        self.status = 'closed'  # Lane starts closed
        self.lane_type = lane_type  # Type of lane (Regular or Self-Service)

    def add_customer(self, customer):  # Adding customers to the lane if it's not full
        if len(self.customers) < self.capacity:
            self.customers.append(customer)
            self.status = 'open'
        else:
            print("Lane is full, please wait for sometime")

    def remove_customer(self):  # Removing a customer from the lane
        if self.customers:
            self.customers.pop(0)
        # If the lane is empty after removing the customer, closing the lane
        if len(self.customers) == 0:
            self.status = 'closed'

    def is_full(self):  # Checking if the lane is full
        return len(self.customers) == self.capacity

    def is_empty(self):  # Checking if the lane is empty
        return len(self.customers) == 0

# RegularLane class from F1.py
class RegularLane(Lane):
    def __init__(self):  # Constructor initializes a RegularLane with a capacity of 5
        super().__init__(5, 'Reg')  # Regular lane has a capacity of 5

# SelfServiceLane class from F1.py
class SelfServiceLane(Lane):
    def __init__(self):  # Constructor initializes a SelfServiceLane with a capacity of 15
        super().__init__(15, 'Slf')  # Self-service lane has a capacity of 15

# Supermarket class from F1.py
class Supermarket:
    def __init__(self, num_customers):  # Constructor initializes a Supermarket with a certain number of customers
        self.customers = [Customer(i+1) for i in range(num_customers)]  # Initializing the customers in the supermarket
        self.lanes = [RegularLane() for _ in range(5)] + [SelfServiceLane()]  # Initializing the lanes in the supermarket
        # Assigning each customer to a lane
        for customer in self.customers:
            self.assign_customer_to_lane(customer)
        # Initially, only two lanes are open
        self.lanes[0].status = "open"
        self.lanes[5].status = "open"

    def assign_customer_to_lane(self, customer):  # Assigning customers to lanes based on the size of their baskets
        # If the customer's basket has less than 10 items and the self-service lane is not full, assign them to the self-service lane
        if customer.basket < 10 and not self.lanes[5].is_full():
            self.lanes[5].add_customer(customer)
        else:
            # Find the regular lane with the shortest queue that is not full
            for lane in self.lanes[:5]:
                if not lane.is_full():
                    lane.add_customer(customer)
                    break

    def display_lane_status(self):  # Display the status of the lanes
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

    def generate_customers(self):  # Continuous generation of new customers
        while True:
            num_new_customers = random.randint(0, 10)
            for _ in range(num_new_customers):
                new_customer = Customer(len(self.customers) + 1)
                self.customers.append(new_customer)
                self.assign_customer_to_lane(new_customer)
            time.sleep(30)

    def simulate_checkout(self, duration):  # duration parameter added
        print("Waiting for customers...")
        self.display_lane_status()
        customer_generation_thread = threading.Thread(target=self.generate_customers)
        customer_generation_thread.start()
        start_time = datetime.now()  # record the start time
        while (datetime.now() - start_time).seconds < duration:  # check if the duration has passed
            self.display_lane_status()
            for lane in self.lanes:
                if lane.status == "open" and not lane.is_empty():
                    if lane.customers[0].basket > 0:
                        lane.customers[0].basket -= 1
                    if lane.customers[0].basket == 0:
                        lane.remove_customer()
            time.sleep(10)
        print("Simulation ended")  # print a message when the simulation ends


supermarket = Supermarket(10)
gui = GUI(root, supermarket)
root.mainloop()