# Password Analyzer 🔐

**Password Analyzer** is a Python-based password security tool designed to evaluate password strength, identify common weaknesses, estimate theoretical cracking time, and generate strong passwords using cryptographically secure randomness.

Built as a cybersecurity project, it combines multiple password analysis techniques with an adaptive password generation workflow to encourage secure password practices.

## ✨ Features

- **Password Strength Analysis:** Evaluates passwords using entropy calculations, pattern detection, and Markov-model analysis.
- **Entropy Calculation:** Estimates password entropy based on character diversity and length.
- **Markov-Model Analysis:** Uses character-transition probabilities learned from a password dataset to identify potentially predictable sequences.
- **Pattern Detection:** Detects common sequences, repeated characters, dictionary words, and predictable leetspeak substitutions.
- **Crack-Time Estimation:** Calculates a theoretical cracking-time estimate using the project's entropy and predictability heuristics.
- **Adaptive Password Generation:** Generates candidate passwords and evaluates them against the analyzer's scoring system.
- **Cryptographically Secure Randomness:** Uses Python's `secrets` module to generate password characters and shuffle candidates.
- **Interactive Terminal Output:** Displays analysis metrics, detected weaknesses, a numerical score, and a final strength verdict using Rich.
- **Command-Line Interface:** Provides separate commands for password checking and generation.

## 🛠️ Technologies Used

- Python
- Poetry
- Rich
- Regular expressions
- Mathematical entropy calculations
- Markov models
- Python's `secrets` and `string` modules

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/password-analyzer.git
cd password-analyzer
```

Replace `YOUR_USERNAME` and the repository name with your actual GitHub details.

### 2. Install Poetry

If Poetry is not installed, follow the instructions at:

[https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)

### 3. Install project dependencies

```bash
poetry install
```

## 🚀 Usage

### Check a password

Run the following command to enter a password interactively:

```bash
poetry run python main.py check
```

Alternatively, provide a password as an argument:

```bash
poetry run python main.py check 'ExamplePassword123!'
```

**Security note:** Interactive entry is preferable because it avoids putting the password directly in shell history or exposing it in process arguments. Use only test passwords when experimenting with command-line arguments.

### Generate a strong password

```bash
poetry run python main.py generate
```

The generator creates candidate passwords, evaluates them using the analyzer, and aims to return a password that reaches the configured target score.

## 📊 Analysis Metrics

| Metric        | Description                                                                           |
| ------------- | ------------------------------------------------------------------------------------- |
| Entropy       | Estimates uncertainty based on password length and recognized character classes.      |
| Markov Score  | Measures the log-probability of character transitions according to the trained model. |
| Crack Time    | Provides a theoretical estimate derived from the project's cracking-time heuristic.   |
| Score         | Produces a numerical password-strength score from 0 to 100.                           |
| Final Verdict | Classifies the result as Very Weak, Weak, Moderate, Strong, or Very Strong.           |

### Password Strength Classification

- **0–29:** Very Weak
- **30–49:** Weak
- **50–69:** Moderate
- **70–84:** Strong
- **85–100:** Very Strong

The generator can use a stricter target than the general analyzer. For example, a target score of 95 requires generated candidates to achieve at least 95/100 under the configured scoring rules.

## 🧠 How It Works

1. The application accepts a password for analysis or starts the password generation workflow.
2. The analyzer calculates entropy and evaluates character-transition probabilities.
3. Pattern detection checks for common sequences, repeated characters, dictionary words, and predictable substitutions.
4. The scoring system combines the analysis results and applies penalties for identified weaknesses.
5. The application presents the metrics and assigns a final strength classification.
6. During generation, candidate passwords are evaluated until the configured acceptance condition is met.

## 🔒 Security Considerations

- Use unique passwords for every account.
- Prefer long, randomly generated passwords over predictable substitutions or familiar phrases.
- Store generated passwords in a reputable password manager.
- Never reuse real passwords when testing a development tool.
- Avoid exposing passwords through shell history, logs, screenshots, or public repositories.
- Do not treat a high score or a large estimated cracking time as proof that a password is unbreakable.

**Important:** The entropy, Markov score, and cracking-time calculations are project-specific heuristics. The Markov model's output depends on its training data, and its score is not a calibrated probability of an attacker guessing the password. A generated password's high internal score does not independently establish its real-world security.

## 🎯 Project Objective

The objective of Password Analyzer is to explore password-strength evaluation, probabilistic modeling, predictable-pattern detection, and secure password generation in a practical Python application.

The project also demonstrates how multiple analytical techniques can be combined in a command-line cybersecurity utility.

---

**Password Analyzer** — Analyze smarter. Generate stronger. Practice better password security.
