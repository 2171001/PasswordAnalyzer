import argparse
import getpass
from core.analyzer import analyze
from core.generator import generate_adaptive_password
from rich import print

def main():
    parser = argparse.ArgumentParser(description="Predator Password Analyzer")

    subparsers = parser.add_subparsers(dest="command")

    # 🔍 check command
    check_parser = subparsers.add_parser("check", help="Analyze a password")
    check_parser.add_argument("password", nargs="?", help="Password to analyze")

    # ⚡ generate command
    subparsers.add_parser("generate", help="Generate a strong password")

    args = parser.parse_args()

    # 🧠 CHECK FLOW
    if args.command == "check":
        if args.password:
            analyze(args.password)
        else:
            password = getpass.getpass("Enter password: ")
            analyze(password)

    # 🔥 GENERATE FLOW
    elif args.command == "generate":
        try:
            pwd, score = generate_adaptive_password(analyze)

            print("\n[+] Generated Password:", pwd)
            print(f"[green]Score Achieved:[/green] {score}/100")

            print("\n[bold cyan]Running internal validation...[/bold cyan]")
            analyze(pwd)

        except ValueError as e:
            print(f"\n[red]{e}[/red]")
            print("[yellow]Try increasing attempts or improving generator randomness[/yellow]")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()