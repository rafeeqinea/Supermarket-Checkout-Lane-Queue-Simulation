# Supermarket Checkout Lane Queue Simulation

A discrete-event simulation of a supermarket checkout system, built in Python. The project models customer arrivals, basket sizes, lane assignment logic, dynamic lane management, and timed checkout processing across multiple regular and self-service lanes. A Tkinter GUI is included for interactive control of the simulation.

This project was developed as part of an undergraduate coursework assignment, demonstrating object-oriented programming, inheritance, multithreading, and modular software design.

---

## Table of Contents

- [Features](#features)
- [Architecture and File Structure](#architecture-and-file-structure)
- [Class Design](#class-design)
- [How It Works](#how-it-works)
- [How to Run](#how-to-run)
- [Example Output](#example-output)
- [Requirements](#requirements)

---

## Features

- **Multiple lane types**: 5 regular checkout lanes (capacity 5 customers each, 1 till) and 1 self-service lane (capacity 15 customers, 8 tills).
- **Intelligent lane assignment**: Customers with fewer than 10 items are routed to self-service; others are assigned to the shortest available regular lane.
- **Dynamic lane management**: Lanes open automatically when all open lanes are full, and close when empty (maintaining a minimum of 2 open lanes). Customers can be redistributed from the self-service lane to regular lanes when capacity is available.
- **Continuous customer generation**: A background thread generates new customers at 30-second intervals, simulating real-world foot traffic.
- **Checkout time modelling**: Processing time varies by till type -- cashier tills process at 4 seconds per item, self-service tills at 6 seconds per item. A `SpecialCustomer` subclass models priority customers with halved processing times.
- **Lottery ticket system**: Customers with 10 or more items have a random chance of winning a lottery ticket.
- **Product-level basket modelling**: The extended version (F1) tracks individual `Product` objects within a `Basket`, rather than a simple item count.
- **GUI interface**: A Tkinter-based GUI provides Start, Stop, lane status query, and Exit controls.
- **Modular, incremental development**: The codebase is structured across progressive task stages (F1, F2, F3), culminating in a fully integrated simulation.

---

## Architecture and File Structure

```
Supermarket Checkout Lane Queue Simulation/
|
|-- Logbook Task 1/
|   |-- Logbook Task1 001306025.py      # Integrated standalone version with GUI
|
|-- Task F1/
|   |-- F1.py                           # Lane infrastructure and supermarket simulation
|
|-- Task F2/
|   |-- F2.py                           # Customer modelling with checkout time and lottery
|
|-- Task F3 (F1&F2 Import)/
|   |-- F1.py                           # Lane infrastructure module (importable)
|   |-- F2.py                           # Customer module (importable)
|   |-- F3 (F1&F2 Import).py           # Integrated simulation importing F1 and F2
|
|-- Supermarket Checkout lane Quese Simulation/
|   |-- F3.py                           # Final standalone simulation (all classes unified)
```

**Task F1** -- Defines the core infrastructure: `Product`, `Basket`, `Customer`, `Lane`, `RegularLane`, `SelfServiceLane`, and `Supermarket` classes. Implements lane management, product assignment, customer generation, and the main simulation loop.

**Task F2** -- Defines the `Customer` class with basket size, checkout time calculation (parameterised by till type), lottery ticket logic, and a `SpecialCustomer` subclass with faster checkout times.

**Task F3** -- Integrates F1 and F2 via Python imports, combining the lane infrastructure from F1 with the enhanced customer model from F2. Adds a configurable simulation duration and post-simulation customer detail reporting.

**Logbook Task 1** -- A self-contained version that includes all classes (Customer, Lane, RegularLane, SelfServiceLane, Supermarket) together with a Tkinter GUI for interactive simulation control.

---

## Class Design

| Class | Responsibility |
|---|---|
| `Product` | Represents a single product with a name attribute. |
| `Basket` | Holds a list of `Product` objects; supports adding products. |
| `Customer` | Holds an ID, a basket (items or `Basket` object), lottery ticket status, and checkout time calculation. |
| `SpecialCustomer` | Extends `Customer` with halved checkout processing times. |
| `Lane` | Base class for checkout lanes; manages a FIFO queue of customers with capacity limits and open/closed status. |
| `RegularLane` | Inherits from `Lane`; capacity of 5, 1 till per lane. |
| `SelfServiceLane` | Inherits from `Lane`; capacity of 15, 8 tills per lane. |
| `Supermarket` | Orchestrates the full simulation: initialises customers and lanes, assigns customers to lanes, manages lane opening/closing, generates new customers on a background thread, and runs the checkout loop. |
| `GUI` | Tkinter interface providing Start, Stop, Sub-Feature (lane status query), and Exit buttons. |

The design makes use of **inheritance** (`RegularLane` and `SelfServiceLane` extend `Lane`; `SpecialCustomer` extends `Customer`), **encapsulation** (each class manages its own state), and **polymorphism** (overridden `checkout_time` in `SpecialCustomer`).

---

## How It Works

1. **Initialisation**: The `Supermarket` is created with a configurable number of customers (default 10). Each customer is assigned a random basket of 1--30 items. Six lanes are created: 5 regular lanes and 1 self-service lane. Two lanes are opened initially.

2. **Lane assignment**: Customers with fewer than 10 items are directed to the self-service lane (if not full). Others are placed in the shortest non-full regular lane.

3. **Simulation loop**: On each tick (every 10 seconds of real time by default):
   - Lane statuses are printed, showing which customers are in each lane.
   - The first customer in each open lane has one item processed (removed from their basket).
   - When a customer's basket is empty, they are removed from the lane.
   - If a lane becomes empty, it is closed (provided at least 2 lanes remain open).

4. **Customer generation**: A background thread creates 0--10 new customers every 30 seconds, simulating ongoing foot traffic.

5. **Lane management** (in the F1 extended version): If all open lanes are full, a closed lane is opened. If lanes are underutilised, empty lanes are closed. Customers may be redistributed from the self-service lane to regular lanes when space is available.

6. **Termination**: In the time-limited versions (F3, Logbook Task 1), the simulation runs for a specified duration (default 30--60 seconds), then prints a summary of all customer details including basket sizes, lottery ticket status, and checkout times.

---

## How to Run

**Prerequisites**: Python 3.6 or later. No external dependencies are required (the project uses only the Python standard library: `tkinter`, `random`, `datetime`, `time`, `threading`).

### Running the standalone simulation (no GUI)

```bash
cd "Supermarket Checkout Lane Queue Simulation/Supermarket Checkout lane Quese Simulation"
python F3.py
```

This runs a self-contained 30-second simulation, printing lane statuses to the console every 10 seconds, followed by individual customer details.

### Running the modular version (F1 + F2 imported into F3)

```bash
cd "Supermarket Checkout Lane Queue Simulation/Task F3 (F1&F2 Import)"
python "F3 (F1&F2 Import).py"
```

This version imports the lane infrastructure from `F1.py` and the customer model from `F2.py`, then runs a 30-second simulation with post-run customer detail reporting.

### Running the GUI version

```bash
cd "Supermarket Checkout Lane Queue Simulation/Logbook Task 1"
python "Logbook Task1 001306025.py"
```

This opens a Tkinter window with four buttons:
- **Start Simulation** -- begins the 60-second checkout simulation in a background thread.
- **Run Sub-Feature v** -- prints the current open/closed status of all lanes to the console.
- **Stop Simulation** -- halts the running simulation.
- **Exit** -- closes the application.

### Running individual modules

```bash
# Run lane simulation only (continuous, Ctrl+C to stop)
cd "Supermarket Checkout Lane Queue Simulation/Task F1"
python F1.py

# Run customer model demonstration
cd "Supermarket Checkout Lane Queue Simulation/Task F2"
python F2.py
```

---

## Example Output

### Lane status display (printed every 10 seconds during simulation)

```
Lane status at 14:32
Total number of customers waiting to check out at 14:32 is: 10
L1(Reg) -> C3 C7
L2(Reg) -> closed
L3(Reg) -> closed
L4(Reg) -> closed
L5(Reg) -> closed
L6(Slf) -> C1 C2 C4 C5 C6 C8 C9 C10
```

### Customer details (printed after simulation ends)

```
### Customer details ###
C1 -> items in basket: 7, hard luck, no lottery ticket this time!
time to process basket at cashier till: 28 Secs
time to process basket at self-service till: 42 Secs

### Customer details ###
C2 -> items in basket: 23, wins a lottery ticket!
time to process basket at cashier till: 92 Secs
time to process basket at self-service till: 138 Secs
```

---

## Requirements

- Python 3.6+
- Tkinter (included in standard Python distributions; on some Linux systems, install via `sudo apt-get install python3-tk`)
- No external packages required
