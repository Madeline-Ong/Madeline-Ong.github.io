morse_code = { 'a':'.-', 'b':'-...', 'c':'-.-.', 'd':'-..', 'e':'.', 
               'f':'..-.', 'g':'--.', 'h':'....', 'i':'..', 'j':'.---', 
               'k':'-.-', 'l':'.-..', 'm':'--', 'n':'-.', 'o':'---', 
               'p':'.--.', 'q':'--.-', 'r':'.-.', 's':'...', 't':'-', 
               'u':'..-', 'v':'...-', 'w':'.--', 'x':'-..-', 'y':'-.--', 
               'z':'--..', '1':'.----', '2':'..---', '3':'...--', 
               '4':'....-', '5':'.....', '6':'-....', '7':'--...', 
               '8':'---..', '9':'----.', '0':'-----', ', ':'--..--', 
               '.':'.-.-.-', '?':'..--..', '/':'-..-.', '-':'-....-', 
               '(':'-.--.', ')':'-.--.-'}
val = list(morse_code.values())
keys = list(morse_code.keys())

def check_purpose(purpose):
    if purpose == 'e' or purpose.startswith('encrypt'):
        purpose = 'encrypt'
        return purpose
    elif purpose == 'd' or purpose.startswith('decrypt'):
        purpose = 'decrypt'
        return purpose
    else:
        return False

purpose = check_purpose(input('Are you encrypting or decrypting a message? ').lower())
while purpose:
    print('Accepted inputs (not case sensitive): E, d, encrypt*, decrypt*')
    purpose = check_purpose(input('Are you encrypting or decrypting a message? ').lower())

letter_sep = input("What is used to separate your letters? ")
while len(letter_sep) == 0 or '-.' in letter_sep:
    print("Invalid letter separator. It cannot be blank or '.' or '-'.\n")
    letter_sep = input("What is used to separate your letters? ")

word_sep = input("What is used to separate your words? ")
while len(word_sep) == 0 or '-.' in word_sep or letter_sep == word_sep:
    print("Invalid word separator. It cannot be blank or '.' or '-' or the same as the letter separator.\n")
    word_sep = input("What is used to separate your words? ")


msg = input('Enter your message to be {}ed: '.format(purpose))

def morse_decrypt(msg):
    global word_sep
    global letter_sep
    global val 
    global keys
    
    words = msg.strip().split(word_sep)
    
    output = ''
    for a in range(len(words)):
    #The strip is to remove spaces if the words are like '- .... . \ -... ' and so on (in this eg, letter sep is ' ' and word sep is '\')
      word = words[a].strip().split(letter_sep)
      for b in range(len(word)):
          for c in range(len(val)):
              if word[b] == val[c]:
                  output += keys[c]
                  break
      if a != len(words)-1:
          output += '_'
    
    print(output) #can add .upper() to change the case of the output

def morse_decrypt(msg):
    global word_sep
    global letter_sep
    
    words = msg.strip().split()
    for word in words:
        for char in word:
            output += morse_code[char] + word_sep
        output += letter_sep
    
    print(output)

if purpose.startswith('d'):
    morse_decrypt(msg)
elif purpose.startswith('e'):
    morse_encrypt(msg)
else: #Should not run but as in case
    print('Error')
    
