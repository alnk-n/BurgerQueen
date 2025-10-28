def main():
    import sqlite3
    
    con = sqlite3.connect("burgerqueen.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    
    homePage(con, cursor)

    con.close()

def homePage(con, cursor):
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(input('> '))
            if valg == 1:
                loginUser(con, cursor)
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

def checkUserPrivileges(cursor):
    print(currentUserID)
    pass

def loginUser(con, cursor):
    print('-' *50)
    print('Login with existing username.')
    
    while True:
        print("Enter your username: ")
        inputUsername = input('> ')
        if checkExistingUser(cursor, inputUsername):
            break # Stops loop if provided username exists in database
        else:
            print("This user doesn't exist. Do you wish to create a new account? (y/N)")
            confirmAccountCreation = input('> ')
            if confirmAccountCreation.lower() == 'y':
                createUser(con, cursor, inputUsername) # If username isn't in database, program asks whether to send over input to createUser function
                return
            else:
                print('-' *50)
                print("Try logging in with an existing username.\n")
                
    print('Input password.')
    inputPassword = input('> ')
    cursor.execute("SELECT Password FROM Users WHERE Username = ?", (inputUsername,))
    userPassword = cursor.fetchone()
    if userPassword and userPassword[0] == inputPassword: # Checks if password matches the database in matching row
        cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (inputUsername,))
        userID = cursor.fetchone()
        global currentUserID
        currentUserID = userID[0]
        print("Login successful!")
        checkUserPrivileges(cursor)
    else:
        print('-' *50)
        print("Invalid username or password.")
        loginUser(con, cursor)


def createUser(con, cursor, inputUsername=None):
    print('-' *50)
    # Provides account name upon creation if sent from loginUser() function
    if inputUsername:
        print(f'Create new user "{inputUsername}".')
    else:
        print('Create new user.')

    # If no value is provided through inputUsername, ask for username
    if not inputUsername:
        print('Enter a username for your new account: ')
        inputUsername = input('> ')

    if checkExistingUser(cursor, inputUsername):
        print('-' *50)
        print('This username already exists. Please choose a different one.')
        createUser(con, cursor)  # Retry if username already exists
    else:
        print('Enter a password for your new account (none to cancel):')
        inputPassword = input('> ')
        if inputPassword == "": # If nothing is input, return to homepage
            print('-' *50)
            homePage(con, cursor)
            return
        else:
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (inputUsername, inputPassword)) # Store the new user
            con.commit()  # Commit to save the new user
            print(f'Account "{inputUsername}" created successfully!')

order = []
def showOrder():
        print('**Your Order**')
        print('-'*10)
        unique_items = set(order)
        for item in unique_items:
            print(f"{order.count(item)}x {item}")
        print('-'*10)

def addToOrder(item):
    order.append(item)
    showOrder()

def placeOrder(con, cursor):
    print('-' *50)
    print('Select your order.')
    print('[1] Whopper Queen\n[2] Triple Cheesy Princess\n[3] Kingdom Fries\n[4] Confirm order\n[5] Exit')
    while True:
        try:
            choice = int(input('> '))
            if choice == 1:
                addToOrder("Whopper Queen")
            elif choice == 2:
                addToOrder("Triple Cheesy Princess")
            elif choice == 3:
                addToOrder("Kingdom Fries")
            elif choice == 4:
                break
            elif choice == 5:
                exit()
            else:
                print('Invalid value. Select items with 1-3, confirm with 4 or quit with 5.')
        except ValueError:
            print('Invalid input. Please enter a number.')
    showOrder()


if __name__ == "__main__":
   main()