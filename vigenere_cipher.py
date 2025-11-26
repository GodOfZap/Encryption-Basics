# Encryption Logic
def vigenere_encrypt(plaintext, key):
    plaintext = plaintext.upper().replace(" ", "")
    key = key.upper()
    ciphertext = ""

    for i in range(len(plaintext)):
        plain_char = ord(plaintext[i]) - ord('A')
        key_char = ord(key[i % len(key)]) - ord('A')
        encrypted_char = (plain_char + key_char) % 26
        ciphertext += chr(encrypted_char + ord('A'))

    return ciphertext

          # Decryption Logic
def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    plaintext = ""

    for i in range(len(ciphertext)):
        cipher_char = ord(ciphertext[i]) - ord('A')
        key_char = ord(key[i % len(key)]) - ord('A')
        decrypted_char = (cipher_char - key_char + 26) % 26
        plaintext += chr(decrypted_char + ord('A'))

    return plaintext
# Main Program 
plain = input("Enter plaintext: ")
key = input("Enter key: ")

cipher = vigenere_encrypt(plain, key)
print("Ciphertext:", cipher)

decrypted = vigenere_decrypt(cipher, key)
print("Decrypted:", decrypted)
