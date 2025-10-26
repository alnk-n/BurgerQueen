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

def loginUser():
    print('-' *50)
    print('Login with existing username.')
    inputUsername = userPointer()
    print('Input password.')
    inputPassword = userPointer()

def createUser():
    pass

main()