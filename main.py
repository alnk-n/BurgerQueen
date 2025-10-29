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
    
def returnCheck(con, cursor, userInput):
    if userInput == "":
        print('\n'*20)
        print('-'*50)
        homePage(con, cursor)
    else:
        return

def loginUser(con, cursor):
    print('-' *50)
    print('Login with existing username.\n(Press Enter to return)')
    print('-' *50)
    
    while True:
        print("Username: ")
        inputUsername = input('> ')
        returnCheck(con, cursor, inputUsername)
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
    user = cursor.fetchone()
    if user and user[0] == inputPassword: # Checks if password matches the database in matching row
        print("Login successful!")
    else:
        print("Invalid username or password.")
        loginUser(con, cursor)


def createUser(con, cursor, inputUsername=None):
    print('-' *50)
    # Provides account name upon creation if sent from loginUser() function
    if inputUsername:
        print(f'Create a new account called "{inputUsername}".\n(Press Enter to return)\n')
    else:
        print('Create a new account.\n(Press Enter to return)\n')

    # If no value is provided through inputUsername, ask for username
    if not inputUsername:
        print('Enter a username for your new account: ')
        inputUsername = input('> ')
        returnCheck(con, cursor, inputUsername)

    if checkExistingUser(cursor, inputUsername):
        print('This username is already taken. Please choose another.\n')
        createUser(con, cursor)  # Retry if username already exists
    else:
        print('Enter a password for your new account:')
        inputPassword = input('> ')
        returnCheck(con, cursor, inputPassword)
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (inputUsername, inputPassword)) # Store the new user
        con.commit()  # Commit to save the new user
        print(f'Account "{inputUsername}" created successfully!')


if __name__ == "__main__":
   main()