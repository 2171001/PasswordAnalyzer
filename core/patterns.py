import re

COMMON_PATTERNS = [
    r"qwerty"
]

def is_sequential(password):
    for i in range(len(password) - 3):
        chunk = password[i:i+4]

        # ascending
        if all(ord(chunk[j]) + 1 == ord(chunk[j+1]) for j in range(len(chunk)-1)):
            return True

        # descending
        if all(ord(chunk[j]) - 1 == ord(chunk[j+1]) for j in range(len(chunk)-1)):
            return True

    return False

def normalize_leetspeak(password):
    replacements = {
        "@": "a",
        "0": "o",
        "1": "i",
        "3": "e",
        "$": "s"
    }
    for k, v in replacements.items():
        password = password.replace(k, v)
    return password

def detect_patterns(password):
    issues = []

    if len(password) < 6:
        issues.append("Too short (minimum 6 characters required)")

    lower_pass = password.lower()

    # 🔥 Normalize ONCE
    normalized = normalize_leetspeak(lower_pass)

    # 🔍 Basic patterns
    for pattern in COMMON_PATTERNS:
        if re.search(pattern, lower_pass):
            issues.append(f"Pattern detected: {pattern}")

    if is_sequential(password):
        issues.append("Sequential characters")

    # 🔁 Repeated characters
    if re.search(r"(.)\1{2,}", password):
        issues.append("Repeated characters")

    # 📖 Direct dictionary words
    if re.search(r"(password|admin)", lower_pass):
        issues.append("Dictionary word")

    # 🔄 Predictable substitutions (ONLY if it's actually a word)
    for word in ["password", "admin", "login", "user"]:
        if word in normalized and word not in lower_pass:
            issues.append("Predictable substitutions")
            break

    # 🧠 Leetspeak dictionary detection
    if any(word in normalized for word in ["password", "admin"]):
        issues.append("Leetspeak dictionary word")

    # Keyboard pattern detection
    keyboard_patterns = ["qwerty", "asdf", "zxcv"]

    for pattern in keyboard_patterns:
        if pattern in lower_pass:
            issues.append("Keyboard pattern detected")

    return list(set(issues))