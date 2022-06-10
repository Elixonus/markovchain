from markov import Markov, Node, Link

markov = Markov.from_string("a b c b b b a")
print(markov.nodes[1].links)