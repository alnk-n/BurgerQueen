import argon2
ph = argon2.PasswordHasher()

from utils import returnCheck
import dashboards


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
    print('\n' * 20)
    if exceptionMessage is not None:
        print(exceptionMessage)
    print('-' * 50)
    print('Login with existing username.\n(Press Enter to return)')
    print('-' * 50)

    while True:
        print("Username: ")
        inputUsername = input('> ')
        if returnCheck(inputUsername):  # checks whether user input is equal to "", returns to home
            dashboards.homePage(con, cursor)
            return
        if checkExistingUser(cursor, inputUsername):
            break
        else:
            print("This user doesn't exist. Do you wish to create a new account? (y/N)")
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
    row = cursor.fetchone()

    if not row:
        loginUser(con, cursor, 'Invalid username or password.')
        return

    stored = row[0]

    try:
        # check if password looks like an argon2 hash
        if isinstance(stored, str) and stored.startswith('$argon2'):
            ph.verify(stored, inputPassword)
        else:
            if stored != inputPassword:
                raise argon2.exceptions.VerifyMismatchError()
            # convert plaintext to hash
            newhash = ph.hash(inputPassword)
            cursor.execute("UPDATE Users SET Password = ? WHERE Username = ?", (newhash, inputUsername))
            con.commit()

        dashboards.redirectUserDashboard(con, cursor, inputUsername)
        return

    except (argon2.exceptions.VerifyMismatchError, argon2.exceptions.InvalidHash):
        loginUser(con, cursor, 'Invalid username or password.')
        return


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
            dashboards.homePage(con, cursor)
            return

    if checkExistingUser(cursor, inputUsername):
        createUser(con, cursor, None, 'This username is already taken. Please choose another.')  # Retry if username already exists
    else:
        print('Enter a password for your new account:')
        inputPassword = input('> ')
        if returnCheck(inputPassword):
            dashboards.homePage(con, cursor) # Return to main menu if Enter is pressed
        
        hashedPassword = ph.hash(inputPassword)

        cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (inputUsername, hashedPassword)) # Store the new user
        con.commit()  # Commit to save the new user
        print(f'Account "{inputUsername}" created successfully!')
        dashboards.redirectUserDashboard(con, cursor, inputUsername)