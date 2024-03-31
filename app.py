import struct
import math
from flask import Flask, render_template, request
# Constants for MD5
S = [
    7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
    5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
    4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
    6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
]

K = [
    # Use the integer part of the sines of integers (in radians) as constants:
    int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)
]

# Initial hash values
initial_values = [
    0x67452301,
    0xEFCDAB89,
    0x98BADCFE,
    0x10325476
]

# Functions for MD5
def F(x, y, z):
    return (x & y) | (~x & z)

def G(x, y, z):
    return (x & z) | (y & ~z)

def H(x, y, z):
    return x ^ y ^ z

def I(x, y, z):
    return y ^ (x | ~z)

# Left rotate function in order to achieve diffusion and confusion.
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    # rotates x by amount positions 
    return ((x << amount) | (x >> (32 - amount))) & 0xFFFFFFFF

# MD5 main function
def md5(message):
    # Pre-processing: padding the message
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    message += struct.pack('<Q', original_bit_len)

    # Process the message in successive 512-bit chunks
    hash_pieces = initial_values[:]

    for chunk_offset in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_offset:chunk_offset + 64]
        for i in range(64):
            if 0 <= i <= 15:
                f = F(b, c, d)
                g = i
            elif 16 <= i <= 31:
                f = G(b, c, d)
                g = (5 * i + 1) % 16
            elif 32 <= i <= 47:
                f = H(b, c, d)
                g = (3 * i + 5) % 16
            elif 48 <= i <= 63:
                f = I(b, c, d)
                g = (7 * i) % 16
            to_rotate = a + f + K[i] + struct.unpack('<I', chunk[g * 4:g * 4 + 4])[0]
            new_b = (b + left_rotate(to_rotate, S[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF

    return sum(x << (32 * i) for i, x in enumerate(hash_pieces))

# Helper function to format the hash in hexadecimal
def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

# for running locally :  

# # if __name__ == '__main__':
# message =str(input("Enter your message : "))
# message=message.encode('utf-8')
# md5_digest = md5(message) # 128bit digest string
# print("MD5 Digest:", md5_to_hex(md5_digest))


# flask module app 
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    digest = ''
    if request.method == 'POST':
        # Retrieve the message from the form
        message = request.form['message']
        # Convert the message to bytes, as the MD5 function expects byte input
        byte_message = message.encode('utf-8')
        # Calculate the MD5 digest
        md5_digest = md5(byte_message)
        # Convert the digest to a hexadecimal string
        digest = md5_to_hex(md5_digest)
    return render_template('index.html', digest=digest)

if __name__ == '__main__':
    app.run(debug=True)  # copy the link form the console and open in web browser
    
    ## OR you can visit https://yadavankit671.pythonanywhere.com/  to view the project