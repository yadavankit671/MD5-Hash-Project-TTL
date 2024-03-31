import math

def isprime(x:int)->bool:
    if x < 2 : return False
    for i in range(2, x//2+1):
        if x%i==0: return False
    return True

def hex_gen(fractional_part)->str:
    hex_string=hex(int(fractional_part * (2**32)) & 0xFFFFFFFF)
    return hex_string.upper()

if __name__ == '__main__':
    num=int(input("Enter a prime number : "))
    #if input is composite
    if(isprime(num)==False):
        raise Exception(str(num)+ " is not a valid prime number ")
    # chaining variable is the fractional part of the square root of the prime number 
    # converted to 32 - bit hex code 
    sqrt_prime=math.sqrt(num)
    fractional_part=sqrt_prime-int(sqrt_prime)
    hex_code=hex_gen(fractional_part)
    print("32-bit hex : "+hex_code)