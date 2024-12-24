from pathlib import Path


def parse_input(input_text):
    section_inputs, section_gates = input_text.split('\n\n')

    values = {
        input: int(value)
        for line in section_inputs.splitlines()
        for input, value in [line.split(': ')]
    }

    gates = {
        (op, in1, in2, out)
        for line in section_gates.splitlines()
        for inputs, out in [line.split(' -> ')]
        for op in ('AND', 'OR', 'XOR') if f' {op} ' in inputs
        for in1, in2 in [inputs.split(f' {op} ')]
    }

    return values, gates


def simulate(values, gates):
    remaining_gates = gates.copy()
    while ready_gates := {
        (op, in1, in2, out)
        for (op, in1, in2, out) in remaining_gates
        if in1 in values and in2 in values
    }:
        for gate in ready_gates:
            op, in1, in2, out = gate
            if op == 'AND':
                values[out] = values[in1] & values[in2]
            elif op == 'OR':
                values[out] = values[in1] | values[in2]
            elif op == 'XOR':
                values[out] = values[in1] ^ values[in2]

            remaining_gates.remove(gate)


def part1():
    input_text = Path('my_input.txt').read_text().strip()
    values, gates = parse_input(input_text)
    simulate(values, gates)
    z_values = {k: v for k, v in values.items() if k.startswith('z')}
    sorted_bits = [v for k, v in sorted(z_values.items())]
    binary_number = ''.join(map(str, sorted_bits[::-1]))
    print(f'Answer: {int(binary_number, 2)}')


def part2():
    input_text = Path('my_input.txt').read_text().strip()
    _, gates = parse_input(input_text)

    def out(s_op, s_in):
        for op, in1, in2, out in gates:
            if s_op == op and s_in in (in1, in2):
                return out

    def ins(s_out):
        for _, in1, in2, out in gates:
            if s_out == out:
                return {in1, in2}
        return {}

    # https://en.wikipedia.org/wiki/Adder_(electronics)#Full_adder
    # partN = xN XOR yN
    # fullN = xN AND yN
    # propN = partN AND carryN-1
    # carryN = fullN OR propN
    # sumN = partN XOR carryN-1 = zN

    max_bits = sum(1 for (*_, out) in gates if out.startswith('z'))
    swapped_outs = []
    carry_out = out('AND', 'x00')

    for bit_index in range(1, max_bits - 1):
        input, output = f'x{bit_index:02d}', f'z{bit_index:02d}'
        part_out = out('XOR', input)
        prop_out = out('AND', part_out) or out('AND', carry_out)
        sum_out = out('XOR', part_out) or out('XOR', carry_out)
        prev_sum_ins = ins(sum_out) | ins(prop_out)
        if carry_out not in prev_sum_ins:
            swapped_outs.append(carry_out)
        sum_out_ins = ins(sum_out)
        if part_out not in sum_out_ins:
            swapped_outs.append(part_out)
        expected_sum_out = {output}
        if sum_out not in expected_sum_out:
            swapped_outs.append(sum_out)
        full_out = out('AND', input)
        carry_out = out('OR', full_out) or out('OR', prop_out)
        carry_out_ins = ins(carry_out)
        if full_out not in carry_out_ins:
            swapped_outs.append(full_out)
        if prop_out not in carry_out_ins:
            swapped_outs.append(prop_out)

    print(f'Answer: {','.join(map(str, sorted(swapped_outs)))}')


if __name__ == '__main__':
    part1()
    part2()
