# Warning: This is code that I had written and refined in secondary school. It works as it is but has more to be worked upon.
# Such as making it run more smoothly, be more effective (use less time-space), and harder to break. There may be notes from past me as well.


# The encryption is addition of certain no. that changes w/ every letter
# Key can be set by user or random and would then be multiplied by its index + 1
# eg: key = 2, msg is "Hello"
#     1st letter "H" will be shifted forward by 1 * 2 = 2 letters to become "J"
#     2nd letter "e" will be shifted forward by 2 * 2 = 4 letters to become "i"
#     3rd letter "l" will be shifted forward by 3 * 2 = 6 letters to become "r"
#     4th letter "l" will be shifted forward by 4 * 2 = 8 letters to become "t"
#     5th letter "o" will be shifted forward by 5 * 2 = 10 letters to become "y"
#     Thus the encrypted msg is "Jirty"

# Encryption:
# • rand key,
# • program able to restart, 
# • exit code, 
# • -ve key 

import random
import sys

global lower
lower = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n'\
            ,'o','p','q','r','s','t','u','v','w','x','y','z']
global upper
upper = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N'\
         ,'O','P','Q','R','S','T','U','V','W','X','Y','Z']

global start
start = None

global key
key = ""

def restarting():
    global start
    global restart
    restart = input("Do you want to encrypt another message?(Yes/No) ").lower()
    if restart == "yes":
        start = True ###purpose of this?
    elif restart == "no":
        print("Exiting...")
        start = False ###is this actually needed?
        sys.exit()
    elif restart == "0":
        confirm = input("Are you sure you want to exit?(Yes/No) ").lower()
        if confirm == 'yes':
            print("Exiting the program...")
            sys.exit()
        elif confirm == "no":
            restart = input("Do you want to encrypt another message?(Yes/No) ").lower()
            if restart == "yes":
                start = True
            elif restart == "no":
                print("Exiting...")
                start = False
                sys.exit()
            else:
                if not(restart == "yes") and restart != 'no':
                    print("Invalid answer \nPlease write Yes or No")
        else:
            print("Invalid input \nPlease enter Yes or No")
            
    else:
        while not(restart == 'yes') and not(restart == 'no'):
            print("Invalid input")
            restart = input("Do you want to encrypt another message?(Yes/No) ").lower()
            if restart == "yes":
                start = True
            elif restart == "no":
                print("Exiting...")
                start = False

def encrypt_key_funct():
    global key
    key = input("What is your key: (For random key, click enter)")
    while key == "0":
        confirm = input("Are you sure you want to exit?(Yes/No) ").lower()
        if confirm == 'yes':
            print("Exiting the program...")
            sys.exit()
        elif confirm == 'no':
            print("Continuing with the program...")
            key = input("What is your key: (For random key, click enter)")
        else:
            print("Invalid input \nPlease enter Yes or No")
    
    if len(key) == 0:
        key = random.randint(1, 25)
    else: 
        if "*" in key or "/" in key or "+" in key or "-" in key or "(" in key or ")" in key:
            key = str(eval(key))
        while ("." in key) == True:
            print("Invalid key \nKey should not be a float")
            key = input("What is your key: (For random key, click enter)")
        while key.isdigit() == False and len(key) != 0:
            if key[1:].isdigit() == True and key[0] == "-":
                break
            print("Invalid key \nKey is not a number")
            key = input("What is your key: (For random key, click enter)")
        while key.isspace() == True:
            print("Key is empty")
            key = input("What is your key: (For random key, click enter)")


def my_encrypt():
    global lower
    global upper
    global start
    global key
    
    confirm = ""
    print("To exit the program, enter 0 at any point")
    start = None
    while start == True or start == None:
        if start == None or start == True:
            msg = input("What is your message? ")
        while len(msg) == 0 or msg.isspace() == True:
            print("Message is empty")
            msg = input("Please enter your message: ")
        while msg == "0":
            confirm = input("Are you sure you want to exit?(Yes/No) ").lower()
            if confirm == 'yes':
                print("Exiting the program...")
                sys.exit()
            elif confirm == "no":
                print("Continuing with the program...")
                msg = input("Please enter your message: ")
            else:
                print("Invalid input \nPlease enter Yes or No")
                
        
        encrypt_key_funct()
        
        key = int(key)%26
        
        while key == 0:
            print("Message has not changed")
            key_0 = input("Would you like to select another key? (Y/N) ").lower()
            if key_0 == "y":
                encrypt_key_funct()
            elif key_0 == "n":
                '''
                print("I apologise but I am not advanced enough to handle this situation.")
                print("Exiting...")
                sys.exit()
                '''
                restarting()
            while key_0 != "y" and not(key_0 == "n"):
                print("Invalid input")
                key_0 = input("Would you like to select another key? (Y/N) ").lower()
                if key_0 == "y":
                    encrypt_key_funct()
                elif key_0 == "n":
                    '''
                    print("I apologise but I am not advanced enough to handle this situation.")
                    print("Exiting...")
                    sys.exit()
                    '''
                    restarting()
        
        msg = msg.strip()
        result = ""
        for i in range(len(msg)):
            if msg[i] == " ":
                result += " "
            elif msg[i].isalpha() != True:
                result += msg[i]
            else:
                for a in range(len(lower)):
                    if msg[i] == lower[a]:
                        y = i + 1
                        result += lower[(a + (y*int(key))) % 26]
                    elif msg[i] == upper[a]:
                        y = i + 1
                        result += upper[(a + (y*int(key))) % 26]
        print("Your encrypted message:", result)
        restarting()


