# dashboards.py

import orders # import functions for making orders, and listing all/ongoing orders

# homePage displays the welcome screen and lets the user choose whether to log in, register, or exit
# Arguments:
# con: used to close database on program exit, gets passed around for when homePage is called again
# cursor: used for querying the database
def homePage(con, cursor):

    import auth # import login and register functions from auth.py

    print('\n'*20)
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(input('> '))
            if valg == 1:
                auth.loginUser(con, cursor, None) # 'None' argument is for 'exceptionMessage', used for feedback
                return
            elif valg == 2:
                auth.createUser(con, cursor)
                return
            elif valg == 3:
                con.close()
                exit()
            else:
                print('Invalid value. Select option 1, 2 or 3.')
        except ValueError:
            print('Invalid input. Please enter a number.')


# redirectUserDashboard opens the correct 'dashboard' based on the provided username's employee status
# Arguments:
# con: only passed around because homePage needs it if called again
# cursor: used for querying the database
# username: used for identifying the currently logged-in user
def redirectUserDashboard(con, cursor, username):
    cursor.execute("SELECT IsEmployee FROM Users WHERE Username = ?", (username,))
    employeeStatus = cursor.fetchone()
    
    if employeeStatus and employeeStatus[0] == 1: # if column is filled in and True
        employeeDashboard(con, cursor, username)
    else:
        customerDashboard(con, cursor, username, 'Login successful.')


# Employee dashboard. Displays menu used for choosing to view ongoing/all orders, and to list the ingredient stock
# Arguments:
# con: only passed around because homePage needs it if called again
# cursor: used for querying the database
# username: used for identifying currently logged-in user
# exceptionMessage: used for displaying additional feedback. Results in cleaner terminal GUI.
def employeeDashboard(con, cursor, username, exceptionMessage = None):
    print('\n'*20)
    if exceptionMessage:
        print(exceptionMessage) # example: 'Whoops! There are no orders in the database.'
    print('-' *50)

    print(f'Hello {username}! Choose an option:')
    print('[1] View ongoing orders\n[2] View all orders\n[3] See ingredient inventory\n[4] Log out')
    from inventory import viewInventory # import from inventory.py file
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                orders.viewOngoingOrders(con, cursor, username) # username is passed as an argument so that it can be passed back here when done. This was a cleaner solution than using a global variable.
            elif choice == 2:
                orders.viewAllOrders(con, cursor, username)
            elif choice == 3:
                viewInventory(con, cursor, username)
            elif choice == 4:
                print('\n'*10)
                print('-'*50)
                homePage(con, cursor)
                return
            else:
                print('Invalid value. Select option 1, 2, or 3, or log out with 4.')
        except ValueError:
            print('Invalid input. Please enter a number.')



# Customer dashboard. Displays menu used for placing orders and seeing the status of all personal orders 
# Arguments:
# con: only passed around because homePage needs it if called again
# cursor: used for querying the database
# username: used for identifying currently logged-in user
# exceptionMessage: used for displaying additional feedback
def customerDashboard(con, cursor, username, exceptionMessage = None): # assumes exceptionMessage is None if not provided
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
                return
            else:
                print('Invalid value. Order food with [1], See order status with [2], and Log out with [3]')
        except ValueError:
            print('Invalid input. Please enter a number.')