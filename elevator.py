from building import Building, Customer, Elevator

while True:
    num_floors = input("Please give the number of floors:")
    num_customers = input("Please give the number of customers:")
    try:
        floors = int(num_floors)
        customers = int(num_customers)
    except ValueError:
        print("You didn't enter a valid number")
        continue

    if floors <= 0:
        print("Please enter a number of floors that is above 0")
        continue
    if customers <= 0:
        print("Please enter a number of customers that is above 0")
        continue

    b = Building(floors, customers)
    print('Made a building with customers',b)
    b.elevator.go_up()
    b.elevator.go_down()
    break