# Decryption:
# • rand key(lst of poss msg), 
# • -ve key, 
# • exit code, 
# • program able to restart
# • program should be able to handle eqn

def decrypt_key_funct():
    global key
    key = input("What is your key? (If key is not known, click enter)")
    while key == "0":
        confirm = input("Are you sure you want to exit?(Yes/No) ").lower()
        if confirm == 'yes':
            print("Exiting the program...")
            sys.exit()
        elif confirm == 'no':
            print("Continuing with the program...")
            key = input("What is your key? (If key is not known, click enter)").lower()
        else:
            print("Invalid input \nPlease enter Yes or No")
    
    if type(key) == str:
        if "*" in key or "/" in key or "+" in key or "-" in key or "(" in key or ")" in key:
            key = str(eval(key))
        while ("." in key) == True:
            print("Invalid key \nKey should not be a float")
            key = input("What is your key? (If key is not known, click enter)")
        while key.isdigit() == False and len(key) != 0:
            if key[1:].isdigit() == True and key[0] == "-":
                break
            print("Invalid key \nKey is not a number")
            key = input("What is your key? (If key is not known, click enter)")
        while key.isspace() == True:
            print("Key is empty")
            key = input("What is your key? (If key is not known, click enter)")
            


def my_decrypt():
    global lower
    global upper
    global start
    global key
    
    confirm = ""
    print("To exit the program, enter 0 at any point")
    
    msg = input("Please enter your encrypted message: ")
    
    start = None
    while start == True or start == None:
        if start == True:
            msg = input("Please enter your encrypted message: ")
        
        while len(msg) == 0 or msg.isspace() == True:
            print("Message is empty")
            msg = input("Please enter your encrypted message: ")
        while msg == "0":
            confirm = input("Are you sure you want to exit?(Yes/No) ").lower()
            if confirm == 'yes':
                print("Exiting the program...")
                sys.exit()
            elif confirm == "no":
                print("Continuing with the program")
                msg = input("Please enter your encrypted message: ")
            else:
                print("Invalid input \nPlease enter Yes or No")
         
        decrypt_key_funct()
        msg = msg.strip()
        
        possible_msg = []
        if len(key) != 0:
            key = int(key) % 26
            result = ""
            for i in range(len(msg)):
                if msg[i] == " ":
                    result += " "
                elif msg[i].isalpha() != True:
                    result += msg[i]
                else:
                    for a in range(len(lower)):
                        index = i + 1 
                        if msg[i] == lower[a]:
                            result += lower[(lower.index(msg[i])-(index*key)) % 26]
                        if msg[i] == upper[a]:
                            result += upper[(upper.index(msg[i])-(index*key)) % 26]
            print("Your decrypted message:", result)
        
        elif len(key) == 0:
            for x in range(1, 26):
                possible_msg.append("")
                decoded = ""
                for i in range(len(msg)):
                    if msg[i] == " ":
                        decoded += " "
                    elif msg[i].isalpha() != True:
                        decoded += msg[i]
                    else:
                        for a in range(len(lower)):
                            index = i + 1 
                            if msg[i] == lower[a]:
                                decoded += lower[(lower.index(msg[i])- index*x) % 26]
                            if msg[i] == upper[a]:
                                decoded += upper[(upper.index(msg[i])- index*x) % 26]
                possible_msg[x-1] += decoded

            print("List of possible messages: ")
            for i in range(len(possible_msg)):
                if (i + 1) < 10:
                    print("{}. ".format(i+1), possible_msg[i])
                else:
                    print("{}.".format(i+1), possible_msg[i])
        print("")
        
        restart = input("Do you want to decrypt another message?(Yes/No) ").lower()
        
        if restart == "yes":
            start = True
        elif restart == "no":
            print("Exiting...")
            start = False
        elif restart == "0":
            confirm = input("Are you sure you want to exit?(Yes/No) ").lower()
            if confirm == 'yes':
                print("Exiting the program...")
                sys.exit()
            elif confirm == "no":
                restart = input("Do you want to decrypt another message?(Yes/No) ").lower()
                if restart == "yes":
                    start = True
                elif restart == "no":
                    print("Exiting...")
                    start = False
                else:
                    while not(restart == "yes") and restart != 'no':
                        print("Invalid answer \nPlease write Yes or No")
                        restart = input("Do you want to decrypt another message?(Yes/No) ").lower()
            else:
                print("Invalid input \nPlease enter Yes or No")
                
        else:
            while not(restart == 'yes') and not(restart == 'no'):
                print("Invalid input")
                restart = input("Do you want to decrypt another message?(Yes/No) ").lower()
                if restart == "yes":
                    start = True
                elif restart == "no":
                    print("Exiting...")
                    start = False

# Calling Both:

def my_code():
    global qn
    qn = input("Do you want to encrypt or decrypt a message? \n(E for encrypt or D for decrypt)").lower()
    if qn == "e":
        my_encrypt()
    elif qn == "d":
        my_decrypt()
    while qn != "e" and not(qn == "d"):
        print("Invalid Input \nProgamme is not able to execute command")
        qn = input("Do you want to encrypt or decrypt a message? \n(E for encrypt or D for decrypt)").lower()
        if qn == "e":
            my_encrypt()
            d_qn = input("Do you want to decrypt your message? (Y/n)").lower()
            if d_qn  == "y":
                my_decrypt()
            elif d_qn  == "n":
                print("Exiting...")
                sys.exit()
            else:
                while d_qn  != "y" or d_qn  != "n":
                    d_qn = input("Invalid input \nDo you want to decrypt your message? (Y/n)").lower()
        elif qn == "d":
            my_decrypt()

my_code()
