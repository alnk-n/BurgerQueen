# auth.py

import argon2
ph = argon2.PasswordHasher()

# the user can return from any prompt by inputting nothing (Press Enter). The returnCheck function handles this.
from utils import returnCheck
import dashboards


# Queries database to see whether argument username exists in Users table
# Arguments:
# cursor: used for querying the database
# inputUsername: takes input username and uses it in the database query
def checkExistingUser(cursor, inputUsername):
    cursor.execute("SELECT 1 FROM Users WHERE Username = ?", (inputUsername,))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False


# Converts username to UserID
# Arguments:
# cursor: used for querying the database
# inputUsername: takes input username and uses it in the database query
def fetchUserID(cursor, username):
    cursor.execute("SELECT UserID FROM Users WHERE Username = ?", (username,))
    userID = cursor.fetchone()
    return userID


# Handles check of pre-existing account, if not, prompt for account creation. Also checks hashed passwords, and updates DB password to hash if it's stored in plaintext (for example caused by running the dummy-data script)
# Arguments:
# con: used for passing database connection along, used for homePage
# cursor: used for querying the database
# exceptionMessage: used for extra feedback to the user
def loginUser(con, cursor, exceptionMessage):
    print('\n' * 20)
    if exceptionMessage is not None:
        print(exceptionMessage) # cleaner solution for error message (e.g. 'Invalid username or password.')
    print('-' * 50)
    print('Login with existing username.\n(Press Enter to return)')
    print('-' * 50)

    while True:
        print("Username: ")
        inputUsername = input('> ')
        if returnCheck(inputUsername):  # checks whether user input is equal to "", returns to home
            dashboards.homePage(con, cursor)
            return
        if checkExistingUser(cursor, inputUsername): # continues password check if username exists in DB
            break
        else:
            print("This user doesn't exist. Do you wish to create a new account? (y/N)") # prompts for account creation if username doesn't exist in DB
            confirmAccountCreation = input('> ')
            if confirmAccountCreation.lower() == 'y':
                createUser(con, cursor, inputUsername)
                return
            else:
                print('\n' * 20)
                print("Try logging in with an existing username.")
                print("(Press Enter to return)")
                print('-' * 50)

    print('Input password.')
    inputPassword = input('> ')

    cursor.execute("SELECT Password FROM Users WHERE Username = ?", (inputUsername,))
    row = cursor.fetchone() # fetches password from DB

    if not row: # if no password is found for some reason, throw an error
        loginUser(con, cursor, 'Invalid username or password.')
        return

    stored = row[0]

    try:
        # check if the stored password is an argon-hashed string
        if isinstance(stored, str) and stored.startswith('$argon2'): # check if password is string and starts with '$argon2'
            # verify that input password hash matches stored hash
            ph.verify(stored, inputPassword) # if True, break the loop and call redirect function
        else:
            # if the stored password is plaintext, compare it with the input password straight up
            if stored != inputPassword: 
                raise argon2.exceptions.VerifyMismatchError()
            
            # if passwords do match, hash the input plaintext password and update the database with hash
            newhash = ph.hash(inputPassword)
            cursor.execute("UPDATE Users SET Password = ? WHERE Username = ?", (newhash, inputUsername))
            con.commit()

        # redirect user to their dashboard after successful login or password update
        dashboards.redirectUserDashboard(con, cursor, inputUsername)
        return

    # handle incorrect username/password or invalid hash
    except (argon2.exceptions.VerifyMismatchError, argon2.exceptions.InvalidHash):
        loginUser(con, cursor, 'Invalid username or password.')
        return


# Handles creation of account. Checks username availability, and hashed input password before storing the new account in DB.
# Arguments:
# con: used for passing database connection along, used for homePage
# cursor: used for querying the database
# inputUsername: used for gracefully using the already input username from the loginUser() function, only requiring the input of a new password.
# exceptionMessage: used internally for extra feedback to the user (e.g. 'This username is already taken. Please choose another.')
def createUser(con, cursor, inputUsername=None, exceptionMessage=None):
    print('\n'*20)
    print('-' *50)
    if exceptionMessage:
        print(exceptionMessage) # cleaner solution for error message (e.g. 'Invalid username or password.')
    
    if inputUsername: # if there's an input username provided by the loginUser() function
        print(f'Create a new account called "{inputUsername}".') # create a new account under that username, require input of new password
    else:
        print('Create a new account.') # standard title printout if not called from loginUser() function
    print('(Press Enter to return)')
    print('-'*50)

    # 'Body text'. If no value is provided through inputUsername, ask for new username input
    if not inputUsername:
        print('Enter a username for your new account: ')
        inputUsername = input('> ')
        if returnCheck(inputUsername): # checks whether user input is equal to "", returns to home
            dashboards.homePage(con, cursor)
            return

    if checkExistingUser(cursor, inputUsername):
        createUser(con, cursor, None, 'This username is already taken. Please choose another.')  # Rerun function if username already exists with graceful exceptionMessage
    else:
        print('Enter a password for your new account:')
        inputPassword = input('> ')
        if returnCheck(inputPassword):
            dashboards.homePage(con, cursor) # return to main menu if nothing is input (if Pressed Enter)
        
        hashedPassword = ph.hash(inputPassword) # hashes newly input password

        # store the new user
        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (inputUsername, hashedPassword))
        con.commit()
        print(f'Account "{inputUsername}" created successfully!')
        dashboards.redirectUserDashboard(con, cursor, inputUsername) # redirects to correct dashboard after account creation