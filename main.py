def main():
    import sqlite3
    
    con = sqlite3.connect("burgerqueen.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM sqlite_master")
    
    homePage(con, cursor)

    con.close()

def userPointer():
    return input('> ')

def homePage(con, cursor):
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(userPointer())
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

user_database = {
    "admin": "password123",
    "user": "hesterbest"
}

def checkExistingUser(inputUsername):
    cursor.execute("SELECT 1 FROM Users WHERE Username = ?", (inputUsername,))
    user = cursor.fetchone()
    if user:
        return True
    else:
        return False

def loginUser():
    print('-' *50)
    print('Login with existing username.')
    
    while True:
        print("Enter your username: ")
        inputUsername = userPointer()
        if checkExistingUser(inputUsername):
            break # Stops loop if provided username exists in database
        else:
            print("This user doesn't exist. Do you wish to create a new account? (y/N)")
            confirmAccountCreation = userPointer()
            if confirmAccountCreation.lower() == 'y':
                createUser(inputUsername) # If username isn't in database, program asks whether to send over input to createUser function
                return
            else:
                print('-' *50)
                print("Try logging in with an existing username.\n")
                
    print('Input password.')
    inputPassword = userPointer()

    if user_database[inputUsername] == inputPassword: # Checks if password matches username key in dictionary
        print("Login successful!")
    else:
        print("Invalid username or password.")
        loginUser()


def createUser(inputUsername=None):
    print('-' *50)
    # Provides account name upon creation if sent from loginUser() function
    if inputUsername:
        print(f'Create new user "{inputUsername}".')
    else:
        print('Create new user.')

    # If no value is provided through inputUsername, ask for username
    if not inputUsername:
        print('Enter a username for your new account:')
        inputUsername = userPointer()

    if checkExistingUser(inputUsername):
        print('This username already exists. Please choose a different one.')
        createUser()  # Retry if username already exists
    else:
        print('Enter a password for your new account (none to cancel):')
        inputPassword = userPointer()
        if inputPassword == "": # If nothing is input, return to homepage
            print('-' *50)
            homePage()
            return
        else:
            user_database[inputUsername] = inputPassword  # Store the new user
            print(f'Account "{inputUsername}" created successfully!')


if __name__ == "__main__":
   main()