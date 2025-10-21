letters= 'abcdefghijklmnopqrstuvwxyz'


def encrypt(plaintext, key):
    ciphertext=''
    for letter in plaintext:
        letter=letter.lower()
        if not letter==' ':
            i = letters.find(letter)
            if i==-1:
                ciphertext+=letter
            else:
                j = i+key
                if j>=26:
                    j-=26
                ciphertext+=letters[j]    
    return ciphertext

def decrypt(ciphertext, key):
    plaintext=''
    for letter in plaintext:
        letter=letter.lower()
        if not letter==' ':
            i = letters.find(letter)
            if i==-1:
                plaintext+=letter
            else:
                j = i-key
                if j<0:
                    j+=26
                plaintext+=letters[j]    
    return plaintext



print()
print('*** CEASER CIPHER***')
print()

print('Do you want to encrypt or decrypt?')
user_input= input('e/d: ').lower() 
print()

if user_input=='e':
    print('ENCRYPTION MODE')
    print()
    key=int(input('enter the key 1 to 26: '))
    text= input('Enter the text you want to encrypt:')
    ciphertext= encrypt(text, key)
    print(f'CIPHERTEXT: {ciphertext}')
elif user_input=='d':
    print('DECRYPTION MODE')
    print()
    key=int(input('enter the key 1 to 26: '))
    text= input('Enter the text you want to decrypt:')
    plaintext= encrypt(text, key)
    print(f'PLAINTEXT: {plaintext}')
