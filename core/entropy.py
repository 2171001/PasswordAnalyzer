import math
import re

def calculate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"[0-9]", password): pool += 10
    if re.search(r"[^\w\s]", password): pool += 50

    return len(password) * math.log2(pool) if pool else 0