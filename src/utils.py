# utils.py

# Essentially checks whether the user has pressed Enter without inputting anything. In my program, this means you wish to cancel/return.
# Arguments:
# userInput: checks input provided in argument. (e.g. a password/username)
def returnCheck(userInput):
    if userInput == "":
        return True
    return False