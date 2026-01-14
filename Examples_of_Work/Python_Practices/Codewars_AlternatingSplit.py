# link to problem: https://www.codewars.com/kata/57814d79a56c88e3e0000786/python
# Full name of problem: Simple Encryption #1 - Alternating Split

# It started simple
def encrypt(text, n):
    if text == "" or text == None or n <= 0:
        return text
    
    for i in range(n):    
        text = text[1::2] + text[::2]
        
    return text

# Here is where I started over thinking. But I got there in the end, reverse-enigeering to get the original. Perhaps not the most efficient.
def decrypt(encrypted_text, n):
    if encrypted_text == "" or encrypted_text == None or n <= 0:
        return encrypted_text
    
    length = len(encrypted_text)
    last_char = None

    # temp is a placeholder variable, will be used later on as working variable
    mid_mark, temp = divmod(length, 2)
    
    # While playing ard w the nums to find a pattern,
    # i realised the last char of an odd num length str is alw the same. so can remove first
    if temp:
        last_char = encrypted_text[-1]
        encrypted_text = encrypted_text[:-1]
        print(temp, n)

    temp = ['']*length
    
    # need to repeat for all interations
    for j in range(n):
        
        # kind of resets the variable, since encrypted_text changes w every iteration
        # reset isnt the word but i cant think of one right now
        if j > 0:
            encrypted_text = temp
            temp = ['']*length
        
        for i in range(mid_mark):
            # inserting the even index chars
            temp[i*2+1] = encrypted_text[i]

            # inserting the odd index chars
            temp[i*2] = encrypted_text[mid_mark+i]
    
    # now to add that last char back
    if last_char is not None:
        temp += [last_char]
        
    return ''.join(temp)


# (Not mine) This is honestly what i was aiming for at first. But I kept mixing things up. Will be studying the how to see if i can implement it.
def decrypt(s, n):
    if not s: return s
    o, l = len(s) // 2, list(s)
    for _ in range(n):
        l[1::2], l[::2] = l[:o], l[o:]
    return ''.join(l)
