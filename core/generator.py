import secrets
import string
import random

# 🔥 Character pools
LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits

# 💀 Rare + exotic symbols
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/`~₹€£¥µΩλ"
RARE_SAFE = "₹€£¥¢"

# 🔥 Dynamic charset selection
CHARSETS = [
    LOWER,
    UPPER,
    DIGITS,
    SYMBOLS,
    RARE_SAFE  # extra rare layer
]


def generate_password(length=None):
    # 🔥 FIX 1 — Random length (break entropy uniformity)
    if length is None:
        length = random.randint(16, 40)

    # 🔥 FIX 2 — Randomly pick character sets
    selected_sets = random.sample(CHARSETS, random.randint(3, len(CHARSETS)))
    pool = "".join(selected_sets)

    password = []

    # 🔥 Force diversity (but only from selected sets)
    for s in selected_sets:
        password.append(secrets.choice(s))

    # Fill remaining randomly
    for _ in range(length - len(password)):
        password.append(secrets.choice(pool))

    # 🔥 FIX 3 — Inject chaos (break Markov predictability)
    password = inject_noise(password)

    # 🔀 Shuffle
    secrets.SystemRandom().shuffle(password)

    return "".join(password)


# 🔥 NEW — Noise injector
def inject_noise(password):
    password = list(password)

    if len(password) < 8:
        return password

    # randomly replace ~25% chars with rare symbols
    noise_count = max(1, len(password) // 4)

    for i in random.sample(range(len(password)), noise_count):
        password[i] = secrets.choice("RARE_SAFE")

    return password


# 🔥 Adaptive generator (keep yours but improved)
def generate_adaptive_password(analyze_func, target_score=95):
    pwd = generate_password()
    score = analyze_func(pwd, silent=True)

    best_pwd = pwd
    best_score = score

    attempts = 0

    while best_score < target_score:
        attempts += 1

        new_pwd = mutate_password(best_pwd)
        new_score = analyze_func(new_pwd, silent=True)

        # 🔥 Only accept improvement
        if new_score > best_score:
            best_pwd = new_pwd
            best_score = new_score

        # 🧠 Escape local stagnation
        if attempts % 25 == 0:
            fresh_pwd = generate_password()
            fresh_score = analyze_func(fresh_pwd, silent=True)

            if fresh_score > best_score:
                best_pwd = fresh_pwd
                best_score = fresh_score

        if best_score > 90:
            # aggressive mutation for final push
            new_pwd = mutate_password(best_pwd + secrets.choice("₹€£¥!@#"))
    
    return best_pwd, best_score

def mutate_password(password):
    password = list(password)

    # 🔁 mutate ~30% positions
    for _ in range(max(1, len(password)//3)):
        i = random.randint(0, len(password)-1)
        password[i] = secrets.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*₹€£¥"
        )

    # ➕ insert rare symbols (controlled)
    if random.random() > 0.6:
        password.insert(
            random.randint(0, len(password)),
            secrets.choice("₹€£¥!@#$%^&*")
        )

    # 🔥 force entropy growth gradually (not explosion)
    if len(password) < 28:
        password.append(secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789₹€£¥"))

    # 🔀 shuffle
    secrets.SystemRandom().shuffle(password)

    return "".join(password)