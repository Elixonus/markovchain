from rich.console import Console
from rich.table import Table
from markov import Markov

markov: Markov

while True:
    try:
        message = input("Input: ")
        split = message.split(" ")
        assert len(split) >= 2
        for s in split:
            assert len(s) >= 1
        markov = Markov.from_string(message)
        break
    except:
        print("Error try again.")
        continue

print()
console = Console()
table = Table(title="Markov Chain Events")
table.add_column("Relationship")
table.add_column("Probability")
for link in markov.get_links():
    table.add_row(f"{link.from_node.name} -> {link.node.name}", f"{link.weight:.3f}")
console.print(table)

input()
