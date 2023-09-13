def check_null(value):

    if value != None:
        valid_input = True

    else:
        valid_input = False
        
    return valid_input


userInput = input("Enter something: ")

valid_input = check_null(userInput)

print(valid_input)
