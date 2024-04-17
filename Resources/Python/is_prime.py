# This is more of a fun fact I suppose. This is one of the more efficient ways to check if a number is prime. (would need to research if there is a faster way)

def is_prime(num):
    #0, 1 & negative nums are never prime
    if num <= 1: 
        return False 
    
    #2 and 3 are prime
    elif num <= 3: 
        return True
    
    #Even nums and multiples of 3 are not prime
    elif num % 2 == 0 or num % 3 == 0: 
        return False
    else:
        #Start from 5 because 4 is not prime
        factor = 5
        
        #Loop till sq root of num (since f1 * f2 = num, then f1 or f2 <= sqrt(n) )
        while factor * factor <= num: 
            
            #Check if current number and number + 2 are factors
            #a  b  c   d   e   f   g   h   i   j
            #5, 7, 11, 13, 17, 19, 23, 29, 31, 37
            #For about every alternate prime num (a,c,e,g), diff is 6 and next prime is +2
            #Even if next prime is not +2 and is +6, if num is divisible by factor+2, then is not prime
            if num % factor == 0 or num % (factor + 2) == 0: 
                return False
            
            #Skip multiples of 2 & 3
            factor += 6  
        return True
