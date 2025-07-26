import argparse
import itertools
import math
import string
import sys
from datetime import datetime
from typing import Dict, List, Set

try:
    from zxcvbn import zxcvbn   # pip install zxcvbn
except ImportError:
    zxcvbn = None  # Fallback if zxcvbn is not installed

LEET_MAP: Dict[str, str] = {
    "a": "4@",
    "b": "8",
    "e": "3",
    "g": "9",
    "i": "1!",
    "l": "1",
    "o": "0",
    "s": "$5",
    "t": "7+",
}

SYMBOLS = "!@#$%^&*()-_=+,.?"

def analyze_password(pwd: str) -> Dict[str, object]:
    if not pwd:
        raise ValueError("Password cannot be empty")

    if zxcvbn:
        result = zxcvbn(pwd)
        return {
            "score": result["score"],
            "entropy": 0.0,  # entropy not available in zxcvbn-python

            "crack_time_display": result["crack_times_display"]["offline_fast_hashing_1e10_per_second"],
            "suggestions": result["feedback"].get("suggestions", []),
        }
    else:
        pool_size = 0
        pools = [string.ascii_lowercase, string.ascii_uppercase, string.digits, SYMBOLS]
        for pool in pools:
            if any(ch in pool for ch in pwd):
                pool_size += len(pool)
        entropy = len(pwd) * math.log2(pool_size) if pool_size else 0
        score = 0
        if entropy >= 60:
            score = 4
        elif entropy >= 45:
            score = 3
        elif entropy >= 30:
            score = 2
        elif entropy >= 15:
            score = 1
        return {
            "score": score,
            "entropy": entropy,
            "crack_time_display": "N/A (offline estimate)",
            "suggestions": [
                "Use a mix of uppercase, lowercase, digits, and symbols",
                "Increase password length",
            ],
        }

def leet_variants(word: str) -> Set[str]:
    variants = {word}
    for idx, ch in enumerate(word.lower()):
        if ch in LEET_MAP:
            for sub in LEET_MAP[ch]:
                variants.add(word[:idx] + sub + word[idx + 1:])
    return variants

def generate_wordlist(words: List[str], leet: bool = True, years: bool = True) -> List[str]:
    cleaned = [w.strip() for w in words if w.strip()]
    base: Set[str] = set()
    for w in cleaned:
        base.update({w, w.lower(), w.capitalize(), w.upper()})
        if leet:
            base.update(leet_variants(w))

    combos: Set[str] = set(base)
    for a, b in itertools.combinations(base, 2):
        combos.add(a + b)
        combos.add(b + a)

    if years:
        current_year = datetime.now().year
        year_range = [str(y) for y in range(current_year - 40, current_year + 1)]
        for word in list(combos):
            for yr in year_range:
                combos.add(word + yr)
                combos.add(yr + word)

    return sorted(combos)

def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer & Wordlist Generator")
    sub = parser.add_subparsers(dest="command", required=True)

    p_analyze = sub.add_parser("analyze", help="Analyze password strength")
    p_analyze.add_argument("-p", "--password", required=True, help="Password to analyze")

    p_generate = sub.add_parser("generate", help="Generate custom wordlist")
    p_generate.add_argument("-w", "--words", required=True, help="Comma-separated keywords (e.g., name,birthday,pet)")
    p_generate.add_argument("-o", "--output", default="wordlist.txt", help="Output filename")
    p_generate.add_argument("--no-leet", action="store_true", help="Disable leetspeak variants")
    p_generate.add_argument("--no-years", action="store_true", help="Disable year combinations")

    args = parser.parse_args()

    if args.command == "analyze":
        result = analyze_password(args.password)
        print(f"Score         : {result['score']} / 4 (0 = Weak, 4 = Strong)")
        print(f"Entropy       : {result['entropy']:.2f} bits")
        print(f"Crack Time    : {result['crack_time_display']}")
        if result["suggestions"]:
            print("Suggestions   :")
            for suggestion in result["suggestions"]:
                print(f"  - {suggestion}")

    elif args.command == "generate":
        keywords = args.words.split(",")
        wordlist = generate_wordlist(keywords, leet=not args.no_leet, years=not args.no_years)
        try:
            with open(args.output, "w", encoding="utf-8") as file:
                for word in wordlist:
                    file.write(word + "\n")
            print(f"[+] Wordlist saved to {args.output} ({len(wordlist)} entries)")
        except Exception as e:
            print(f"[!] Failed to write file: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
