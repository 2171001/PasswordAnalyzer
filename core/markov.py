import math
import pickle
from collections import defaultdict


class MarkovModel:
    def __init__(self):
        self.model = defaultdict(dict)
        self.totals = defaultdict(int)

    def train(self, password_iterator, limit=None):
        count = 0

        for pwd in password_iterator:
            pwd = pwd.strip()
            if not pwd:
                continue

            pwd = "^" + pwd.lower() + "$"

            for i in range(len(pwd) - 1):
                a, b = pwd[i], pwd[i + 1]

                # 🔥 FIX: manual increment (no defaultdict magic)
                if b not in self.model[a]:
                    self.model[a][b] = 0

                self.model[a][b] += 1
                self.totals[a] += 1

            count += 1
            if limit and count >= limit:
                break

    def probability(self, password):
        password = "^" + password.lower() + "$"
        log_prob = 0

        for i in range(len(password) - 1):
            a, b = password[i], password[i + 1]

            freq = self.model.get(a, {}).get(b, 0)
            total = self.totals.get(a, 0)

            # smoothing
            if total == 0:
                prob = 1e-6
            else:
                prob = freq / total if freq > 0 else 1e-6

            log_prob += math.log(prob)

        return log_prob

    # 💾 SAVE MODEL
    def save(self, path):
        with open(path, "wb") as f:
            pickle.dump((dict(self.model), dict(self.totals)), f)

    # 📂 LOAD MODEL
    def load(self, path):
        with open(path, "rb") as f:
            model, totals = pickle.load(f)

        # 🔥 restore as defaultdicts
        self.model = defaultdict(dict, model)
        self.totals = defaultdict(int, totals)