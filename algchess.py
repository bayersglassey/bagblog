
from typing import List, Dict, Tuple, Iterable


Location = Tuple[int, int]
LocationContents = str
Board = Dict[Location, LocationContents]


def unique_boards(boards: Iterable[Board]) -> List[Board]:
    """Since boards are dicts, and therefore unhashable, we can't pass
    them into sets.
    Instead, we have this function which finds unique boards.

        >>> for board in unique_boards([
        ...     {(0, 0): 'A'},
        ...     {(0, 0): 'B'},
        ...     {(0, 0): 'A'},
        ...     {(0, 0): 'C'},
        ... ]): print(board)
        {(0, 0): 'A'}
        {(0, 0): 'B'}
        {(0, 0): 'C'}

    """
    found = {}
    for board in boards:
        key = frozenset(board.items())
        if key in found:
            continue
        found[key] = board
    return list(found.values())


def parse_board(lines, x0=0, y0=0) -> Board:
    """

        >>> f = parse_board([
        ...     ' K ',
        ...     'P..',
        ... ], 10, 20)
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (11, 21): 'K'
        (10, 20): 'P'
        (11, 20): '.'
        (12, 20): '.'

    """
    f = {}
    if isinstance(lines, str):
        lines = lines.splitlines()
    h = len(lines)
    for _y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == ' ':
                continue
            y = h - _y - 1
            f[(x0 + x, y0 + y)] = c
    return f


def print_board(f: Board, *, file=None, border=True):
    """

        >>> print_board({})
        ++
        ++

        >>> print_board({
        ...     (0, 0): 'P',
        ...     (1, 0): '.',
        ...     (2, 0): '.',
        ...     (1, 1): 'K',
        ... })
        +---+
        | K |
        |P..|
        +---+

    """
    if not f:
        w = 0
        h = 0
        lines = []
    else:
        min_x = min(x for x, y in f)
        min_y = min(y for x, y in f)
        max_x = max(x for x, y in f)
        max_y = max(y for x, y in f)
        w = max_x - min_x + 1
        h = max_y - min_y + 1
        lines = []
        for y in range(h):
            lines.append(''.join(
                f.get((x + min_x, y + min_y), ' ')
                for x in range(w)))
        lines.reverse()
    if border:
        print('+' + '-' * w + '+', file=file)
    for line in lines:
        if border:
            line = f'|{line}|'
        print(line, file=file)
    if border:
        print('+' + '-' * w + '+', file=file)


