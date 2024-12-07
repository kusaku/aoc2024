from pathlib import Path


def read_input(file_path):
    input_data = Path(file_path).read_text().strip()
    equations = []
    for line in input_data.splitlines():
        test_value, numbers = line.split(':')
        test_value = int(test_value.strip())
        numbers = list(map(int, numbers.strip().split()))
        equations.append((test_value, numbers))

    return equations


def evaluate_expression(numbers, operators):
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        elif op == '||':
            result = int(str(result) + str(numbers[i + 1]))

    return result


def is_valid_equation(test_value, numbers, allowed_operators):
    n = len(numbers) - 1
    k = len(allowed_operators)

    for i in range(k ** n):
        operators = []

        for _ in range(n):
            operators.append(allowed_operators[i % k])
            i //= k

        if evaluate_expression(numbers, operators) == test_value:
            return True

    return False


def calculate_total_calibration(file_path, allowed_operators):
    equations = read_input(file_path)
    total_calibration_result = 0
    total_equations = len(equations)
    completed = 0
    last_percent = -1

    for test_value, numbers in equations:
        if is_valid_equation(test_value, numbers, allowed_operators):
            total_calibration_result += test_value

        completed += 1
        percent = completed * 100 // total_equations
        if percent > last_percent:
            print(f'Progress: {percent}%', end='\r', flush=True)
            last_percent = percent

    print('\r\033[2K', end='')

    return total_calibration_result


def part1():
    result = calculate_total_calibration('my_input.txt', allowed_operators=['+', '*'])
    print(f'Answer: {result}')


def part2():
    result = calculate_total_calibration('my_input.txt', allowed_operators=['+', '*', '||'])
    print(f'Answer: {result}')


if __name__ == '__main__':
    part1()
    part2()
