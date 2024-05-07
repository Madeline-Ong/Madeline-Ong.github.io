def rail_fence_cipher_e():
    rails = input('Enter your number of rails: ')
    while rails.isdigit() == False:
        print('\nPlease try again, the number of rails should be an integer.')
        rails = input('Enter your number of rails: ')

    rails = int(rails)
    plaintext = input('Enter your plaintext: ').strip()
    ciphertext = [''] * rails

    down = True
    row = 0
    for index in range(len(plaintext)):
        if plaintext[index].isspace():
            continue
        else: 
            ciphertext[row] += plaintext[index]
        if row < (rails-1) and down == True:
            row += 1
        elif row > 0 and down == False:
            row -= 1

        if row == 0 or row == (rails-1):
            down = not down

    ciphertext = ''.join(ciphertext)
    print(ciphertext)

    ### Optional (for the spacing) ###
##    for index in range(0, len(ciphertext)):
##        if index % 6 == 0:
##            ciphertext = ciphertext[:index] + ' ' + ciphertext[index:]

    ciphertext = ciphertext.strip()
    print(ciphertext)
