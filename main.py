def main():
    loginPage()

def loginPage():
    print('HELLO, AND WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:')
    print('[1] Log in with existing user\n[2] Create new user\n[3] Exit program')
    while True:
        try:
            valg = int(input('> '))
            if valg == 1:
                loginUser()
                break
            elif valg == 2:
                createUser()
                break
            elif valg == 3:
                exit()
            else:
                print('Invalid value. Try again.')
        except ValueError:
            print('Invalid input. Please enter a number.')

username = 'admin'
password = 'password'

def loginUser():
    print('-' *30)

def createUser():
    pass

main()