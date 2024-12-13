from pathlib import Path
from math import gcd

solve = lambda fn, off=0: print('Answer:', sum(
    (s[0] * 3 + s[1]) for a1, a2, b1, b2, p1, p2 in [
        (*map(int, blk.splitlines()[0].split('X+')[1].split(', Y+')),
        *map(int, blk.splitlines()[1].split('X+')[1].split(', Y+')),
        *map(int, blk.splitlines()[2].split('X=')[1].split(', Y=')))
        for blk in Path(fn).read_text().strip().split('\n\n')]
        if (d := a1 * b2 - a2 * b1) and
           (x := (p1 + off) * b2 - (p2 + off) * b1) % d == 0 and
           (y := (p1 + off - a1 * (x // d))) % b1 == 0 and
           (x := x // d) >= 0 and (y := y // b1) >= 0 and
           (s := (x, y))
))

if __name__ == '__main__':
    solve('my_input.txt')
    solve('my_input.txt', off=10_000_000_000_000)
