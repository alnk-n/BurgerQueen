def homePage(con, cursor):

    import auth

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