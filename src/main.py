def main():
    import sqlite3

    con = sqlite3.connect("../data/burgerqueen.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    
    homePage(con, cursor)

    con.close()

def homePage(con, cursor):
    print('\n'*20)
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(input('> '))
            if valg == 1:
                loginUser(con, cursor, exceptionMessage=None)
                break
            elif valg == 2:
                createUser(con, cursor)
                break
            elif valg == 3:
                exit()
            else:
                print('Invalid value. Select option 1, 2 or 3.')
        except ValueError:
            print('Invalid input. Please enter a number.')

def redirectUserDashboard(con, cursor, username):
    cursor.execute("SELECT IsEmployee FROM Users WHERE Username = ?", (username,))
    employeeStatus = cursor.fetchone()
    if employeeStatus and employeeStatus[0] == 1:
        employeeDashboard(con, cursor, username)
    else:
        customerDashboard(con, cursor, username, 'Login successful.')


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
    print('-'*50)
    print('Your Order')
    print('-'*50)

    orderItems = order.split(",") if order else [] # split the order string using commas, into a list of items
    uniqueItems = set(orderItems) # use a set to find unique items
    for item in uniqueItems:
        print(f"{orderItems.count(item)}x {item}")
    
    print('-'*50)

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
                customerDashboard(con, cursor, username) # returns to user dashboard
                return
            else:
                print('Invalid value. Select items with 1-3, confirm with 4 or quit with 5.')
        except ValueError:
            print('Invalid input. Please enter a number.')
    
    listSelection(order)

    UserID = fetchUserID(cursor, username)[0]
    burgerIDs = fetchBurgerIDs(cursor, order)

    for burgerID in burgerIDs:
        cursor.execute("INSERT INTO Orders (UserID, BurgerID) VALUES (?, ?)", (UserID, burgerID))
        con.commit()
    customerDashboard(con, cursor, username, 'Order sent. You can always check its status on the "See order status" page.')


def showOrderStatus(con, cursor, username):
    pass


def employeeDashboard(con, cursor, username):
    pass


def customerDashboard(con, cursor, username, exceptionMessage = None):
    print('\n'*20)
    print(exceptionMessage)
    print('-' *50)
    print(f'Hello {username}! Choose an option:')
    print('[1] Order food\n[2] See order status\n[3] Log out')
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                placeOrder(con, cursor, username)
            elif choice == 2:
                showOrderStatus(cursor, username)
            elif choice == 3:
                print('\n'*10)
                print('-'*50)
                homePage(con, cursor)
            else:
                print('Invalid value. Order food with [1], See order status with [2], and Log out with [3]')
        except ValueError:
            print('Invalid input. Please enter a number.')


if __name__ == "__main__":
   main()