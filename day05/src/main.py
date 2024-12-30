from pathlib import Path


def parse_input(filename):
    rules_section, updates_section = Path(filename).read_text().strip().split('\n\n')

    rules = [
        tuple(map(int, line.split('|')))
        for line in rules_section.splitlines()
    ]

    updates = [
        list(map(int, line.split(',')))
        for line in updates_section.splitlines()
    ]

    return rules, updates


def is_order_correct(update, rules):
    positions = {page: i for i, page in enumerate(update)}
    for x, y in rules:
        if x in positions and y in positions:
            if positions[x] > positions[y]:
                return False
    return True


def get_middle_page(update):
    return update[len(update) // 2]


def sort_update(update, rules):
    graph = {page: set() for page in update}
    indegree = {page: 0 for page in update}

    for x, y in rules:
        if x in graph and y in graph:
            graph[x].add(y)
            indegree[y] += 1

    sorted_update = []
    stack = [page for page in update if indegree[page] == 0]

    while stack:
        current = stack.pop()
        sorted_update.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                stack.append(neighbor)

    return sorted_update


def part1():
    rules, updates = parse_input('my_input.txt')
    correct_middle_sum = 0

    for update in updates:
        if is_order_correct(update, rules):
            correct_middle_sum += get_middle_page(update)

    print(f"Answer: {correct_middle_sum}")


def part2():
    rules, updates = parse_input('my_input.txt')
    incorrect_middle_sum = 0

    for update in updates:
        if not is_order_correct(update, rules):
            corrected_update = sort_update(update, rules)
            incorrect_middle_sum += get_middle_page(corrected_update)

    print(f"Answer: {incorrect_middle_sum}")


if __name__ == "__main__":
    part1()
    part2()
