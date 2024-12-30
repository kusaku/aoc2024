from pathlib import Path


def parse_input(filename):
    lines = [line for line in Path(filename).read_text().strip().splitlines() if line.strip()]
    a = int(lines[0].split(":")[1].strip())
    b = int(lines[1].split(":")[1].strip())
    c = int(lines[2].split(":")[1].strip())
    program = list(map(int, lines[3].split(":")[1].strip().split(',')))

    return (a, b, c), program


def run_program(registers, program):
    a, b, c = registers
    ip = 0
    output = []

    def combo_value(operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return a
        elif operand == 5:
            return b
        elif operand == 6:
            return c
        return 0

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1] if ip + 1 < len(program) else 0

        if opcode == 0:  # adv - divide A by 2^(combo operand)
            denominator = 1 << combo_value(operand)
            a //= denominator
        elif opcode == 1:  # bxl - XOR B with literal operand
            b ^= operand
        elif opcode == 2:  # bst - set B to (combo operand) % 8
            b = combo_value(operand) % 8
        elif opcode == 3:  # jnz - jump to operand if A is non-zero
            if a != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc - XOR B with C
            b ^= c
        elif opcode == 5:  # out - output (combo operand) % 8
            output.append(combo_value(operand) % 8)
        elif opcode == 6:  # bdv - divide A by 2^(combo operand), result in B
            denominator = 1 << combo_value(operand)
            b = a // denominator
        elif opcode == 7:  # cdv - divide A by 2^(combo operand), result in C
            denominator = 1 << combo_value(operand)
            c = a // denominator
        else:
            break

        ip += 2

    return output


def part1():
    registers, program = parse_input("my_input.txt")
    result = run_program(registers, program)
    answer = ','.join(map(str, result))

    print(f"Answer: {answer}")


def part2():
    _, program = parse_input("my_input.txt")
    a, b, c = 1 << (3 * (len(program) - 1)), 0, 0
    result = [0] * len(program)

    while result != program:
        for pos in reversed(range(len(program))):
            if result[pos] != program[pos]:
                a += 1 << (3 * pos)
                result = run_program((a, b, c), program)

    print(f"Answer: {a}")


if __name__ == "__main__":
    part1()
    part2()
