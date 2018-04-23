from random import randint, choice
from copy import copy

class Building():

    def __init__(self, num_floors, num_customers):
        self.num_floors = num_floors
        self.num_customers = num_customers
        self.customer_list = self.get_customers(self.num_customers)
        self.elevator = self.make_elevator()
        self.floors = self.make_floors(self.num_floors)

    def __str__(self):
        return 'A building with ' + str(self.num_floors) + ' floors and ' + str(self.num_customers) + ' customers in it.'

    @property
    def num_floors(self):
        return self._num_floors

    @num_floors.setter
    def num_floors(self,num_floors):
        self._num_floors = num_floors

    @property
    def num_customers(self):
        return self._num_customers

    @num_customers.setter
    def num_customers(self,num_customers):
        self._num_customers = num_customers

    @property
    def customer_list(self):
        return self._customer_list

    @customer_list.setter
    def customer_list(self,customer_list):
        self._customer_list = customer_list

    @property
    def elevator(self):
        return self._elevator

    @elevator.setter
    def elevator(self,elevator):
        self._elevator = elevator

    @property
    def floors(self):
        return self._floors

    @floors.setter
    def floors(self,floors):
        self._floors = floors

    def get_customers(self, num_customers):
        customers = []
        for customer in range(0, num_customers):
            c = Customer(self)
            print('Made customer:',c)
            customers.append(c)
        return customers

    def make_elevator(self):
        elevator = Elevator(self)
        print('Made an elevator:',elevator)
        return elevator

    def make_floors(self, num_floors):
        floornumbers = list(range(num_floors))
        print(floornumbers)
        floors = []
        for number, floor in enumerate(floornumbers):
            f = Floor(number, self)
            print('Made floor:',f)
            floors.append(f)
        return floors

class Elevator():
    def __init__(self, building):
        self.passengers = []
        self.location = 0
        self.building = building

    def __str__(self):
        return 'An elevator with ' + str(len(self.passengers)) + ' customers in it on floor ' + str(self.location)

    def go_up(self):
        for floor in self.building.floors:
            print('The lift stopped on floor ' + str(floor.number) + ' with ' + str(len(floor.customers_waiting)) + ' customers waiting.')
            dropped_off = self.drop_off_passengers(floor)
            picked_up = self.pick_up_customers(floor, 'up')
            print(str(picked_up) + ' customers got in and ' + str(dropped_off) + ' got out. The new number of passengers is ' + str(len(self.passengers)))
            print('The new status of floor ' + str(floor.number) + ' is now: ' + str(len(floor.customers_waiting)) + ' customers waiting.')

    def go_down(self):
        for floor in reversed(self.building.floors):
            print('The lift stopped on floor ' + str(floor.number) + ' with ' + str(len(floor.customers_waiting)) + ' customers waiting.')
            dropped_off = self.drop_off_passengers(floor)
            picked_up = self.pick_up_customers(floor, 'down')
            print(str(picked_up) + ' customers got in and ' + str(dropped_off) + ' got out. The new number of passengers is ' + str(len(self.passengers)))
            print('The new status of floor ' + str(floor.number) + ' is now: ' + str(len(floor.customers_waiting)) + ' customers waiting.')

    def pick_up_customers(self, floor, direction):
        # print('Picking up customers....')
        new_passengers = []
        customers_waiting = copy(floor.customers_waiting)
        for customer in customers_waiting:
            # Get new passengers based on direction
            if ((customer.location < customer.destination) and direction == 'up') or ((customer.location > customer.destination) and direction == 'down'):
                # Add the waiting customer to the passengers
                new_passengers.append(customer)
                # Remove customer from the waiting customers of the floor
                floor.customers_waiting.remove(customer)
                # As long as the customer is in the elevator put his location on None
                customer.location = None
        # Add customers to the passengers
        self.passengers.extend(new_passengers)
        return len(new_passengers)

    def drop_off_passengers(self, floor):
        # print('Dropping off customers....')
        # Get the customers that are on their on_destination
        leaving_customers = []
        passengers_before = copy(self.passengers)
        for passenger in passengers_before:
            if passenger.destination == floor.number:
                # Set the location of the passenger to the correct floor
                passenger.location = floor.number
                # Add the passenger to the customers of that floor and the leaving passengers
                floor.customers.append(passenger)
                leaving_customers.append(passenger)
                # Remove customer from the passenger list
                self.passengers.remove(passenger)
        return len(leaving_customers)


class Floor():

    def __init__(self, number, in_building):
        self.number = number
        self.customers = self.get_customers_on_location(in_building)
        self.customers_waiting = self.get_customers_waiting(in_building)

    def __str__(self):
        return 'A floor on level ' + str(self.number) + ' with ' + str(len(self.customers)) + ' customers on it of which ' + str(len(self.customers_waiting)) + ' is/are waiting'

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self,number):
        self._number = number

    @property
    def customers_waiting(self):
        return self._customers_waiting

    @customers_waiting.setter
    def customers_waiting(self,customers_waiting):
        self._customers_waiting = customers_waiting

    def get_customers_on_location(self, building):
        customers = []
        for customer in building.customer_list:
            if customer.location == self.number:
                customers.append(customer)
        return customers

    def get_customers_waiting(self, building):
        customers = []
        for customer in building.customer_list:
            if (customer.location == self.number) and (not customer.on_destination):
                customers.append(customer)
        return customers


class Customer():

    def __init__(self, in_building):
        self.in_building = in_building
        self.location = randint(0, self.in_building.num_floors-1)
        self.destination = self.find_destination(self.location, self.in_building.num_floors)
        self.on_destination = False

    def __str__(self):
        return 'A customer which is on floor ' + str(self.location) + ' with destination ' + str(self.destination)

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self,location):
        self._location = location

    @property
    def on_destination(self):
        return self._on_destination

    @on_destination.setter
    def on_destination(self,on_destination):
        self._on_destination = on_destination

    def find_destination(self, location, num_floors):
        destination = location
        while destination == location:
            destination = randint(0, num_floors-1)
        return destination
