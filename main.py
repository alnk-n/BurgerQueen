def main():
    import sqlite3
    
    con = sqlite3.connect("burgerqueen.db")
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

def checkExistingUser(cursor, inputUsername):
    cursor.execute("SELECT 1 FROM Users WHERE Username = ?", (inputUsername,))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False
    
def returnCheck(userInput):
    if userInput == "":
        return True
    return False

def redirectUserDashboard(con, cursor, username):
    cursor.execute("SELECT IsEmployee FROM Users WHERE Username = ?", (username,))
    employeeStatus = cursor.fetchone()
    if employeeStatus and employeeStatus[0] == 1:
        employeeDashboard(con, cursor, username)
    else:
        customerDashboard(con, cursor, username)

def loginUser(con, cursor, exceptionMessage):
    print('\n'*20)
    if exceptionMessage != None:
        print(exceptionMessage)
    print('-' *50)
    print('Login with existing username.\n(Press Enter to return)')
    print('-' *50)
    
    while True:
        print("Username: ")
        inputUsername = input('> ')
        if returnCheck(inputUsername): # checks whether user input is equal to "", returns to home
            homePage(con, cursor)
            return
        if checkExistingUser(cursor, inputUsername):
            break # Stops loop if provided username exists in database
        else:
            print("This user doesn't exist. Do you wish to create a new account? (y/N)")
            confirmAccountCreation = input('> ')
            if confirmAccountCreation.lower() == 'y':
                createUser(con, cursor, inputUsername) # If username isn't in database, program asks whether to send over input to createUser function
                return
            else:
                print('\n'*20)
                print("Try logging in with an existing username.")
                print("(Press Enter to return)")
                print('-' *50)
                
    print('Input password.')
    inputPassword = input('> ')
    cursor.execute("SELECT Password FROM Users WHERE Username = ?", (inputUsername,))
    userPassword = cursor.fetchone()
    if userPassword and userPassword[0] == inputPassword: # Checks if password matches the database in matching row
        print("Login successful!")
        redirectUserDashboard(con, cursor, inputUsername)
    else:
        loginUser(con, cursor, 'Invalid username or password.')


def createUser(con, cursor, inputUsername=None, exceptionMessage=None):
    print('\n'*20)
    print('-' *50)
    if exceptionMessage:
        print(exceptionMessage)
    # Provides account name upon creation if sent from loginUser() function
    if inputUsername:
        print(f'Create a new account called "{inputUsername}".')
    else:
        print('Create a new account.')
    print('(Press Enter to return)')
    print('-'*50)

    # If no value is provided through inputUsername, ask for username
    if not inputUsername:
        print('Enter a username for your new account: ')
        inputUsername = input('> ')
        if returnCheck(inputUsername): # checks whether user input is equal to "", returns to home
            homePage(con, cursor)
            return

    if checkExistingUser(cursor, inputUsername):
        createUser(con, cursor, None, 'This username is already taken. Please choose another.')  # Retry if username already exists
    else:
        print('Enter a password for your new account:')
        inputPassword = input('> ')
        if returnCheck(inputPassword):
            homePage(con, cursor) # Return to main menu if Enter is pressed
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (inputUsername, inputPassword)) # Store the new user
        con.commit()  # Commit to save the new user
        print(f'Account "{inputUsername}" created successfully!')
        redirectUserDashboard(con, cursor, inputUsername)


def listSelection(order):
        print('**Your Order**')
        print('-'*10)
        unique_items = set(order)
        for item in unique_items:
            print(f"{order.count(item)}x {item}")
        print('-'*10)

def addToOrder(order, item):
    order.append(item)
    listSelection(order)

def placeOrder(con, cursor, username):
    order = ()
    print('\n'*20)
    print('-' *50)
    print('Select the items you wish to add to your order.\nConfirm with [4].')
    print('-' *50)
    
    print('[1] Whopper Queen\n[2] Triple Cheesy Princess\n[3] Kingdom Fries\n[4] Confirm order\n[5] Return')
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                addToOrder(order, "Whopper Queen")
            elif choice == 2:
                addToOrder(order, "Triple Cheesy Princess")
            elif choice == 3:
                addToOrder(order, "Kingdom Fries")
            elif choice == 4:
                break
            elif choice == 5:
                redirectUserDashboard(con, cursor, username)
            else:
                print('Invalid value. Select items with 1-3, confirm with 4 or quit with 5.')
        except ValueError:
            print('Invalid input. Please enter a number.')
    listSelection()


def showOrderStatus(con, cursor, username):
    pass


def employeeDashboard(con, cursor, username):
    pass


def customerDashboard(con, cursor, username):
    print('\n'*20)
    print('Login successful.')
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