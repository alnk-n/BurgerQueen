# orders.py

import auth  # imports authentication functions
import dashboards  # imports dashboard functions for user and employee dashboards


# Function to fetch the BurgerIDs corresponding to the items in the order. Returns a list of BurgerIDs
# Arguments:
# cursor: used to execute database queries
# order: a string of burger names separated by commas
def fetchBurgerIDs(cursor, order):
    burgerNamesList = order.split(',') # convert comma-separated string to list
    burgerIDs = []

    for burgerName in burgerNamesList:
        cursor.execute("SELECT BurgerID FROM Burgers WHERE Name = ?", (burgerName,)) # queries for burger ID using its corresponding name
        result = cursor.fetchone()
        
        if result:
            burgerIDs.append(str(result[0])) # if provided burger name exists in DB, return and append its ID to the list
        else:
            print(f'Burger "{burgerName}" not found in database.')
    return burgerIDs # return ID list


# Returns clean terminal confirmation output with items provided by a concatinated order string
# Arguments:
# order: string consisting of unique item names separated by a comma (e.g. "Kingdom Fries,Triple Cheesy Princess,Kingdom Fries")
def listSelection(order):
    print('\n'*20)
    print('-'*50)
    print('Your order was successfully processed!\nYou can always check its status in the "See order status" page.')
    print('-'*50)

    orderItems = order.split(",") if order else [] # split the order string using commas, into a list of items
    uniqueItems = set(orderItems) # use a set to find unique items
    for item in uniqueItems:
        print(f"{orderItems.count(item)}x {item}")


# Takes in existing order string, and concatinates new item name separated by a comma
# Arguments:
# order: string consisting of unique item names separated by a comma (e.g. "Kingdom Fries,Triple Cheesy Princess,Kingdom Fries")
# item: takes in item name and concatinates it to the order variable
def addToOrder(order, item):
    if order:
        order += "," + item # if there's already items in the order, add comma before appending new item
    else:
        order = item # first item doens't need a comma
    return order # returns the updated order variable


# Provides selection menu to customer and commits selected items as orders to database
# Arguments:
# con: used for committing orders and passing database connection along for homePage
# cursor: used to execute database queries
# username: used for identifying logged-in customer and associating their UserID with their order
# order: string consisting of unique item names separated by a comma (e.g. "Kingdom Fries,Triple Cheesy Princess,Kingdom Fries"). 
#        It's formatted like this because it's easier to directly use it in a database query.
def placeOrder(con, cursor, username, order = None):
    print('\n'*20)
    print('-' *50)
    print('Select the items you wish to add to your order.\n[Confirm with 4].')
    print('-' *50)
    
    print('[1] Whopper Queen\n[2] Triple Cheesy Princess\n[3] Kingdom Fries\n[4] Confirm order\n[5] Return')
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                order = addToOrder(order, "Whopper Queen")
                print('Added 1x Whopper Queen.')
            elif choice == 2:
                order = addToOrder(order, "Triple Cheesy Princess")
                print('Added 1x Triple Cheesy Princess.')
            elif choice == 3:
                order = addToOrder(order, "Kingdom Fries")
                print('Added 1x Kingdom Fries.')
            elif choice == 4:
                break # exit loop to confirm
            elif choice == 5:
                dashboards.customerDashboard(con, cursor, username) # returns to user dashboard
                return
            else:
                print('Invalid value. Select items with 1-3, confirm with 4 or quit with 5.')
        except ValueError:
            print('Invalid input. Please enter a number.')

    UserID = auth.fetchUserID(cursor, username)[0] # converts username to UserID
    burgerIDs = fetchBurgerIDs(cursor, order) # covnverts order string ('Kingdom Fries,Kingdom Fries') to string of IDs ('3,3')

    cursor.execute("SELECT MAX(OrderID) FROM Orders") # fetches the highest value from the OrderID column
    lastOrder = cursor.fetchone()[0]
    newOrderID = (lastOrder or 0) + 1 # adds one to the highest value and uses it for the new order

    for burgerID in burgerIDs:
        # for each item in the order, insert row with OrderID (defined above), associated UserID and burgerID
        cursor.execute("INSERT INTO Orders (OrderID, UserID, BurgerID) VALUES (?, ?, ?)", (newOrderID, UserID, burgerID))
    con.commit()

    listSelection(order) # order confirmation printout
    dashboards.customerDashboard(con, cursor, username, "nospace") # returns to customer dashboard. "nospace" argument prevents newline printout in the customerDashboard function.


