from core.markov import MarkovModel
from core.entropy import calculate_entropy
from core.patterns import detect_patterns
from core.crack_time import estimate_crack_time
import os
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress


# 🔹 Stream passwords instead of loading all
def stream_passwords(file_path):
    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            yield line.strip()


# 🔹 Initialize model
markov_model = MarkovModel()
#model_trained = False

MODEL_FILE = "data/markov_model.pkl"

# 🔹 Train only once (lazy loading)
def ensure_model():
    if os.path.exists(MODEL_FILE):
        # markov_model.load(MODEL_FILE)
        return

    if not os.path.exists("data/passwords.txt"):
        print("[red]Password dataset not found![/red]")
        return

    print("[yellow]Training Markov model...[/yellow]")

    markov_model.train(
        stream_passwords("data/passwords.txt"),
        limit=500000    # ⚡ prevent freezing
    )

    markov_model.save(MODEL_FILE)

    print("[green]Model ready.[/green]")


def format_time(seconds):
    if seconds < 1:
        return f"{seconds:.4f} sec"
    elif seconds < 60:
        return f"{seconds:.2f} sec"
    elif seconds < 3600:
        return f"{seconds/60:.2f} min"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hrs"
    else:
        return f"{seconds/86400:.2f} days"


def analyze(password, silent=False):
    ensure_model()

    entropy = calculate_entropy(password)

    if entropy > 100:
        entropy = 100 + (entropy - 100) * 0.3

    issues = detect_patterns(password)
    markov_score = markov_model.probability(password)

    crack_time = estimate_crack_time(entropy, markov_score)

    if markov_score > -80:
        crack_time *= 0.01
    elif markov_score > -150:
        crack_time *= 0.1

    # 🔥 scoring
    score = int((entropy / 160) * 100)

    if markov_score > -50:
        score -= 30
    elif markov_score > -100:
        score -= 15

    if len(password) > 20 and markov_score > -120:
        score -= 10

    score -= len(issues) * 10
    score = max(0, min(100, score))

    # 🧠 SILENT MODE EXIT
    if silent:
        return score

    # 🔥 UI starts here (clean block)
    print(Panel.fit(f"[bold cyan]Analyzing Password[/bold cyan]\n[white]{password}[/white]"))

    table = Table(title="Analysis Metrics")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="magenta")

    table.add_row("Entropy", f"{entropy:.2f}")
    table.add_row("Markov Score", f"{markov_score:.2f}")
    table.add_row("Crack Time", format_time(crack_time))
    table.add_row("Score", f"{score}/100")

    print(table)

    if issues:
        print("\n[bold red][!] Weaknesses Detected:[/bold red]")
        for issue in set(issues):
            print(f"[red]- {issue}[/red]")
    else:
        print("\n[bold green][✔] No obvious weaknesses found[/bold green]")

    print("\n[bold]Strength Indicator:[/bold]")
    with Progress() as progress:
        task = progress.add_task("[green]Evaluating...", total=100)
        progress.update(task, completed=score)

    if score < 30:
        verdict = "[bold red]Very Weak[/bold red]"
    elif score < 50:
        verdict = "[red]Weak[/red]"
    elif score < 70:
        verdict = "[yellow]Moderate[/yellow]"
    elif score < 85:
        verdict = "[green]Strong[/green]"
    else:
        verdict = "[bold green]Very Strong[/bold green]"

    print(f"\n[bold]Final Verdict:[/bold] {verdict}\n")