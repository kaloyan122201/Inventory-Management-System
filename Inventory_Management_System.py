import json

#showing options
def show_options():
    counter = 1
    options = [" Add"," Update"," View Inventory"," Sell"," Delete"," Search"," Check Total Amount", " Save and Exit"]
    for option in options:
        print(f"{counter}.{option}")
        counter+=1

#function for add new items
def adding(dictionary_items):
    print("To go back type 'Exit'!")
    print("Add item in format item-quantity-price")
    while True:
        name = input("\nEnter item name: ").title()
        if not all(part.isalpha() for part in name.split()):
            print("Invalid name! Please enter a valid item name (letters only).")
            continue
        elif name =="Exit":
            break
        quantity = input("Enter quantity: ")
        if quantity =="Exit":
            break
        if not quantity.isdigit():
                print("Quantity must be a positive number.")
                continue
        else:
            quantity = int(quantity)

        price = input("Enter price: ")
        if price =="Exit":
            break
        try:
            price = float(price)  # This will catch both int and float
        except ValueError:
            print("Invalid price. Please enter a numeric value.")

        if name not in dictionary_items.keys():
            dictionary_items[name] = quantity,price
        else:
            updating(name,quantity,price,dictionary_items)

#Updating items
def updating(item_name,item_quantity,item_price,items_dictionary):
    if item_name in items_dictionary.keys():
        items_dictionary[item_name] = item_quantity,item_price

#Updating existing items
def updating_existing_items(stock):
    print("Type 'Exit' to go back!")
    print("Enter item name that you want to update: ")
    while True:
        name = input("Name of the item: ").title()
        if name =="Exit":
            break
        if not all(part.isalpha() for part in name.split()):
            print("Invalid name! Please enter a valid item name (letters only).")
            continue
        try:
            new_quantity = int(input("Enter new quantity: "))
            if new_quantity <=0:
                print("Quantity should be a positive number.")
                continue
        except ValueError:
            print("Enter valid input...")
            continue
        try:
            new_price = float(input("Enter new price: "))
            if new_price <0:
                print("Price should be a positive number.")
                continue
        except ValueError :
            print("Enter valid input...")
        if name in stock.keys():
            stock[name] = new_quantity,new_quantity
            print(f"Item {name} updated successfully!")
        else:
            print(f"{name} not existing in your inventory!")

#viewing inventory
def viewing_inventory(stock):
    for name,data in stock.items():
        print(f"Name: {name}, Quantity: {data[0]}, Price: {data[1]:.2f}")

#selling items from stock
def sell_items(stock):
    print("Type 'Exit' to go back!")
    while True:
        name = input("Selling item: ").title()
        if name =="Exit":
            break
        elif not all(part.isalpha() for part in name.split()):
            print("Invalid name! Please enter a valid item name (letters only).")
            continue
        if name in stock.keys():
            quantity,price = stock[name]
            selling_amount = int(input("How many pieces you want to sell: "))
            if quantity - selling_amount <=10:
                print(f"Warning: Quantity of {name} is below 10 (Current: {quantity-selling_amount}).")
            if selling_amount > quantity:
                print("There is not enough quantity in the inventory.")
                print(f"You have {quantity} of {name} in the inventory")
                selling_amount = int(input("How many pieces you want to sell: "))
            elif selling_amount == quantity:
                ready_to_sell_everything = input(f"You are going to sell everything of {name}.\nAre you sure? (y/n): ").lower()
                if ready_to_sell_everything == "y":
                    stock[name] = quantity-selling_amount, price
                    del stock[name]
                else:
                    continue
            else:
                stock[name] = quantity - selling_amount, price
        else:
            print(f"There is no {name} inside your inventory!")
            continue

#function for deleting items if they are inside
def delete_items(stock):
    print("Type 'Exit' to go back!")
    while True:
        item = input("Enter item name you want to delete: ").title()
        if item == "Exit":
            break
        elif item.isdigit():
            print("Enter the name of the item that you want to delete from the inventory")
            continue
        if item not in stock.keys():
            print("This item is not in your inventory. Try again")
            continue
        else:
            print(f"Successfully delete item {item}")
            del stock[item]

#function for searching for items
def searching_for_item(stock):
    print("Type 'Exit' to go back!")
    while True:
        name = input("Search for: ").title()
        if name == "Exit":
            break
        if not all(part.isalpha() for part in name.split()):
            print("Invalid name! Please enter a valid item name (letters only).")
            continue
        if name in stock.keys():
            quantity,price = stock[name]

            print(f"Found {name}: Quantity: {quantity} , Price: {price}")
        else:
            print(f"{name} not found in your inventory! Try again.")
            continue

#function for saving the data entered into JSON file called inventory.json
def save_inventory(stock, filename="inventory.json"):
    try:
        with open(filename, "w") as file:
            json.dump(stock, file)
        print(f"Inventory saved to {filename}.")
    except Exception as e:
        print(f"Error saving inventory: {e}")
#function for loading this file every time we open the program to work with previous data
def load_inventory(filename="inventory.json"):
    try:
        with open(filename, "r") as file:
            stock = json.load(file)
            # Convert values from list to tuple (if needed)
            for key in stock:
                stock[key] = tuple(stock[key])
            print(f"Inventory loaded from {filename}.")
            return stock
    except FileNotFoundError:
        print("No saved inventory found. Starting with an empty one.")
        return {}
    except Exception as e:
        print(f"Error loading inventory: {e}")
        return {}

#function for checking total amount of $ of the inventory
def check_total_value(stock):
    total = 0
    for name,(quantity,price) in stock.items():
        total += quantity*price
    currency = input("Enter currency for your inventory: ")
    print(f"Total inventory value: {total:.2f}{currency}")

#option for saving the file with JSON
print("Welcome to the Inventory Management System - Clean & Tidy")
items= load_inventory()

while True:
    show_options()
    try:
        choice = int(input("\nChoose number (1-7): "))
    except ValueError:
        show_options()
        print("Enter valid number!")
        continue
    match choice:
        case 1:
            adding(items)
        case 2:
            updating_existing_items(items)
        case 3:
            viewing_inventory(items)
        case 4:
            sell_items(items)
        case 5:
            delete_items(items)
        case 6:
            searching_for_item(items)
        case 7:
            check_total_value(items)
        case 8:
            save_inventory(items)
            break
        case _:
            print("Please enter a valid number\n")
            continue