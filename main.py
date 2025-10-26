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



username = 'admin'
password = 'password'

def checkExistingUser(inputUsername):
    if inputUsername == username:
        return True
    else:
        print("This user doesn't exist. Do you wish to create a new account? (y/N)")
        confirmAccountCreation = userPointer()
        if confirmAccountCreation.lower() == 'y':
            createUser(inputUsername)
            return False
        else:
            print("Login with existing username.")
            return False



def loginUser():
    print('-' *50)
    print('Login with existing username.')
    
    while True:
        inputUsername = userPointer()
        if checkExistingUser(inputUsername):
            break

    print('Input password.')
    inputPassword = userPointer()

    if inputUsername == username and inputPassword == password:
        print("Login successful!")
    else:
        print("Invalid username or password.")
        loginUser()



def createUser(loginInput):
    pass



main()