def main():
    loginPage()

def userPointer():
    return input('> ')

def loginPage():
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(userPointer())
            if valg == 1:
                loginUser()
                break
            elif valg == 2:
                createUser()
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
    if inputUsername in user_database:
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
            break
        else:
            print("This user doesn't exist. Do you wish to create a new account? (y/N)")
            confirmAccountCreation = userPointer()
            if confirmAccountCreation.lower() == 'y':
                createUser(inputUsername)
                return
            else:
                print("Try logging in with an existing username.\n")
                
    print('Input password.')
    inputPassword = userPointer()

    if user_database[inputUsername] == inputPassword:
        print("Login successful!")
    else:
        print("Invalid username or password.")
        loginUser()



def createUser(inputUsername=None):
    print('-' *50)
    print('Input new username.')

    if not inputUsername:
        print('Enter a username for your new account:')
        inputUsername = userPointer()

    if checkExistingUser(inputUsername):
        print("This username already exists. Please choose a different one.")
        createUser()  # Retry if username already exists
    else:
        print('Enter a password for your new account:')
        inputPassword = userPointer()
        user_database[inputUsername] = inputPassword  # Store the new user
        print(f"Account created successfully for {inputUsername}!")



main()