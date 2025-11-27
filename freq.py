# Install wordfreq if not already installed:
# pip install wordfreq

from wordfreq import zipf_frequency

def caesar_decrypt(ciphertext, shift):
    result = ""
    for ch in ciphertext:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            result += chr((ord(ch) - base - shift) % 26 + base)
        else:
            result += ch
    return result

def score_text(text):
    # Score based on how "English-like" the words are
    words = text.split()
    return sum(zipf_frequency(word.lower(), "en") for word in words)

def brute_force_caesar(ciphertext, top_n=5):
    candidates = []
    for shift in range(1, 26):  # try all possible shifts
        decrypted = caesar_decrypt(ciphertext, shift)
        score = score_text(decrypted)
        candidates.append((shift, decrypted, score))
    
    # Sort by score (higher = more likely English)
    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates[:top_n]


# --- Main Program ---
cipher = input("Enter the ciphertext: ")

results = brute_force_caesar(cipher, top_n=5)

print("\nMost likely decryptions:")
for shift, text, score in results:
    print(f"Shift={shift}, Text='{text}', Score={score:.2f}")
