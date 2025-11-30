import math
from collections import Counter

# --- Kasiski Examination ---
def kasiski_examination(ciphertext, min_len=3, max_len=5):
    ciphertext = ciphertext.lower()
    results = {}

    for L in range(min_len, max_len + 1):
        repeats = {}
        for i in range(len(ciphertext) - L + 1):
            seq = ciphertext[i:i + L]
            repeats.setdefault(seq, []).append(i)

        seq_infos = []
        for seq, positions in repeats.items():
            if len(positions) >= 2:
                dists = [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]
                if dists:
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

# --- Factor frequency from Kasiski GCDs ---
def gcd_factor_frequency(kasiski_results, max_factor=20):
    gcds = []
    for L in kasiski_results:
        for _, _, _, g in kasiski_results[L]:
            if g > 1:
                gcds.append(g)

    factor_counts = Counter()
    for g in gcds:
        for f in range(2, max_factor+1):
            if g % f == 0:
                factor_counts[f] += 1
    return factor_counts

# --- Main Program ---
def main():
    cipher = input("Enter ciphertext: ").lower().replace(" ", "")
    min_range = 1
    max_range = 5

    print("\n=== Vigenère Key Length Analysis ===")
    print(f"Ciphertext length: {len(cipher)}")
    print(f"Key length range: {min_range}-{max_range}\n")

    # Step 1: Kasiski Examination
    kasiski_results = kasiski_examination(cipher, min_len=3, max_len=5)
    print("Kasiski Examination Results:")
    if not kasiski_results:
        print("  No repeated sequences of length 3–5 found.\n")
    else:
        for L in sorted(kasiski_results.keys()):
            print(f"  For sequence length {L}:")
            for seq, positions, dists, g in kasiski_results[L]:
                print(f"    '{seq}' at positions {positions} → distances {dists}, GCD={g}")
        print()

        # Factor frequency table
        factor_counts = gcd_factor_frequency(kasiski_results, max_factor=max_range)
        print("Kasiski Factor Frequency (possible key lengths):")
        for f, count in sorted(factor_counts.items()):
            print(f"  Length {f}: occurs {count} times")
        print()

    # Step 2: Index of Coincidence
    likely_len, ic_values = guess_key_length(cipher, min_len=min_range, max_len=max_range)
    print("Index of Coincidence by assumed key length:")
    for k, ic in sorted(ic_values.items()):
        print(f"  Key length {k}: IC={ic:.4f}")
    print(f"\nLikely key length (IC-based): {likely_len}")

if __name__ == "__main__":
    main()
