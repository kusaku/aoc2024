use itertools::Itertools;
use std::collections::{HashMap, HashSet};
use std::fs;

type Graph<'a> = HashMap<&'a str, HashSet<&'a str>>;
type Clique<'a> = HashSet<&'a str>;

fn parse_input<'a>(data: &'a str) -> Graph<'a> {
    let mut graph: Graph = HashMap::new();

    for line in data.lines() {
        let parts: Vec<&str> = line.split('-').collect();
        let (node1, node2) = (parts[0], parts[1]);

        graph.entry(node1).or_insert_with(HashSet::new).insert(node2);
        graph.entry(node2).or_insert_with(HashSet::new).insert(node1);
    }

    graph
}

fn find_cliques<'a>(graph: &'a Graph<'a>) -> Vec<Clique<'a>> {
    // https://en.wikipedia.org/wiki/Bron–Kerbosch_algorithm
    let mut stack: Vec<(Clique, Clique, Clique)> = vec![(
        HashSet::new(),
        HashSet::from_iter(graph.keys().cloned()),
        HashSet::new(),
    )];
    let mut cliques = Vec::new();

    while let Some((current_clique, mut potential_nodes, mut excluded_nodes)) = stack.pop() {
        if potential_nodes.is_empty() && excluded_nodes.is_empty() {
            cliques.push(current_clique);
            continue;
        }

        for node in potential_nodes.clone() {
            let neighbors = &graph[&node];
            stack.push((
                &current_clique | &HashSet::from([node]),
                &potential_nodes & neighbors,
                &excluded_nodes & neighbors,
            ));
            potential_nodes.remove(node);
            excluded_nodes.insert(node);
        }
    }

    cliques
}

fn part1() {
    let data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let graph = parse_input(&data);

    let cliques = find_cliques(&graph);
    let mut triplets: HashSet<Vec<&str>> = HashSet::new();

    for clique in cliques.into_iter().filter(|clique| clique.len() >= 3) {
        for triplet in clique.into_iter().combinations(3) {
            if triplet.iter().any(|node| node.starts_with('t')) {
                triplets.insert(triplet.into_iter().sorted().collect());
            }
        }
    }

    println!("Answer: {}", triplets.len());
}

fn part2() {
    let data = fs::read_to_string("my_input.txt").expect("Failed to read input file");
    let graph = parse_input(&data);

    let cliques = find_cliques(&graph);
    let largest_clique = cliques.into_iter().max_by_key(|clique| clique.len()).unwrap();

    println!("Answer: {}", largest_clique.into_iter().sorted().join(","));
}

fn main() {
    part1();
    part2();
}
