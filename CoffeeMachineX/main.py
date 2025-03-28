from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

my_machine_money = MoneyMachine()
my_coffee_maker = CoffeeMaker()
my_menu = Menu()
is_on = True

while is_on:
    options = my_menu.get_items()
    choice = input(f"What would you like? {options} : ")

    if choice == "off":
        is_on = False  # Exit the loop
        break  # Stop execution

    elif choice == "report":
        my_coffee_maker.report()
        my_machine_money.report()

    else:
        drink = my_menu.find_drink(choice)

        if drink is None:
            print("Invalid selection. Please choose from the menu.")
            continue  # Ask again

        # Check if enough resources
        if not my_coffee_maker.is_resource_sufficient(drink):
            print("Machine shutting down due to insufficient resources.")
            break  # Exit immediately

        # Check if payment is successful
        if not my_machine_money.make_payment(drink.cost):
            print("Transaction failed due to insufficient funds. Exiting...")
            break  # Exit immediately

        # If everything is fine, make coffee
        my_coffee_maker.make_coffee(drink)
        print(f"Here is your {drink.name}.  Enjoy!")
