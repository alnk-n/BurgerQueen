from auth import fetchUserID
import dashboards


def fetchBurgerIDs(cursor, order):
    burgerNamesList = order.split(',')
    burgerIDs = []

    for burgerName in burgerNamesList:
        cursor.execute("SELECT BurgerID FROM Burgers WHERE Name = ?", (burgerName,))
        result = cursor.fetchone()
        
        if result:
            burgerIDs.append(str(result[0]))
        else:
            print(f'Burger "{burgerName}" not found in database.')
    return burgerIDs


def listSelection(order):
    print('\n'*20)
    print('-'*50)
    print('Your order was successfully processed!\nYou can always check its status from the "See order status" page.')
    print('-'*50)

    orderItems = order.split(",") if order else [] # split the order string using commas, into a list of items
    uniqueItems = set(orderItems) # use a set to find unique items
    for item in uniqueItems:
        print(f"{orderItems.count(item)}x {item}")


def addToOrder(order, item):
    if order:
        order += "," + item # if there's already items in the order, add comma before appending new item
    else:
        order = item # first item doens't need a comma
    return order # returns the updated order variable


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

    UserID = fetchUserID(cursor, username)[0]
    burgerIDs = fetchBurgerIDs(cursor, order)

    cursor.execute("SELECT MAX(OrderID) FROM Orders")
    lastOrder = cursor.fetchone()[0]
    newOrderID = (lastOrder or 0) + 1

    for burgerID in burgerIDs:
        cursor.execute("INSERT INTO Orders (OrderID, UserID, BurgerID) VALUES (?, ?, ?)", (newOrderID, UserID, burgerID))
    con.commit()
    
    listSelection(order)
    dashboards.customerDashboard(con, cursor, username, "nospace")


def viewMyOrders(con, cursor, username):
    pass