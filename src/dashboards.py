# dashboards.py
import orders


def homePage(con, cursor):

    import auth

    print('\n'*20)
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(input('> '))
            if valg == 1:
                auth.loginUser(con, cursor, exceptionMessage=None)
                break
            elif valg == 2:
                auth.createUser(con, cursor)
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


def employeeDashboard(con, cursor, username, exceptionMessage = None):
    print('\n'*20)
    if exceptionMessage:
        print(exceptionMessage)
    print('-' *50)
    print(f'Hello {username}! Choose an option:')
    print('[1] View ongoing orders\n[2] View all orders\n[3] See ingredient inventory\n[4] Log out')
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                orders.viewOngoingOrders(con, cursor, username)
            elif choice == 2:
                orders.viewAllOrders(con, cursor, username)
            elif choice == 3:
                showIngredientInventory(con, cursor)
            elif choice == 4:
                print('\n'*10)
                print('-'*50)
                homePage(con, cursor)
            else:
                print('Invalid value. Select option 1, 2, or 3, or log out with 4.')
        except ValueError:
            print('Invalid input. Please enter a number.')


def customerDashboard(con, cursor, username, exceptionMessage = None):
    if exceptionMessage == "nospace":
        pass
    elif exceptionMessage == None:
        print('\n'*20)
    else:
        print('\n'*20)
        print(exceptionMessage)
    print('-' *50)
    print(f'Hello {username}! Choose an option:')
    print('[1] Order food\n[2] See order status\n[3] Log out')
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                orders.placeOrder(con, cursor, username)
            elif choice == 2:
                orders.viewMyOrders(con, cursor, username)
            elif choice == 3:
                print('\n'*10)
                print('-'*50)
                homePage(con, cursor)
            else:
                print('Invalid value. Order food with [1], See order status with [2], and Log out with [3]')
        except ValueError:
            print('Invalid input. Please enter a number.')


def showIngredientInventory(con, cursor):
    pass