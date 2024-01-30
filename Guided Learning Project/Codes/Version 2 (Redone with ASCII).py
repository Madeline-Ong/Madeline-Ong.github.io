# This version uses the ASCII table so upper and lowercase letters, numbers, and symbols are all included here.

# Although I didn't know of it as I was coming up with the idea in secondary school, my cipher is under the category of Affine Substitution Cipher.
# Where each letter is mapped to its numeric equivalent(x), multiplied by a constant(y), then shifted by another constant(y), and then get the remainder using mod 26 to shift within the range of the alphabet. 
# Affine Cipher formula:  chr = (yx + z) mod 26
# But in my case, the formula is different. Instead of the multiplication and rotational constants, y and z, my cipher uses the index of the chr and the key, multiplied together. 
#     In this version of my cipher, using the ASCII, the formula still uses the numerical equivalent(x) after subtracting 31, but it is shifted by the index of the chr(y) multiplied by the key(k). 
#     The modulus is also changed to 95 as the range of the key value would be 95 since the min chr num is 32 (' ') and max is 126 ('~').
#     The subtracting 31 is so that x stays within the range of ASCII unicode English chr (32-126). Then to convert back to the ASCII unicode English chr range, I add 31. 
# Formula with ASCII:     chr = (x - 31 + yk) mod 95 + 31


##################### Encryption ######################
def encryption():
    from random import randint
    def e_key_check(key):
        global key_max
        
        if key == '':
            key = randint(1, key_max)
            return key
        
        # isdigit checks for just numbers so even -1 would be rejected
        if not key.isdigit():
            print('Key must be numerical and a positive number. Please try again.')
            return None
            
        # checking if key is in acceptable range
        if key > str(key_max) or key == '0':
            print('Key must be more than 0 and less than {}.'.format(key_max))
            return None

        #if pass all checks, returns key to break out of while loop
        return key

    
    # User inputting message to be encrypted
    print()
    plaintext = input('What is the message to be encrypted? ').strip()
    
    key = None
    while key is None:
        key = e_key_check(input('What is the key? (Must be numerical) ').strip())

    key = int(key)
    print(key)
    ciphertext = ''
    for index in range(len(plaintext)):
        char_num = ord(plaintext[index])
        #since py indexing starts from 0, +1 to get position
        index += 1
        new_char_num = (char_num - 31 + index * key) % key_max + 31
        #+31 because if its 1 over 126, will bceome 32 (' ')
        result = chr(new_char_num)
        ciphertext += str(result)
        
    print(ciphertext + '\n')

##################### Decryption ######################
def decryption():
    def d_key_check(key):
        global key_max
        
        #if key is unknown
        if key == 'u':
            return key
        
        # isdigit checks for just numbers so even -1 would be rejected
        if not key.isdigit():
            print('Key must be numerical and a positive number. Please try again.')
            return None
            
        # checking if key is in acceptable range
        if key > str(key_max) or key == '0':
            print('Key must be more than 0 and less than {}.'.format(key_max))
            return None

        #if pass all checks, returns key to break out of while loop
        return key

    def decrypting(key):
        plaintext = ''
        for index in range(len(ciphertext)):
            char_num = ord(ciphertext[index])
            #since py indexing starts from 0, +1 to get position
            index += 1
            new_char_num = (char_num - 31 - index * key) % key_max + 31
            result = chr(new_char_num)
            plaintext += result
        return plaintext

    # User inputting message to be decrypted
    print()
    ciphertext = input('What is the message to be decrypted? ').strip()

    key = None
    while key is None:
        key = d_key_check(input('What is the key? (If unknown key, type \'u\') ').strip())

    if key != 'u':
        key = int(key)
        plaintext = decrypting(key)
        print(plaintext)
    else:
        for key in range(key_max - 1):
            key += 1
            plaintext = decrypting(key)
            print('{}. {}'.format(key, plaintext))
    print()


##################### Choosing encrypt or decrypt ######################

key_max = 95
choice = None
while choice is None:
    print()
    choice = input('Do you want to encrypt or decrypt a message? (d/e) ').lower()
    if choice in 'encryption':
        encryption()
    elif choice in 'decryption':
        decryption()
    else:
        print('Invalid input, please try again.')
        choice = None
        continue

    restart = None
    while restart is None:
        restart = input('Do you want to encrypt or decrypt another message? (y/n) ').lower()
        if restart in 'yes':
            choice = None
        elif restart in 'no':
            print('\nExiting...\n')
            break
        else:
            restart = None

    
