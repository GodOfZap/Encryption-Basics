import math
from collections import Counter
from wordfreq import zipf_frequency, top_n_list

# --- Improved Kasiski Examination ---
def kasiski_examination(ciphertext, min_len=3, max_len=5):
    """
    Return a dict:
      { seq_len: [ (sequence, [positions], [distances], gcd), ... ] }

    For each sequence length L in [min_len, max_len], we:
      - find all repeated L-grams,
      - record their positions,
      - compute distances between consecutive positions,
      - compute gcd of those distances.
    """
    ciphertext = ciphertext.lower()
    results = {}

    for L in range(min_len, max_len + 1):
        repeats = {}
        # record all positions of each L-gram
        for i in range(len(ciphertext) - L + 1):
            seq = ciphertext[i:i + L]
            repeats.setdefault(seq, []).append(i)

        seq_infos = []
        for seq, positions in repeats.items():
            if len(positions) >= 2:
                # distances between consecutive occurrences
                dists = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
                if len(dists) >= 1:
                    g = dists[0]
                    for d in dists[1:]:
                        g = math.gcd(g, d)
                    seq_infos.append((seq, positions, dists, g))
        if seq_infos:
            results[L] = seq_infos

    return results

# --- Index of Coincidence ---
def index_of_coincidence(text):
    freq = Counter([c for c in text if c.isalpha()])
    N = sum(freq.values())
    if N <= 1:
        return 0
    return sum(f * (f - 1) for f in freq.values()) / (N * (N - 1))

def guess_key_length(ciphertext, min_len=2, max_len=10):
    ic_values = {}
    for k in range(min_len, max_len + 1):
        groups = [''.join(ciphertext[i::k]) for i in range(k)]
        avg_ic = sum(index_of_coincidence(g) for g in groups if g) / k
        ic_values[k] = avg_ic
    likely = min(ic_values, key=lambda x: abs(ic_values[x] - 0.065))
    return likely, ic_values

# --- Vigenère Decrypt ---
def vigenere_decrypt(ciphertext, key):
    key = key.lower()
    plaintext = ""
    for i in range(len(ciphertext)):
        c = ord(ciphertext[i].lower()) - ord('a')
        k = ord(key[i % len(key)]) - ord('a')
        p = (c - k + 26) % 26
        plaintext += chr(p + ord('a'))
    return plaintext

# --- N-gram based scoring: works on continuous text (no spaces needed) ---
def score_text(text):
    """
    Higher score = more English-like.

    Strategy:
      - Normalize to lowercase letters only.
      - For all substring lengths n = 2..8, slide a window over the text.
      - For each n-gram, add zipf_frequency(ngram, "en").
      - Real English text contains many common short sequences that score > 0.
      - Random junk mostly hits near-0 frequencies.
    """
    text = ''.join(c for c in text.lower() if 'a' <= c <= 'z')
    ngram_min = 2
    ngram_max = 8

    N = len(text)
    if N < ngram_min:
        return -1e9  # hopelessly short / non-English

    total_score = 0.0

    for n in range(ngram_min, min(ngram_max, N) + 1):
        for i in range(N - n + 1):
            ngram = text[i:i + n]
            total_score += zipf_frequency(ngram, "en")

    return total_score

# --- Load many English words of a given length ---
def load_all_words(length=4, max_words=500000):
    all_words = top_n_list("en", max_words)
    return [w for w in all_words if len(w) == length and w.isalpha()]

# --- Main Program ---
def main():
    cipher = input("Enter ciphertext: ").lower().replace(" ", "")
    min_range = int(input("Enter minimum key length to test: "))
    max_range = int(input("Enter maximum key length to test: "))
    out_path = input("Enter output filename (e.g., results.txt): ").strip()

    candidates = []

    with open(out_path, "w", encoding="utf-8") as f:
        # Header
        f.write("=== Vigenère Analysis Output ===\n")
        f.write(f"Ciphertext: {cipher}\n")
        f.write(f"Key length range: {min_range}-{max_range}\n\n")

        # Step 1: Kasiski Examination (improved)
        kasiski_results = kasiski_examination(cipher, min_len=3, max_len=5)
        f.write("Kasiski Examination Results:\n")
        if not kasiski_results:
            f.write("  No repeated sequences of length 3–5 found.\n\n")
        else:
            for L in sorted(kasiski_results.keys()):
                f.write(f"  For sequence length {L}:\n")
                for seq, positions, dists, g in kasiski_results[L]:
                    f.write(
                        f"    '{seq}' at positions {positions} → "
                        f"distances {dists}, GCD={g}\n"
                    )
            f.write("\n")

        # Step 2: Index of Coincidence
        likely_len, ic_values = guess_key_length(cipher, min_len=2, max_len=10)
        f.write("Index of Coincidence by assumed key length (2–10):\n")
        for k, ic in sorted(ic_values.items()):
            f.write(f"  Key length {k}: IC={ic:.4f}\n")
        f.write(f"\nLikely key length (IC-based): {likely_len}\n\n")

        # Step 3: Candidate generation and scoring
        for key_len in range(min_range, max_range + 1):
            dictionary = load_all_words(length=key_len, max_words=500000)
            f.write(f"Loaded {len(dictionary)} words of length {key_len}. Scoring...\n")
            for key in dictionary:
                plain_guess = vigenere_decrypt(cipher, key)
                score = score_text(plain_guess)
                candidates.append((key, plain_guess, score))
            f.write("  Scoring complete.\n\n")

        # Sort and write all candidates to file
        candidates.sort(key=lambda x: x[2], reverse=True)
        f.write(f"Total candidates: {len(candidates)}\n\n")
        f.write("Candidates (sorted by score, highest first):\n")
        for key, plain, score in candidates:
            f.write(f"Key='{key}' → Plaintext='{plain}' (Score={score:.2f})\n")

    print(f"\nAll results saved to {out_path}")

if __name__ == "__main__":
    main()
