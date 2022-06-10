from rich.console import Console
from rich.table import Table
from markov import Markov, Node, Link

markov = Markov.from_string("a b c b b b a")
print(markov.nodes[1].links)

console = Console()

table = Table(title="Markov Chain Nodes")
table.add_column("Node Name")
table.add_column("Node ID")
for node in markov.get_nodes():
    table.add_row(f"{node.name}", f"N{id(node)}")
console.print(table)

table = Table(title="Markov Chain Links")
table.add_column("Link Relationship")
table.add_column("Link Probability")
table.add_column("Link ID")
for link in markov.get_links():
    table.add_row(f"{link.from_node.name} -> {link.node.name}", f"{link.weight:.3f}", f"L{id(link)}")
console.print(table)