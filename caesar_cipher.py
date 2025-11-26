letters = 'abcdefghijklmnopqrstuvwxyz'

print("Enter the plaintext:")
plainText = input().lower()

print("Enter the key value:")
try:
    key = int(input())
except ValueError:
    print("Invalid key. Please enter a number.")
    exit()

# Encryption Logic
cipherText = ''
for char in plainText:
    if char in letters:
        index = letters.index(char)
        shiftedIndex = (index + key) % 26
        cipherText += letters[shiftedIndex]
    else:
        cipherText += char

print("Encrypted Text:", cipherText)

# Decryption Logic
decryptedText = ''
for char in cipherText:
    if char in letters:
        index = letters.index(char)
        shiftedIndex = (index - key) % 26
        decryptedText += letters[shiftedIndex]
    else:
        decryptedText += char

print("Decrypted Text:", decryptedText)
