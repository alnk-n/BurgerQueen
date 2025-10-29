from utils import returnCheck


def checkExistingUser(cursor, inputUsername):
    cursor.execute("SELECT 1 FROM Users WHERE Username = ?", (inputUsername,))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False


def fetchUserID(cursor, username):
    cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
    userID = cursor.fetchone()
    return userID


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