def viewMyOrders(con, cursor, username):
    UserID = auth.fetchUserID(cursor, username)[0]
    cursor.execute("""
    SELECT o.OrderID, b.Name, o.IsDone
    FROM Orders o
    JOIN Burgers b ON o.BurgerID = b.BurgerID
    WHERE o.UserID = ?
    ORDER BY o.OrderID
    """, (UserID,))
    rows = cursor.fetchall()

    ordersDictionary = {}

    for OrderID, BurgerName, status in rows:
        if OrderID not in ordersDictionary:
            ordersDictionary[OrderID] = []
        ordersDictionary[OrderID].append((BurgerName, status))
    
    print('-'*50)
    print("Your orders:")
    print('-'*50)
    for OrderID, items in ordersDictionary.items():
        print(f"Order Number #{OrderID:<{10}} | Status")
        for burger_name, status in items:
            if status == 1:
                print(f"- {burger_name:<{22}} | [Done]")
            else:
                print(f"- {burger_name:<{22}} | [Preparing..]")
        print()
    print("-" * 50)
    input("(Press Enter to exit)")
    dashboards.customerDashboard(con, cursor, username)


def viewAllOrders(con, cursor, username):
    cursor.execute("""
    SELECT o.OrderID, u.Username, b.Name, o.IsDone
    FROM Orders o
    JOIN Burgers b ON o.BurgerID = b.BurgerID
    JOIN Users u ON o.UserID = u.UserID
    ORDER BY o.OrderID
    """)
    rows = cursor.fetchall()

    if not rows:
        dashboards.employeeDashboard(con, cursor, username, 'Whoops! There are no orders in the database.')

    ordersDictionary = {}

    for OrderID, User, BurgerName, status in rows:
        if OrderID not in ordersDictionary:
            ordersDictionary[OrderID] = {'User': User, 'Items': []}
        ordersDictionary[OrderID]['Items'].append((BurgerName, status))

    print('-'*50)
    print("All orders:")
    print('-'*50)
    for OrderID, items in ordersDictionary.items():
        print(f"Order Number #{OrderID:<{10}} | Status")
        print(f"Ordered by: {items['User']:<{12}} |")
        for burger_name, status in items['Items']:
            if status == 1:
                print(f"- {burger_name:<{22}} | [Done]")
            else:
                print(f"- {burger_name:<{22}} | [Preparing..]")
        print()
    print("-" * 50)
    input("(Press Enter to exit)")
    dashboards.employeeDashboard(con, cursor, username)


def viewOngoingOrders(con, cursor, username):
    cursor.execute("""
    SELECT o.OrderID, u.Username, b.Name, o.IsDone
    FROM Orders o
    JOIN Burgers b ON o.BurgerID = b.BurgerID
    JOIN Users u ON o.UserID = u.UserID
    WHERE o.IsDone = 0
    ORDER BY o.OrderID
    """)
    rows = cursor.fetchall()

    if not rows:
        dashboards.employeeDashboard(con, cursor, username, 'Phew! There are no ongoing orders.')

    ordersDictionary = {}

    for OrderID, User, BurgerName, status in rows:
        if OrderID not in ordersDictionary:
            ordersDictionary[OrderID] = {'User': User, 'Items': []}
        ordersDictionary[OrderID]['Items'].append((BurgerName, status))

    print('-'*50)
    print("Ongoing orders:")
    print('-'*50)
    for OrderID, items in ordersDictionary.items():
        print(f"Order Number #{OrderID:<{10}} | Status")
        print(f"Ordered by: {items['User']:<{12}} |")
        for burger_name, status in items['Items']:
            if status == 1:
                print(f"- {burger_name:<{22}} | [Done]")
            else:
                print(f"- {burger_name:<{22}} | [Preparing..]")
        print()
    print("-" * 50)

    print("Enter the order number to mark it as complete (or press Enter to exit):")
    choice = int(input('> '))

    if choice:
        try:
            cursor.execute("UPDATE Orders SET IsDone = 1 WHERE OrderID = ? AND IsDone = 0", (choice,))
            con.commit()
            
            cursor.execute("""
                SELECT b.Name
                FROM Orders o
                JOIN Burgers b ON o.BurgerID = b.BurgerID
                WHERE o.OrderID = ?
            """, (choice,))
            burgers = [row[0] for row in cursor.fetchall()]
            orderItems = ', '.join(burgers)

            import inventory
            inventory.updateInventory(con, cursor, orderItems)

            print('\n'*20)
            print('-'*50)
            if cursor.rowcount > 0:
                print(f"Order #{choice} has been marked as complete.")
                viewOngoingOrders(con, cursor, username)
            else:
                print(f"Order #{choice} not found or already completed.")
                
            viewOngoingOrders(con, cursor, username)

        except ValueError:
            print("Invalid input. Please enter a valid order number.")

    dashboards.employeeDashboard(con, cursor, username)