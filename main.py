from rich.console import Console
from rich.table import Table
from markov import Markov

markov = Markov.from_string("cloudy sunny cloudy rainy cloudy sunny cloudy cloudy")
console = Console()
table = Table(title="Markov Chain Events")
table.add_column("Relationship")
table.add_column("Probability")
for link in markov.get_links():
    table.add_row(f"{link.from_node.name} -> {link.node.name}", f"{link.weight:.3f}")
console.print(table)
