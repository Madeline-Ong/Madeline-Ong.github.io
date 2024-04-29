# This takes in the inputs that are separated by new lines (when you press enter). 
lines = []
print("Enter your multi-line input. Press Enter without a value on that line to compile the input.")
while True:
    user_input = input()
    
    # If the user pressed Enter without a value, it would break out of the loop:
    if user_input == '':
        break
    else:
        lines.append(user_input.strip())


# This prints the list of all the entered strings - for debugging
#print(lines,end='\n\n')

# This specific code is more for ease, for compiling information - compiling the entered strings into 1 line. It can be changed for other uses, for example, sorting the input alphabetically, etc.

# This compiles the strings from the list into 1 string:
print(''.join(lines))