class Movement:
    """A function mapping Location -> Location.
    These functions form a group (in the sense of group theory) and can be
    combined accordingly with the `*` operator.

        >>> m = Movement.identity()
        >>> print(m)
        1
        >>> print(m((10, 20)))
        (10, 20)

        >>> m = Movement.slide(1, -3)
        >>> print(m)
        r d^3
        >>> print(m((10, 20)))
        (11, 17)
        >>> print(m(m))
        r d^3 r d^3
        >>> print(m ** 2)
        r d^3 r d^3
        >>> print(m ** -1)
        l u^3
        >>> print(~m)
        l u^3

        >>> m = Movement.slide(-1, 0) * Movement.rotate(2)
        >>> print(m)
        l R^2
        >>> m((10, 20))
        (-9, -20)

    """

    def __init__(self, movements):
        # Each element is a tuple (x, y) or an int (i.e. rotation)
        self.movements = movements

    @staticmethod
    def _reverse(m):
        if isinstance(m, tuple):
            x, y = m
            return -x, -y
        elif isinstance(m, int):
            return -m
        else:
            raise ValueError(f"Unexpected: {m!r}")

    @staticmethod
    def identity() -> 'Movement':
        return Movement([])

    @staticmethod
    def slide(x, y) -> 'Movement':
        return Movement([(x, y)])

    @staticmethod
    def rotate(r) -> 'Movement':
        return Movement([r % 4])

    def __str__(self):
        parts = []
        for m in self.movements:
            if isinstance(m, tuple):
                x, y = m
                if x == 1:
                    parts.append('r')
                elif x == -1:
                    parts.append('l')
                elif x > 1:
                    parts.append(f'r^{x}')
                elif x < -1:
                    parts.append(f'l^{-x}')
                if y == 1:
                    parts.append('u')
                elif y == -1:
                    parts.append('d')
                elif y > 1:
                    parts.append(f'u^{y}')
                elif y < -1:
                    parts.append(f'd^{-y}')
            elif isinstance(m, int):
                if m == 1:
                    parts.append('R')
                elif m:
                    parts.append(f'R^{m}')
            else:
                raise ValueError(f"Unexpected: {m!r}")
        return '1' if not parts else ' '.join(parts)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.movements!r})'

    def __mul__(self, other):
        return self(other)

    def __invert__(self) -> 'Movement':
        return Movement(list(map(self._reverse, self.movements)))

    def __pow__(self, exp: int) -> 'Movement':
        movements = self.movements
        if exp < 0:
            movements = list(map(self._reverse, self.movements))
        return Movement(movements * abs(exp))

    def __call__(self, other):
        if isinstance(other, tuple):
            x, y = other
            for m in self.movements:
                if isinstance(m, tuple):
                    mx, my = m
                    x += mx
                    y += my
                elif isinstance(m, int):
                    for i in range(m):
                        # 90 degree counter-clockwise rotation
                        # (positive y points upwards)
                        x0 = x
                        x = -y
                        y = x0
                else:
                    raise ValueError(f"Unexpected: {m!r}")
            return x, y
        elif isinstance(other, set):
            return {self(x) for x in other}
        elif isinstance(other, dict):
            return {self(k): v for k, v in other.items()}
        elif isinstance(other, Movement):
            return Movement(self.movements + other.movements)
        else:
            raise TypeError(type(other))


def compose(*ff):
    def composite(x):
        for f in ff:
            x = f(x)
        return x
    return composite


def match(f: Board, g: Board, addx: int, addy: int) -> bool:
    """Is f a subset of g?"""
    return all(g.get((x + addx, y + addy)) == c for (x, y), c in f.items())


def find(f: Board, g: Board) -> List[Movement]:
    """Return all movements at which f is found as a subset of g

        >>> f = parse_board([
        ...     '.',
        ...     'p',
        ... ])

        >>> g = parse_board([
        ...     '....p',
        ...     '..p.p',
        ...     'p....',
        ... ])

        >>> for m in find(f, g): print(m)
        r^2 u
        1

    """
    if not f:
        # Would need to return the set of all movements!
        return ValueError("Can't search for empty board")

    # TODO: as an optimisation, try to pick an item for which c != '.'
    (x, y), c = next(iter(f.items()))

    return {
        Movement.slide(x2 - x, y2 - y)
        for (x2, y2), c2 in g.items()
        if c2 == c and match(f, g, x2 - x, y2 - y)}


def replace(f: Board, g: Board) -> Board:
    """

        >>> f = parse_board([
        ...     ' BC',
        ...     '  ',
        ... ])

        >>> g = parse_board([
        ...     '.A',
        ...     '..',
        ... ])

        >>> print_board(replace(f, g))
        +---+
        |.BC|
        |.. |
        +---+

    """
    h = g.copy()
    h.update(f)
    return h


def find_and_replace(f: Board, g: Board, h: Board) -> List[Board]:
    """

        >>> f = parse_board([
        ...     '.',
        ...     'p',
        ... ])

        >>> g = parse_board([
        ...     'p',
        ...     '.',
        ... ])

        Together, f and g represent the rule that you can move a pawn
        forward into an empty square of the chessboard.

        >>> h = parse_board([
        ...     '...',
        ...     '..p',
        ...     'p.p',
        ... ])

        >>> for b in find_and_replace(f, g, h): print_board(b)
        +---+
        |...|
        |p.p|
        |..p|
        +---+
        +---+
        |..p|
        |...|
        |p.p|
        +---+

    """
    return [replace(m(g), h) for m in find(f, h)]

