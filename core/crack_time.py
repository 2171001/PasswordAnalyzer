def estimate_crack_time(entropy, markov_score):
    guesses_per_second = 1e11

    # Base entropy compression
    effective_entropy = entropy * 0.5

    seconds = 2 ** effective_entropy / guesses_per_second

    # 🔥 Adjust based on predictability
    if markov_score > -80:
        seconds *= 0.001   # extremely predictable
    elif markov_score > -150:
        seconds *= 0.01
    elif markov_score > -250:
        seconds *= 0.1
    else:
        seconds *= 10      # highly random → harder

    return seconds