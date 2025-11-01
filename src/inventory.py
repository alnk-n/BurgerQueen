# inventory.py


# When an order is marked as complete by an employee, this takes that order, and subtracts its used ingredient amount from the inventory.
# Arguments:
# con: passing along to eventually be re-used in homePage() function
# cursor: used for executing database queries
# order: string with all items in an order separated by commas provided by the orders.py viewOngoingOrders() function
def updateInventory(con, cursor, order):
    items = order.split(',') if order else [] # split the order string into a list of items, or use an empty list if order is empty

    for item in items:
        item = item.strip() # remove leading/trailing whitespace
        
        # for each burger, fetch its ID and store as temporary "burgerID" variable
        cursor.execute("SELECT BurgerID FROM Burgers WHERE Name = ?", (item,))
        burger = cursor.fetchone()
        if not burger:
            print(f'Burger "{item}" not found.')
            continue
        burgerID = burger[0]

        # use BurgerID to find that burger's used ingredients and amount of each ingredient
        cursor.execute("SELECT IngredientID, Quantity FROM BurgerRecipes WHERE BurgerID = ?", (burgerID,))
        ingredients = cursor.fetchall()

        # subtract said ingredients from stock
        for ingredientID, amount in ingredients:
            cursor.execute("UPDATE Ingredients SET AmountInStock = AmountInStock - ? WHERE IngredientID = ?", (amount, ingredientID))

    con.commit()

# Lists name and quantity of each ingredient in inventory
# Arguments:
# con: passing along to eventually be re-used in homePage() function
# cursor: used for executing database queries
# username: used for passing logged-in user's username back to the employee dashboard
def viewInventory(con, cursor, username):
    cursor.execute("SELECT IngredientName, AmountInStock FROM Ingredients")
    rows = cursor.fetchall()

    if not rows:
        print("No ingredients found in inventory.")
        return

    ingredientsDictionary = {} # use dictionary to store ingredientName as key and amount as value

    for IngredientName, AmountInStock in rows:
        ingredientsDictionary[IngredientName] = AmountInStock # set keys and their values

    # print out ingredient inventory
    print('\n'*20)
    print('-' * 50)
    print("Current Inventory:")
    print('-' * 50)
    for ingredient, amount in ingredientsDictionary.items():
        print(f"{ingredient:<{30}} | x {amount}")
    print('-' * 50)
    input("(press Enter to exit)") # waits until user presses Enter
    import dashboards
    dashboards.employeeDashboard(con, cursor, username)