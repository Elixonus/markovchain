from __future__ import annotations
from random import choices as random, randint
from itertools import pairwise, combinations


class Markov:
    nodes: list[Node]

    def __init__(self, nodes: list[Node]) -> None:
        self.nodes = nodes

    def get_nodes(self) -> list[Node]:
        nodes = self.nodes.copy()
        return nodes

    def get_links(self) -> list[Link]:
        links = []
        for node in self.nodes:
            links.extend(node.links)
        return links

    def get_node(self, entry_node: int) -> Node:
        return self.nodes[entry_node].get_node()

    def get_link(self, entry_node: int) -> Link:
        return self.nodes[entry_node].get_link()

    @classmethod
    def from_string(cls, string: str) -> Markov:
        # node construction
        strings = string.split(" ")
        nodes = []
        for i, s in enumerate(strings):
            try:
                index = strings.index(s, 0, i)
            except ValueError:
                node = Node([], s)
            else:
                node = nodes[index]
            nodes.append(node)
        # link construction
        for i, (n1, n2) in enumerate(pairwise(nodes)):
            n1.links.append(Link(n2, 1, n1))
        # dirty link cleanup
        for node in nodes:
            node.merge()
        for node in nodes:
            node.normalize()
        # unique nodes only
        unique = []
        for node in nodes:
            if node not in unique:
                unique.append(node)
        return cls(unique)


class Node:
    links: list[Link]
    name: str | None

    def __init__(self, links: list[Link], name: str = None) -> None:
        self.links = links
        self.name = name

    def __repr__(self) -> str:
        if self.name is None:
            return f"Node with #{id(self)}"
        else:
            return f"Node \"{self.name}\" with #{id(self)}"

    def get_node(self) -> Node:
        node = random(self.links, weights=[link.weight for link in self.links])[0].node
        return node

    def get_link(self) -> Link:
        link = random(self.links, weights=[link.weight for link in self.links])[0]
        return link

    def normalize(self) -> None:
        total = sum(link.weight for link in self.links)
        for link in self.links:
            link.weight /= total

    def merge(self) -> None:
        removed_links = []
        for link1, link2 in combinations(self.links, 2):
            if link1.node is link2.node:
                link1.weight += link2.weight
                removed_links.append(link2)
        self.links = [link for link in self.links if link not in removed_links]


class Link:
    node: Node
    weight: float
    from_node: Node

    def __init__(self, node: Node, weight: float, from_node: Node) -> None:
        self.node = node
        self.weight = weight
        self.from_node = from_node

    def __repr__(self) -> str:
        return f"Link with node: #{id(self.node)} weight: {self.weight}"
