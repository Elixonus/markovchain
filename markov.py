from __future__ import annotations
from random import choices as random, randint
from itertools import pairwise
import cairo
import matplotlib.pyplot as plt
import numpy as np


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
            n1.links.append(Link(n2, 1))
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

    def render(self) -> None:
        width = 250 + 50 * len(self.get_links())
        height = 150 + 100 * len(self.nodes)

        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
        ctx = cairo.Context(surface)
        ctx.select_font_face("Arial")
        ctx.set_source_rgb(1, 0.8784, 0.6666)
        ctx.rectangle(0, 0, width, height)
        ctx.fill()

        ctx.translate(0.1 * width, 0)

        def draw_arrow(node1: Node, node2: Node, weight, arrow_number) -> None:
            # got to also make repeating cycles rendered on the side as circle
            ctx.translate(0, -10 * min(arrow_number, 4))
            ctx.move_to(0.5 * width + 10, 140 + 100 * self.nodes.index(node1))
            ctx.translate(-50 * arrow_number, 0)
            ctx.line_to(0.5 * width - 30, 140 + 100 * self.nodes.index(node1))
            ctx.line_to(0.5 * width - 30, 140 + 100 * self.nodes.index(node2))
            ctx.translate(50 * arrow_number, 0)
            ctx.line_to(0.5 * width + 10, 140 + 100 * self.nodes.index(node2))
            ctx.stroke()
            ctx.set_font_size(20)
            ctx.translate(-50 * arrow_number, 0)
            ctx.move_to(0.5 * width - 70, 140 + 100 * (self.nodes.index(node1) + self.nodes.index(node2)) / 2)
            ctx.show_text(f"{weight:.2f}")
            ctx.translate(50 * arrow_number, 0)
            ctx.translate(0, 10 * min(arrow_number, 4))
        for node in self.nodes:
            for l, link in enumerate(node.links):
                from random import random
                ctx.set_source_rgb(0.8 * (self.nodes.index(node) / (len(self.nodes) - 1)), 0, 0)
                ctx.set_line_width(5)
                draw_arrow(node, link.node, link.weight, self.nodes.index(node))
        ctx.set_font_size(40)
        for n, node in enumerate(self.nodes):
            text_width = ctx.text_extents(node.name).width
            ctx.rectangle(0.5 * width, 100 + 100 * n, text_width + 25, 50)
            ctx.set_source_rgb(1, 1, 1)
            ctx.fill_preserve()
            ctx.set_source_rgb(0, 0, 0)
            ctx.set_line_width(5)
            ctx.stroke()
            ctx.move_to(0.5 * width + 10, 140 + 100 * n)
            ctx.set_source_rgb(0, 0, 0)
            ctx.show_text(node.name)

        raw = surface.get_data().tolist()
        counter = 0
        image = np.empty((width, height, 3), dtype=np.uint8)
        for x in range(width):
            for y in range(height):
                for c in range(3):
                    image[x][y][2 - c] = raw[counter]
                    counter += 1
                counter += 1

        rolls = []
        roll = randint(0, len(self.nodes) - 1)
        for r in range(10):
            node = self.nodes[roll].get_node()
            roll = self.nodes.index(node)
            rolls.append(roll)

        fig, ax = plt.subplots()
        ax.plot(rolls)

        fig, ax = plt.subplots()
        ax.imshow(image)
        ax.set_title(f"Markov Chain for {len(self.nodes)} nodes")
        plt.show()


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
        for l1 in range(len(self.links)):
            for l2 in range(len(self.links) + 1, len(self.links)):
                link1 = self.links[l1]
                link2 = self.links[l2]
                if link1.node is link2.node:
                    link1.weight += link2.weight
                    del self.links[l2]
                    l2 -= 1


class Link:
    node: Node
    weight: float

    def __init__(self, node: Node, weight: float) -> None:
        self.node = node
        self.weight = weight

    def __repr__(self) -> str:
        return f"Link with node: #{id(self.node)} weight: {self.weight}"
