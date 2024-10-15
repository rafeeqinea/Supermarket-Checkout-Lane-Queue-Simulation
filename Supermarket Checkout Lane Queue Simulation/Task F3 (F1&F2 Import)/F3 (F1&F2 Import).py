# Importing necessary libraries
import random
from datetime import datetime
import time
import threading

# Importing necessary classes from F1.py and F2.py
from F1 import Lane, RegularLane, SelfServiceLane, Supermarket
from F2 import Customer

# Supermarket class from F1.py
class Supermarket(Supermarket):
    def __init__(self, num_customers):  # Constructor initializes a Supermarket with a certain number of customers
        self.customers = [Customer(i+1) for i in range(num_customers)]  # Initializing the customers in the supermarket
        self.lanes = [RegularLane() for _ in range(5)] + [SelfServiceLane()]  # Initializing the lanes in the supermarket
        # Assigning each customer to a lane
        for customer in self.customers:
            self.assign_customer_to_lane(customer)
        # Initially, only two lanes are open
        self.lanes[0].status = "open"
        self.lanes[5].status = "open"

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
        # Display details for each customer after the simulation ends
        for customer in self.customers:
            customer.display_details()

# Creating a supermarket with 10 customers and starting the simulation for 60 seconds
supermarket = Supermarket(10)
supermarket.simulate_checkout(30)