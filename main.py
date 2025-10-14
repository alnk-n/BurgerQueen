def main():
    loginPage()

def loginPage():
    print("HELLO, WELCOME TO BURGER QUEEN. CHOOSE AN ALTERNATIVE:")
    print("[1] Log in with existing user\n[2] Create new user\n[3] Exit program")
    valg = str(input())
    if valg == 1:
        loginUser()
    if valg == 2:
        createUser()
    if valg == 3:
        exit()

main()