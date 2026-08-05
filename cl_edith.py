from rich.console import Console
from rich.prompt import Prompt

console = Console()

def show_menu():
    console.print("\n[bold]Menu[/bold]")
    console.print("1) Starten")
    console.print("2) Instellingen")
    console.print("3) Afsluiten")

def main():
    while True:
        show_menu()
        choice = Prompt.ask("Kies een optie", choices=["1", "2", "3"], default="3")

        if choice == "1":
            console.print("[green]Je koos: Starten[/green]")
        elif choice == "2":
            console.print("[yellow]Je koos: Instellingen[/yellow]")
        elif choice == "3":
            console.print("[red]Afsluiten...[/red]")
            break

if __name__ == "__main__":
    main()
