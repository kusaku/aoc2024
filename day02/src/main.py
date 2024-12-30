from itertools import pairwise
from pathlib import Path


def parse_input(filename):
    return [
        list(map(int, line.split()))
        for line
        in Path(filename).read_text().splitlines()
    ]


def is_report_safe(report):
    differences = [b - a for a, b in pairwise(report)]
    increasing = all(1 <= diff <= 3 for diff in differences)
    decreasing = all(-1 >= diff >= -3 for diff in differences)

    return increasing or decreasing


def is_report_safe_with_dampener(report):
    if is_report_safe(report):
        return True

    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1:]
        if is_report_safe(modified_report):
            return True

    return False


def part1():
    safe_reports = sum(is_report_safe(report) for report in parse_input('my_input.txt'))

    print(f'Answer: {safe_reports}')


def part2():
    safe_reports_with_dampener = sum(is_report_safe_with_dampener(report) for report in parse_input('my_input.txt'))

    print(f'Answer: {safe_reports_with_dampener}')


if __name__ == '__main__':
    part1()
    part2()
