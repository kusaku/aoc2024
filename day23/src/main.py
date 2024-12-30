from collections import defaultdict
from itertools import combinations
from pathlib import Path

def parse_input(filename):
    graph = defaultdict(set)

    for line in Path(filename).read_text().strip().splitlines():
        node1, node2 = line.split('-')
        graph[node1].add(node2)
        graph[node2].add(node1)

    return graph

def find_cliques(graph):
    # https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
    stack = [(set(), set(graph.keys()), set())]
    cliques = []

    while stack:
        current_clique, potential_nodes, excluded_nodes = stack.pop()

        if not potential_nodes and not excluded_nodes:
            cliques.append(current_clique)
            continue

        while potential_nodes:
            node = potential_nodes.pop()
            stack.append(
                (
                    current_clique | {node},
                    potential_nodes & graph[node],
                    excluded_nodes & graph[node]
                )
            )
            excluded_nodes.add(node)

    return cliques

def part1():
    graph = parse_input('my_input.txt')

    cliques = find_cliques(graph)
    triplets = {
        tuple(sorted(triplet))
        for clique in cliques if len(clique) >= 3
        for triplet in combinations(clique, 3)
        if any(node.startswith('t') for node in triplet)
    }

    print(f'Answer: {len(triplets)}')

def part2():
    graph = parse_input('my_input.txt')

    cliques = find_cliques(graph)
    largest_clique = sorted(max(cliques, key=len))

    print(f'Answer: {','.join(largest_clique)}')

if __name__ == '__main__':
    part1()
    part2()
