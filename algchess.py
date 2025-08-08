"""This file contains an implementation of the algebra described in:
entries/2025/jul/algebra_of_chess.md

## Examples

Let's define the basic pawn move, forward to an empty square:

    >>> pawn_move_search = parse_board([
    ...     '.',
    ...     'p',
    ... ])

    >>> pawn_move_replace = parse_board([
    ...     'p',
    ...     '.',
    ... ])

    >>> pawn_move_rule = FindAndReplaceRule(pawn_move_search, pawn_move_replace)
    >>> print(pawn_move_rule)
    p;. -> .;p

Now let's see, on an example board fragment, all possible pawn moves:

    >>> board = parse_board([
    ...     '....',
    ...     '..K.',
    ...     'pppp',
    ...     '....',
    ... ])

    >>> for b in pawn_move_rule(board): print_board(b)
    +----+
    |....|
    |p.K.|
    |.ppp|
    |....|
    +----+
    +----+
    |....|
    |.pK.|
    |p.pp|
    |....|
    +----+
    +----+
    |....|
    |..Kp|
    |ppp.|
    |....|
    +----+

Now, let's see all valid moves consisting of moving a pawn, then moving a
pawn. Note that the two pawns don't need to be the same one!.. (we'll see
how to specify that later on.)

    >>> for b in (pawn_move_rule * pawn_move_rule)(board): print_board(b)
    +----+
    |....|
    |ppK.|
    |..pp|
    |....|
    +----+
    +----+
    |....|
    |p.Kp|
    |.pp.|
    |....|
    +----+
    +----+
    |p...|
    |..K.|
    |.ppp|
    |....|
    +----+
    +----+
    |....|
    |.pKp|
    |p.p.|
    |....|
    +----+
    +----+
    |.p..|
    |..K.|
    |p.pp|
    |....|
    +----+
    +----+
    |...p|
    |..K.|
    |ppp.|
    |....|
    +----+

Now let's give pawns the ability to take kings diagonally...

    >>> pawn_take_right_search = parse_board([
    ...     ' K',
    ...     'p',
    ... ])

    >>> pawn_take_right_replace = parse_board([
    ...     ' p',
    ...     '.',
    ... ])

    >>> pawn_take_right_rule = FindAndReplaceRule(pawn_take_right_search, pawn_take_right_replace)

    >>> pawn_take_left_search = parse_board([
    ...     'K',
    ...     ' p',
    ... ])

    >>> pawn_take_left_replace = parse_board([
    ...     'p',
    ...     ' .',
    ... ])

    >>> pawn_take_left_rule = FindAndReplaceRule(pawn_take_left_search, pawn_take_left_replace)

    >>> pawn_rule = OneOfRule([pawn_move_rule, pawn_take_right_rule, pawn_take_left_rule])
    >>> print(pawn_rule)
    (p;. -> .;p) | (p;rK -> .;rp) | (rp;K -> r.;p)

Now that pawns can either move forward or take kings diagonally, what are
all the valid moves from this position?..

    >>> board = parse_board([
    ...     '....',
    ...     '..K.',
    ...     'pppp',
    ...     '....',
    ... ])

    >>> for b in pawn_rule(board): print_board(b)
    +----+
    |....|
    |p.K.|
    |.ppp|
    |....|
    +----+
    +----+
    |....|
    |.pK.|
    |p.pp|
    |....|
    +----+
    +----+
    |....|
    |..Kp|
    |ppp.|
    |....|
    +----+
    +----+
    |....|
    |..p.|
    |p.pp|
    |....|
    +----+
    +----+
    |....|
    |..p.|
    |ppp.|
    |....|
    +----+

Now, let's see how to define rules which apply another rule repeatedly to
the *same* piece.
We'll use the special piece, '%', which means "the current piece of interest".
There is a special Rule subclass, PieceOfInterestRule, which chooses a piece
of interest, and then applies rules which can refer to that piece of interest
as '%'.

    >>> move_once_search = parse_board([
    ...     '.',
    ...     '%',
    ... ])

    >>> move_once_replace = parse_board([
    ...     '%',
    ...     '.',
    ... ])

    >>> move_once_rule = FindAndReplaceRule(move_once_search, move_once_replace)

    A rule which says we can move any given pawn forwards twice.
    >>> pawn_move_twice_rule = PieceOfInterestRule('p', move_once_rule ** 2)
    >>> print(pawn_move_twice_rule)
    %p: (%;. -> .;%){2}

    >>> board = parse_board([
    ...     '..K.',
    ...     '....',
    ...     'pppp',
    ...     '....',
    ... ])

    >>> for b in pawn_move_twice_rule(board): print_board(b)
    +----+
    |p.K.|
    |....|
    |.ppp|
    |....|
    +----+
    +----+
    |.pK.|
    |....|
    |p.pp|
    |....|
    +----+
    +----+
    |..Kp|
    |....|
    |ppp.|
    |....|
    +----+

How about rooks' ability to move forwards *one or more* times, until they hit
an obstacle?..
For this, we will use Rule.one_or_more(), which means repeat from 1 to infinity.

    >>> rook_move_rule = PieceOfInterestRule('R', move_once_rule.one_or_more())
    >>> print(rook_move_rule)
    %R: (%;. -> .;%)+

    >>> board = parse_board([
    ...     '....',
    ...     '...K',
    ...     '....',
    ...     'R..R',
    ... ])

    >>> for b in rook_move_rule(board): print_board(b)
    +----+
    |....|
    |...K|
    |R...|
    |...R|
    +----+
    +----+
    |....|
    |R..K|
    |....|
    |...R|
    +----+
    +----+
    |R...|
    |...K|
    |....|
    |...R|
    +----+
    +----+
    |....|
    |...K|
    |...R|
    |R...|
    +----+

"""
import re
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Tuple, Iterable, Optional, Union, FrozenSet
from typing import Callable, NamedTuple


MOVEMENT_REGEX = re.compile(r'[udlrR](?:\^-?\d+)?')
RULE_TOKEN_REGEX = re.compile('|'.join((
    r'[()|*+]',
    r'%.:',
    r'->',
    r'{.*?}',
    r'(?:[udlrR^0-9 *-]*)?[^(){}|*+:\->]+',
)))


Location = Tuple[int, int]
LocationContents = str
Board = Dict[Location, LocationContents]
BoardKey = FrozenSet[Tuple[Location, LocationContents]]


HighlightFunc = Callable[[str], str]
ansi_reverse = lambda s: f'\033[7m{s}\033[0m'


def get_player_bool_choice(msg) -> bool:
    """Gets input from the user, selecting True or False"""
    while True:
        print(msg)
        print("Choose ('y' or 'n'):")
        choice = None
        choice_text = input("> ").strip().lower()
        if choice_text in ('y', 'n'):
            return choice_text == 'y'
        print("### ERROR: Choice must be 'y' or 'n'")


def get_player_choice(choices, *, msg=None):
    """Gets input from the user, selecting one of a number of choices"""

    if isinstance(choices, list):
        labels = choices
        values = choices
    elif isinstance(choices, dict):
        labels = choices
        values = list(choices.values())
    else:
        raise TypeError(type(choices))

    if not choices:
        return None
    elif len(choices) == 1:
        return values[0]

    if msg is None:
        msg = "Choose an option:"

    while True:
        print(msg)
        for i, label in enumerate(labels, 1):
            label = str(label)
            if '\n' in label:
                label_indented = '\n'.join('    ' + line for line in label.splitlines())
                print(f" {i}:\n{label_indented}")
            else:
                print(f" {i}: {label}")
        choice = None
        choice_text = input("> ")
        try:
            choice = int(choice_text)
        except ValueError:
            pass
        if choice is None or choice < 1 or choice > len(choices):
            print(f"### ERROR: Choice must be a number in the range 1..{len(choices)}")
        else:
            return values[choice - 1]


def get_board_key(board: Board) -> BoardKey:
    """Returns a hashable representation of a Board"""
    return frozenset(board.items())


def get_board_bounds(board: Board) -> Tuple[int, int, int, int]:
    if not board:
        return 0, 0, 0, 0
    min_x = min(x for x, y in board)
    min_y = min(y for x, y in board)
    max_x = max(x for x, y in board)
    max_y = max(y for x, y in board)
    return min_x, min_y, max_x, max_y


def replace_piece(p0: LocationContents, p1: LocationContents, board: Board, inplace=True) -> Board:
    """Replace p0 with p1 in the given board"""
    if inplace:
        for k, p in board.items():
            if p == p0:
                board[k] = p1
        return board
    else:
        return {k: p1 if p == p0 else p
            for k, p in board.items()}


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
        key = get_board_key(board)
        if key in found:
            continue
        found[key] = board
    return list(found.values())


def parse_movement(text: str) -> 'Movement':
    """Parses a Movement from the given text

        >>> print(parse_movement('1'))
        1

        >>> print(parse_movement('u'))
        u

        >>> print(parse_movement('uu'))
        u u

        >>> print(parse_movement('u^2'))
        u^2

        >>> print(parse_movement('u^-2'))
        d^2

        >>> print(parse_movement('u^2 d^0'))
        u^2

        >>> print(parse_movement('u^2 R'))
        u^2 R

        >>> print(parse_movement('u^2 R^4'))
        u^2

    """
    mm = []
    for part in MOVEMENT_REGEX.findall(text):
        c = part[0]
        if c == '1':
            continue
        if '^' in part:
            n = int(part[2:])
            if n == 0:
                continue
        else:
            n = 1
        if c == 'u':
            mm.append((0, n))
        elif c == 'd':
            mm.append((0, -n))
        elif c == 'l':
            mm.append((-n, 0))
        elif c == 'r':
            mm.append((n, 0))
        elif c == 'R':
            n = n % 4
            if n == 0:
                continue
            mm.append(n)
        else:
            raise Exception(f"Unexpected: {c!r}")
    return Movement(mm)


def parse_board(lines_or_text, x0=0, y0=0) -> Board:
    """Parses a board from the given text (or lines of text)

        >>> f = parse_board([
        ...     ' K ',
        ...     'P..',
        ... ], 10, 20)
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (11, 21): 'K'
        (10, 20): 'P'
        (11, 20): '.'
        (12, 20): '.'

        >>> f = parse_board('P..;rK', 10, 20)
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (10, 20): 'P'
        (11, 20): '.'
        (12, 20): '.'
        (11, 21): 'K'

        >>> f = parse_board('0.0; .0.; 0.0', 10, 20)
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (11, 20): '.'
        (10, 21): '.'
        (12, 21): '.'
        (11, 22): '.'

        >>> f = parse_board('.[.p].')
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (0, 0): '.'
        (1, 0): '.p'
        (2, 0): '.'

        >>> f = parse_board('.[^.p].')
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (0, 0): '.'
        (1, 0): '^.p'
        (2, 0): '.'

        >>> f = parse_board('l^2 * .p')
        >>> for k, v in f.items(): print(f'{k!r}: {v!r}')
        (-2, 0): '.'
        (-1, 0): 'p'

    """
    f = {}
    if isinstance(lines_or_text, str):
        text = lines_or_text

        if '*' in text:
            parts = text.split('*')
            text = parts.pop()
            m_text = ''.join(parts)
            x0, y0 = parse_movement(m_text)((x0, y0))

        x = x0
        y = y0
        it = iter(text)
        for c in it:
            if c in (' ', '1'):
                continue
            elif c == '[':
                cc = ''
                for c in it:
                    if c == ']':
                        break
                    else:
                        cc += c
                f[(x, y)] = cc
                x += 1
            elif c == ';':
                x = x0
                y += 1
            elif c == 'u':
                y += 1
            elif c == 'd':
                y -= 1
            elif c == 'l':
                x -= 1
            elif c == 'r':
                x += 1
            elif c == '0':
                x += 1
            else:
                f[(x, y)] = c
                x += 1
    else:
        lines = lines_or_text
        h = len(lines)
        for _y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == ' ':
                    continue
                y = h - _y - 1
                f[(x0 + x, y0 + y)] = c
    return f


def square_repr(square: LocationContents) -> str:
    """Algebraic representation of a single square's contents within a Board"""
    if square[0] == '^':
        return f'[^{square[1:]}]'
    elif len(square) > 1:
        return f'[{square}]'
    else:
        return square


def board_repr(f: Board) -> str:
    """Returns a string representation of a board, suitable for use with
    parse_board

        >>> board = {
        ...     (0, 0): 'P',
        ...     (1, 0): '.',
        ...     (2, 0): '.',
        ...     (1, 1): 'K',
        ... }

        >>> for i in range(4):
        ...     print(board_repr(Movement.rotate(i) * board))
        P..;rK
        l^2 * rP;K.;r.
        l^3 d^2 * rK;..P
        d^3 * .;.K;P

        >>> board = {
        ...     (0, 0): '.',
        ...     (1, 0): '.p',
        ...     (2, 0): '.',
        ... }
        >>> print(board_repr(board))
        .[.p].

        >>> board = {
        ...     (0, 0): '.',
        ...     (1, 0): '^.p',
        ...     (2, 0): '.',
        ... }
        >>> print(board_repr(board))
        .[^.p].

    """
    if not f:
        return '0'
    min_x, min_y, max_x, max_y = get_board_bounds(f)
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    lines = []
    for y in range(min_y, max_y + 1):
        line = ''.join(
            square_repr(f.get((x, y), 'r'))
            for x in range(min_x, max_x + 1))
        lines.append(line.rstrip('r'))
    s = ';'.join(lines)
    if min_x != 0 or min_y != 0:
        s = f'{Movement.slide(min_x, min_y)} * {s}'
    return s


def get_board_lines(
        board: Board,
        *,
        file=None,
        border=True,
        highlights: Union[Iterable[Location], Dict[Location, HighlightFunc]] = (),
        str_join=''.join, # hack, so you can pass curtsies.FmtStr's join
        ) -> List[str]:
    """The innards of print_board"""
    if not board:
        w = 0
        h = 0
        lines = []
    else:
        if isinstance(highlights, dict):
            highlight_funcs = highlights
        else:
            highlights = set(highlights)
            highlight_funcs = {}
        min_x, min_y, max_x, max_y = get_board_bounds(board)
        w = max_x - min_x + 1
        h = max_y - min_y + 1
        lines = []
        def _square_repr(square, x, y):
            s = square_repr(square)
            if (x, y) in highlights:
                func = highlight_funcs.get((x, y), ansi_reverse)
                return func(s)
            else:
                return s
        for y in range(min_y, max_y + 1):
            lines.append(str_join(
                _square_repr(board.get((x, y), ' '), x, y)
                for x in range(min_x, max_x + 1)))
        lines.reverse()
    if border:
        lines = [f'|{line}|' for line in lines]
        border_line = '+' + '-' * w + '+'
        lines.insert(0, border_line)
        lines.append(border_line)
    return lines


def print_board(board: Board, *, file=None, **kwargs):
    """Prints the given board, in a format suitable for use with parse_board
    (if passed to it as a list of strings, one per line)

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
    lines = get_board_lines(board, **kwargs)
    for line in lines:
        print(line, file=file)


def parse_rule(text: str, *, debug=False) -> 'Rule':
    """Parses a Rule, should be more or less the inverse of Rule.__str__

        >>> print(parse_rule('(p;. -> .;p) | (p;rK -> .;rp) | (rp;K -> r.;p)'))
        (p;. -> .;p) | (p;rK -> .;rp) | (rp;K -> r.;p)

        >>> print(parse_rule('%p: (%;. -> .;%)(%;. -> .;%)'))
        %p: (%;. -> .;%)(%;. -> .;%)

        >>> print(parse_rule('%p: (.;% -> r^2 * %;.)+'))
        %p: (.;% -> r^2 * %;.)+

    """
    tokens = [token for token in RULE_TOKEN_REGEX.findall(text)
        if token.strip()]
    depth = 0
    token_i = 0
    debug_print = lambda msg: None
    if debug:
        def debug_print(msg):
            print('  ' * depth + msg)
    def get_token():
        nonlocal token_i
        _token_i = token_i
        if token_i >= len(tokens):
            token = None
        else:
            token = tokens[token_i]
            token_i += 1
        debug_print(f"get_token @{_token_i}: {token!r}")
        return token
    def unget():
        nonlocal token_i
        token_i -= 1
        debug_print(f"unget @{token_i}: {tokens[token_i]!r}")
    def expect(expected):
        actual = get_token()
        if actual != expected:
            raise Exception(f"Expected {expected!r}, got {actual!r}")
    def _parse(*, no_binops=False):
        # Recursive parse step...

        nonlocal depth
        depth += 1

        token = get_token()
        if token is None:
            raise Exception("Unexpected end of string")
        elif token == '(':
            rule = _parse()
            expect(')')
        elif token[-1] == ':' and token[0] == '%' and len(token) == 3:
            piece = token[1]
            rule = _parse()
            rule = PieceOfInterestRule(piece, rule)
        else:
            board_left_token = token
            board_left = parse_board(board_left_token)
            token = get_token()
            if token != '->':
                raise Exception(f"Expected '->' after {board_left_token!r}, got {token!r}")
            token = get_token() or ''
            board_right = parse_board(token)
            rule = FindAndReplaceRule(board_left, board_right)

        # Handle repetition suffixes
        token = get_token()
        if token is None:
            pass
        elif token == '?':
            rule = rule.optionally()
        elif token == '*':
            rule = rule.zero_or_more()
        elif token == '+':
            rule = rule.one_or_more()
        elif token[0] == '{':
            token = token.strip('{}')
            if ',' in token:
                lhs, rhs = token.split(',')
                n = int(lhs)
                m = None if not rhs.strip() else int(rhs)
            else:
                n = m = int(token)
            rule = rule.between(n, m)
        else:
            unget()

        if no_binops:
            depth -= 1
            return rule

        # Handle binary operators on rules
        while True:
            while True:
                token = get_token()
                if token in (None, ')'):
                    depth -= 1
                    if token == ')':
                        unget()
                    return rule
                elif token == '(':
                    rhs = _parse(no_binops=True)
                    expect(')')
                    rule *= rhs
                else:
                    break
            if token == '|':
                rhs = _parse(no_binops=True)
                rule |= rhs
            else:
                break
    return _parse()


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

        >>> for i in range(4):
        ...     print(Movement.rotate(i) * {(0, 0): 'p'})
        {(0, 0): 'p'}
        {(-1, 0): 'p'}
        {(-1, -1): 'p'}
        {(0, -1): 'p'}

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
    def slide(x: int = 0, y: int = 0) -> 'Movement':
        return Movement([(x, y)])

    @staticmethod
    def rotate(r: int = 1) -> 'Movement':
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

    def __call__(self, other, *, square=False):
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
                        if square:
                            # We aren't rotating a point, we're rotating
                            # a board square, whose centre is its bottom-left
                            # corner.
                            x -= 1
                else:
                    raise ValueError(f"Unexpected: {m!r}")
            return x, y
        elif isinstance(other, list):
            return [self(x) for x in other]
        elif isinstance(other, dict):
            return {self(k, square=True): v for k, v in other.items()}
        elif isinstance(other, Movement):
            return Movement(self.movements + other.movements)
        elif isinstance(other, Rule):
            return other._distribute(self)
        elif isinstance(other, str):
            # Allows movements to be applied to e.g. PieceOfInterestRule.piece
            return other
        else:
            raise TypeError(type(other))


def match(f: Board, g: Board, addx: int, addy: int) -> bool:
    """Is f a subset of g?"""
    return all(
        (g.get((x + addx, y + addy), '<notfound>') in c) ^ (c[0] == '^')
        for (x, y), c in f.items())


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
        raise ValueError("Can't search for empty board")

    c = None
    for k, _c in f.items():
        if _c[0] == '^':
            # Can't match on a negative pattern, since there would be
            # infinite matches
            continue
        c = _c
        if len(c) == 1 and c != '.':
            # We prefer single-character matches, since those are easier to
            # check for.
            # We prefer non-'.' matches, since those are probably more likely
            # to occur (i.e. in most board games, most of the board is empty).
            break
    if c is None:
        raise ValueError(f"Can't search for board: {board_repr(f)}")
    x, y = k

    return [
        Movement.slide(x2 - x, y2 - y)
        for (x2, y2), c2 in g.items()
        if c2 in c and match(f, g, x2 - x, y2 - y)]


def replace(f: Board, g: Board, *, in_place=False) -> Board:
    """Return g with part of it replaced by f.

        >>> f = parse_board([
        ...     ' BC',
        ...     ' C',
        ... ])

        >>> g = parse_board([
        ...     '.A',
        ...     '..',
        ... ])

        >>> print_board(replace(f, g))
        +---+
        |.BC|
        |.C |
        +---+

        >>> print_board(replace(g, f))
        +---+
        |.AC|
        |.. |
        +---+

    """
    h = g if in_place else g.copy()
    h.update(f)
    return h


def delete(f, kk):
    """Deletes locations from a board"""
    pop = f.pop
    for k in kk:
        pop(k, None)
    return f


def find_and_replace(f: Board, g: Board, h: Board) -> List[Board]:
    """Returns all possible boards which are like h with f replaced by g.

        >>> f = parse_board([
        ...     '.',
        ...     'p',
        ... ])

        >>> g = parse_board([
        ...     'p',
        ...     '.',
        ... ])

        >>> h = parse_board([
        ...     '...',
        ...     '..p',
        ...     'p.p',
        ... ])

        >>> for b in find_and_replace(f, {}, h): print_board(b)
        +---+
        |.. |
        |.. |
        |p.p|
        +---+
        +---+
        |...|
        | .p|
        | .p|
        +---+

        >>> for b in find_and_replace(f, g, h): print_board(b)
        +---+
        |..p|
        |...|
        |p.p|
        +---+
        +---+
        |...|
        |p.p|
        |..p|
        +---+

    """
    return [
        replace(
            m(g),
            delete(h.copy(), (m(k) for k in f)),
            in_place=True)
        for m in find(f, h)]


def board_diff(b1: Board, b2: Board) -> List[Location]:
    """Returns a list of locations whose contents changed between b1 and b2

        >>> b1 = parse_board('ppp;...')
        >>> for k, v in b1.items(): print(f'{k}: {v}')
        (0, 0): p
        (1, 0): p
        (2, 0): p
        (0, 1): .
        (1, 1): .
        (2, 1): .

        >>> b2 = parse_board('.0.;p.p;0p')
        >>> for k, v in b2.items(): print(f'{k}: {v}')
        (0, 0): .
        (2, 0): .
        (0, 1): p
        (1, 1): .
        (2, 1): p
        (1, 2): p

        >>> for k in board_diff(b1, b2): print(k)
        (0, 0)
        (1, 0)
        (2, 0)
        (0, 1)
        (2, 1)
        (1, 2)

    """
    # Locations in b1 which were removed or modified in b2:
    kk = [k for k, v in b1.items() if b2.get(k) != v]
    # Locations in which were added in b2:
    kk += [k for k in b2 if k not in b1]
    return kk


class Rule(metaclass=ABCMeta):
    """A rule is a function which maps a board to a set of possible boards,
    i.e. a set of possible "moves" a player might make, taking the board
    from one position to another.

    This is an abstract base class; only its subclasses should be
    instantiated.
    """

    def __init__(self):
        raise NotImplementedError("To be implemented by subclasses")

    def __eq__(self, other):
        return isinstance(other, Rule) and (self is other or str(self) == str(other))

    def to_user_choice_repr(self) -> str:
        return self.prettystring(hide_poi=True)

    def prettystring(self, *, hide_poi=False, indentmode=0) -> str:
        """

            >>> rule = OneOfRule([
            ...     PieceOfInterestRule('♖', OneOfRule([
            ...         parse_rule('%;. -> .;%').one_or_more(),
            ...         parse_rule('%;. -> .;%').zero_or_more() * parse_rule(f'%;♟ -> .;%')
            ...     ])),
            ...     PieceOfInterestRule('♗', OneOfRule([
            ...         parse_rule('%;l. -> .;l%').one_or_more(),
            ...         parse_rule('%;l. -> .;l%').zero_or_more() * parse_rule(f'%;l♟ -> .;l%')
            ...     ])),
            ... ])

            >>> print(rule.prettystring())
            (%♖: ((%;. -> .;%)+) |
             (((%;. -> .;%)*)(%;♟ -> .;%))) |
            (%♗: ((r%;. -> r.;%)+) |
             (((r%;. -> r.;%)*)(r%;♟ -> r.;%)))

            >>> rule = parse_rule('%p: ((. -> %)(. -> %) | (. -> %) | (. -> %))')

            >>> print(rule.prettystring(indentmode=1))
            %p: (
              (
                . -> %
              )(
                . -> %
              )
            ) | (
              . -> %
            ) | (
              . -> %
            )

        """
        as_str = str(self)

        if hide_poi:
            rhs = as_str
            as_str = ''
            while ':' in rhs:
                lhs, rhs = rhs.split(':', 1)
                depth = 0
                for i, c in enumerate(rhs):
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
                        if depth < 0:
                            break
                rhs = rhs[i:]
                as_str += f'{lhs}: ...'
            as_str += rhs

        depth = 0
        lines = []
        if indentmode == 0:
            parts = as_str.split(' | ')
            last_part_i = len(parts) - 1
            for part_i, part in enumerate(parts):
                spaces = ' ' * depth
                line = spaces + part
                if part_i < last_part_i:
                    line += ' |'
                lines.append(line)
                for c in part:
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
        elif indentmode == 1:
            for i, part in enumerate(as_str.split('(')):
                if i:
                    if lines and '(' not in lines[-1]:
                        lines[-1] += '('
                    else:
                        lines.append('  ' * depth + '(')
                    depth += 1
                for j, subpart in enumerate(part.split(')')):
                    line = ''
                    if j:
                        depth -= 1
                        line += ')'
                    if subpart:
                        line += subpart
                    if line:
                        lines.append('  ' * depth + line)
        else:
            raise ValueError(f"Bad indentmode: {indentmode!r}")
        return '\n'.join(lines)

    @staticmethod
    def identity() -> 'Rule':
        return FindAndReplaceRule({}, {})

    def __or__(self, other: 'Rule') -> 'OneOfRule':
        if isinstance(other, OneOfRule):
            rules = other.rules.copy()
            rules.insert(0, self)
            return OneOfRule(rules)
        return OneOfRule([self, other])

    def __mul__(self, other: 'Rule') -> 'SequentialRule':
        if isinstance(other, SequentialRule):
            rules = other.rules.copy()
            rules.insert(0, self)
            return SequentialRule(rules)
        return SequentialRule([self, other])

    def __pow__(self, exp: int) -> 'RepeatRule':
        return self.repeat(exp)

    def optionally(self, **kwargs) -> 'RepeatRule':
        return RepeatRule(self, 0, 1, **kwargs)

    def zero_or_more(self, **kwargs) -> 'RepeatRule':
        return RepeatRule(self, 0, **kwargs)

    def one_or_more(self, **kwargs) -> 'RepeatRule':
        return RepeatRule(self, 1, **kwargs)

    def repeat(self, n: int, **kwargs) -> 'RepeatRule':
        return RepeatRule(self, n, n, **kwargs)

    def between(self, at_least: int, at_most: Optional[int] = None, **kwargs) -> 'RepeatRule':
        # NOTE: an at_most of None is interpreted as infinity
        return RepeatRule(self, at_least, at_most, **kwargs)

    def __call__(self, boards: Union[Board, Iterable[Board]]) -> List[Board]:
        if isinstance(boards, dict):
            return unique_boards(self._apply(boards))
        else:
            return unique_boards(
                out_board
                for board in boards
                for out_board in self._apply(board))

    @abstractmethod
    def _apply(self, board: Board) -> List[Board]: ...

    @abstractmethod
    def _player_choice(self, board: Board) -> Optional[Board]: ...

    @abstractmethod
    def _distribute(self, m: Movement) -> 'Rule': ...


class FindAndReplaceRule(Rule):
    """A rule which consists of finding a given board fragment (the "pattern")
    and replacing it with another (the "replacement").
    """

    def __init__(self, pattern: Board, replacement: Board, *, raw=False):

        if not raw:
            # Apply the same movement to pattern & replacement, such that
            # the rule's behaviour remains the same, but its string
            # representation becomes a bit cleaner (contains fewer movements)
            pattern_bounds = get_board_bounds(pattern)
            replacement_bounds = get_board_bounds(replacement)
            min_x = min(pattern_bounds[0], replacement_bounds[0])
            min_y = min(pattern_bounds[1], replacement_bounds[1])
            if min_x or min_y:
                pattern = {(x - min_x, y - min_y): v
                    for (x, y), v in pattern.items()}
                replacement = {(x - min_x, y - min_y): v
                    for (x, y), v in replacement.items()}

        self.pattern = pattern
        self.replacement = replacement

    def __str__(self):
        return f'{board_repr(self.pattern)} -> {board_repr(self.replacement)}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.pattern!r}, {self.replacement!r})'

    def _apply(self, board: Board) -> List[Board]:
        if not self.pattern and not self.replacement:
            # Identity rule
            return [board]
        return find_and_replace(self.pattern, self.replacement, board)

    def _player_choice(self, board: Board) -> Optional[Board]:
        print(f"Matching find-and-replace rule: {self.to_user_choice_repr()}")
        if not self.pattern and not self.replacement:
            # Identity rule
            return board
        movements = find(self.pattern, board)
        locations = [m * (0, 0) for m in movements]
        print("...matched at locations:")
        print_board(board, highlights=locations)
        movement = get_player_choice(movements, msg="Choose a location at which to apply the replacement:")
        return movement and replace(
            movement(self.replacement),
            delete(board.copy(), (movement(k) for k in self.pattern)),
            in_place=True)

    def _distribute(self, m: Movement) -> 'Rule':
        return FindAndReplaceRule(m * self.pattern, m * self.replacement)


class OneOfRule(Rule):
    """A rule which consists of applying exactly one of a set of other rules"""

    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def __str__(self):
        return 'nil' if not self.rules else ' | '.join(f'({r})' for r in self.rules)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rules!r})'

    def __or__(self, other: 'Rule') -> 'OneOfRule':
        if isinstance(other, OneOfRule):
            rules = self.rules + other.rules
        else:
            rules = self.rules.copy()
            rules.append(other)
        return OneOfRule(rules)

    def _apply(self, board: Board) -> List[Board]:
        boards = []
        for rule in self.rules:
            boards.extend(rule(board))
        return boards

    def _player_choice(self, board: Board) -> Optional[Board]:
        rules = [rule for rule in self.rules
            if rule(board)]
        rule_choices = {rule.to_user_choice_repr(): rule for rule in rules}
        rule = get_player_choice(rule_choices, msg="Choose a rule to apply:")
        return rule and rule._player_choice(board)

    def _distribute(self, m: Movement) -> 'Rule':
        return OneOfRule([m * rule for rule in self.rules])


class SequentialRule(Rule):
    """A rule which consists of applying a sequence of other rules, one
    after another.
    """

    def __init__(self, rules: List[Rule]):
        self.rules = rules

    def __str__(self):
        return 'nil' if not self.rules else ''.join(f'({r})' for r in self.rules)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rules!r})'

    def __mul__(self, other: Rule) -> 'SequentialRule':
        if isinstance(other, SequentialRule):
            rules = self.rules + other.rules
        else:
            rules = self.rules.copy()
            rules.append(other)
        return SequentialRule(rules)

    def _apply(self, board: Board) -> List[Board]:
        boards = [board]
        for rule in self.rules:
            boards = rule(boards)
        return boards

    def _player_choice(self, board: Board) -> Optional[Board]:
        for i, rule in enumerate(self.rules, 1):
            if board is None:
                return None
            print(f"Applying rule {i} in a sequence of {len(self.rules)}: {rule.to_user_choice_repr()}")
            board = rule._player_choice(board)
        return board

    def _distribute(self, m: Movement) -> 'Rule':
        return SequentialRule([m * rule for rule in self.rules])


class PieceOfInterestRule(Rule):
    """A rule which consists of choosing a "piece of interest" on the board,
    then applying another rule with the chosen piece replaced by '%'.
    """

    def __init__(self, piece: LocationContents, rule: Rule):
        self.piece = piece
        self.rule = rule

    def __str__(self):
        return f'%{self.piece}: {self.rule}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.piece!r}, {self.rule!r})'

    def _apply_at(self, board: Board, location: Location) -> List[Board]:
        board[location] = '%'
        try:
            return self.rule(board)
        finally:
            board[location] = self.piece

    def _apply(self, board: Board) -> List[Board]:
        if any(v == '%' for v in board.values()):
            return self.rule(board)
        boards = []
        keys = list(board)
        for k in keys:
            if board[k] != self.piece:
                continue
            boards.extend(replace_piece('%', self.piece, board)
                for board in self._apply_at(board, k))
        return boards

    def _player_choice(self, board: Board) -> Optional[Board]:
        if any(v == '%' for v in board.values()):
            return self.rule._player_choice(board)
        print(f"Searching for locations of {self.piece} on board:")
        print_board(board)
        locations = [k for k, v in board.items() if v == self.piece
            and self._apply_at(board, k)]
        print("...matched at locations:")
        print_board(board, highlights=locations)
        location = get_player_choice(locations, msg=f"Choose the location of the {self.piece} to move:")
        if not location:
            return None
        original_board = board
        original_board[location] = '%'
        try:
            board = self.rule._player_choice(original_board)
            return board and replace_piece('%', self.piece, board)
        finally:
            original_board[location] = self.piece

    def _distribute(self, m: Movement) -> 'Rule':
        return PieceOfInterestRule(m * self.piece, m * self.rule)


class RepeatRule(Rule):
    """A rule which consists of applying another rule repeatedly.

    Example usage:

        These rules describe a piece ('u' or 'd') which travels up and down,
        bouncing off another piece ('B'), which is stationary.
        >>> rule = OneOfRule([
        ...     FindAndReplaceRule({(0, 0): 'u', (0, 1): '.'}, {(0, 0): '.', (0, 1): 'u'}),
        ...     FindAndReplaceRule({(0, 0): 'u', (0, 1): 'B'}, {(0, 0): 'd', (0, 1): 'B'}),
        ...     FindAndReplaceRule({(0, 0): '.', (0, 1): 'd'}, {(0, 0): 'd', (0, 1): '.'}),
        ...     FindAndReplaceRule({(0, 0): 'B', (0, 1): 'd'}, {(0, 0): 'B', (0, 1): 'u'}),
        ... ])

        The initial board has the bouncing piece travelling upwards, trapped
        between two stationary pieces.
        The bouncing piece should bounce back and forth between the stationary
        ones.
        >>> board = parse_board([
        ...     'B',
        ...     '.',
        ...     'u',
        ...     '.',
        ...     'B',
        ... ])

        If the rule is applied between 2 and 4 times, these are the possible
        board positions:
        >>> for b in rule.between(2, 4)(board): print_board(b)
        +-+
        |B|
        |d|
        |.|
        |.|
        |B|
        +-+
        +-+
        |B|
        |.|
        |d|
        |.|
        |B|
        +-+
        +-+
        |B|
        |.|
        |.|
        |d|
        |B|
        +-+

        If the rule is applied 0 or more times, these are the possible board
        positions:
        >>> for b in rule.zero_or_more()(board): print_board(b)
        +-+
        |B|
        |.|
        |u|
        |.|
        |B|
        +-+
        +-+
        |B|
        |u|
        |.|
        |.|
        |B|
        +-+
        +-+
        |B|
        |d|
        |.|
        |.|
        |B|
        +-+
        +-+
        |B|
        |.|
        |d|
        |.|
        |B|
        +-+
        +-+
        |B|
        |.|
        |.|
        |d|
        |B|
        +-+
        +-+
        |B|
        |.|
        |.|
        |u|
        |B|
        +-+

    """

    def __init__(
            self,
            rule: Rule,
            at_least: int,
            at_most: Optional[int] = None,
            *,
            greedy: bool = False,
            ):
        if at_most is not None and at_most < at_least:
            raise TypeError(f"Invalid args: {at_most} < {at_least}")
        self.rule = rule
        self.at_least = at_least
        self.at_most = at_most
        self.greedy = greedy

    def __str__(self):
        p = self.at_least, self.at_most
        if p == (0, None):
            brackets_part = '*'
        elif p == (1, None):
            brackets_part = '+'
        else:
            brackets_part = f'{self.at_least}'
            if self.at_most is None:
                brackets_part += ','
            elif self.at_most != self.at_least:
                brackets_part = f'{brackets_part}, {self.at_most}'
            brackets_part = '{' + brackets_part + '}'
        return f'({self.rule}){brackets_part}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.rule!r}, {self.at_least!r}, {self.at_most!r})'

    def _apply(self, board: Board) -> List[Board]:
        boards = [board]
        for i in range(self.at_least):
            boards = self.rule(boards)
        all_boards = boards

        # We apply our rule "forever"!.. except, to avoid an infinite
        # loop, we actually only apply our rule while we find new boards
        # which we haven't seen yet.
        board_keys = {get_board_key(b) for b in boards}
        i = self.at_least
        while True:
            if self.at_most is not None and i >= self.at_most:
                break
            new_boards = []
            for new_board in self.rule(boards):
                key = get_board_key(new_board)
                if key in board_keys:
                    continue
                new_boards.append(new_board)
                board_keys.add(key)
            if not new_boards:
                break
            if self.greedy:
                all_boards = new_boards
            else:
                all_boards.extend(new_boards)
            boards = new_boards
            i += 1

        return unique_boards(all_boards)

    def _player_choice(self, board: Board) -> Optional[Board]:
        i = 0
        board_keys = {get_board_key(board)}
        while True:
            if board is None:
                return None
            print(f"Applying repetition {i + 1} of rule: {self.rule.to_user_choice_repr()}")
            if i >= self.at_least:
                if self.at_most is not None and i >= self.at_most or not self.rule(board):
                    break
                if not self.greedy:
                    print("The board now looks like:")
                    print_board(board)
                    should_continue = get_player_bool_choice(f"Apply the rule again? {self.rule.to_user_choice_repr()}")
                    if not should_continue:
                        break
            board = self.rule._player_choice(board)
            board_key = get_board_key(board)
            if board_key in board_keys:
                # Avoid infinite loop
                break
            board_keys.add(board_key)
            i += 1
        return board

    def _distribute(self, m: Movement) -> 'Rule':
        return RepeatRule(m * self.rule, self.at_least, self.at_most)


class Game(NamedTuple):
    rule: Rule
    initial_board: Board


def reverse_xo_pieces(piece: LocationContents) -> LocationContents:
    return piece.replace('X', '<X>').replace('O', 'X').replace('<X>', 'O')
class ReverseXOMovement:
    def __call__(self, other):
        if isinstance(other, str):
            return reverse_xo_pieces(other)
        elif isinstance(other, dict):
            return {k: reverse_xo_pieces(v) for k, v in other.items()}
        elif isinstance(other, Rule):
            return other._distribute(self)
        else:
            raise TypeError(type(other))
    __mul__ = __call__
TIC_TAC_TOE = Game(
    rule=OneOfRule([
        parse_rule('. -> X'),
        parse_rule('. -> O'),
    ]) * OneOfRule([
        rule
        for c in 'XO'
        for rule in (
            # Win conditions... ☺
            parse_rule(f'{c}{c}{c} -> ☺☺☺'),
            parse_rule(f'{c};{c};{c} -> ☺;☺;☺'),
            parse_rule(f'{c};r{c};rr{c} -> ☺;r☺;rr☺'),
            parse_rule(f'{c};l{c};ll{c} -> ☺;l☺;ll☺'),
        )
    ]).zero_or_more(greedy=True),
    initial_board=parse_board('...;...;...'),
)

SNAKE_BODY = '↑←↓→'
SNAKE_TAIL = '↟↞↡↠'
SNAKE_PIECES = SNAKE_BODY + SNAKE_TAIL
def snake_rotate_piece(piece: LocationContents, n: int) -> LocationContents:
    if len(piece) != 1:
        return ''.join(map(snake_rotate_piece, piece))
    if piece in SNAKE_PIECES:
        i = SNAKE_PIECES.index(piece)
        i = (i // 4) * 4 + (i + n) % 4
        return SNAKE_PIECES[i]
    else:
        return piece
class SnakeRotateMovement:
    def __init__(self, n: int):
        self.n = n
        self.rotate = Movement.rotate(n)
    def __call__(self, other):
        if isinstance(other, str):
            return snake_rotate_piece(other, self.n)
        elif isinstance(other, dict):
            n = self.n
            other = self.rotate * other
            for k, v in other.items():
                other[k] = snake_rotate_piece(v, n)
            return other
        elif isinstance(other, Rule):
            return other._distribute(self)
        else:
            raise TypeError(type(other))
    __mul__ = __call__
_SNAKE_TAIL_FOLLOW_RULE = parse_rule('(↟;↑ -> .;↟)|(↟;→ -> .;↠)|(↟;← -> .;↞)')
SNAKE = Game(
    rule=OneOfRule([
        SnakeRotateMovement(i) * rule
        for i in range(4)
        for rule in (
            # Eat:
            parse_rule('S;$ -> ↑;S'),
            # Move:
            parse_rule('S;. -> ↑;S') * OneOfRule([
                SnakeRotateMovement(i) * _SNAKE_TAIL_FOLLOW_RULE
                for i in range(4)
            ]),
        )
    ]),
    initial_board=parse_board([
        ' .$.....',
        '.............',
        '..↠S.$..  .$$',
        '$.......   $$',
        '......$.',
    ]),
)

CHESS_PIECES_UNFILLED = '♙♔♕♗♘♖'
CHESS_PIECES_FILLED = '♟♚♛♝♞♜'
CHESS_PIECES = CHESS_PIECES_UNFILLED + CHESS_PIECES_FILLED
def chess_reverse_piece(piece: LocationContents) -> LocationContents:
    if len(piece) != 1:
        return ''.join(map(chess_reverse_piece, piece))
    if piece in CHESS_PIECES:
        l = len(CHESS_PIECES)
        i = CHESS_PIECES.index(piece) + l // 2
        return CHESS_PIECES[i % l]
    else:
        return piece
class ChessReverseMovement:
    rotate = Movement.rotate(2)
    def __call__(self, other):
        if isinstance(other, str):
            return chess_reverse_piece(other)
        elif isinstance(other, dict):
            other = self.rotate * other
            for k, v in other.items():
                other[k] = chess_reverse_piece(v)
            return other
        elif isinstance(other, Rule):
            return other._distribute(self)
        else:
            raise TypeError(type(other))
    __mul__ = __call__
_CHESS_ROOK_RULE = OneOfRule([
    # Just move
    parse_rule('%;. -> .;%').one_or_more(),
    # Move and take
    parse_rule('%;. -> .;%').zero_or_more(greedy=True) * parse_rule(f'%;[{CHESS_PIECES_FILLED}] -> .;%')
])
_CHESS_BISHOP_RULE = OneOfRule([
    # Just move
    parse_rule('%;l. -> .;l%').one_or_more(),
    # Move and take
    parse_rule('%;l. -> .;l%').zero_or_more(greedy=True) * parse_rule(f'%;l[{CHESS_PIECES_FILLED}] -> .;l%')
])
CHESS_RULE = OneOfRule([
    PieceOfInterestRule('♙', OneOfRule([
        # Move one square up
        parse_rule('%;. -> .;%'),
        # Move two squares up from initial position
        parse_rule(f'[^.{CHESS_PIECES}];0;%;.;. -> 0;0;.;.;%'),
        # Take diagonally
        parse_rule(f'%;r[{CHESS_PIECES_FILLED}] -> .;r%'),
        parse_rule(f'%;l[{CHESS_PIECES_FILLED}] -> .;l%'),
    ]) * OneOfRule([
        # If a pawn reaches the far rank, it must transform!
        parse_rule(f'%;[^.{CHESS_PIECES}] -> {p}')
        for p in '♕♗♘♖'
    ]).optionally(greedy=True)),
    PieceOfInterestRule('♔', OneOfRule([
        # Move or take in any of 8 directions
        Movement.rotate(i) * rule
        for i in range(4)
        for rule in (
            parse_rule(f'%;[.{CHESS_PIECES_FILLED}] -> .;%'),
            parse_rule(f'%;l[.{CHESS_PIECES_FILLED}] -> .;l%'),
        )
    ] + [
        # Castling!.. allowed even through check, due to the difficulty
        # of detecting check with algebra alone...
        parse_rule(f'[^.{CHESS_PIECES}];♖..% -> 0;.%♖.'),
        parse_rule(f'[^.{CHESS_PIECES}];%...♖ -> 0;.♖%..'),
    ])),
    PieceOfInterestRule('♕', OneOfRule([
        Movement.rotate(i) * rule
        for i in range(4)
        for rule in (_CHESS_BISHOP_RULE, _CHESS_ROOK_RULE)
    ])),
    PieceOfInterestRule('♗', OneOfRule([
        Movement.rotate(i) * _CHESS_BISHOP_RULE
        for i in range(4)
    ])),
    PieceOfInterestRule('♘', OneOfRule([
        Movement.rotate(i) * rule
        for i in range(4)
        for rule in (
            parse_rule(f'%;;r[.{CHESS_PIECES_FILLED}] -> .;;r%'),
            parse_rule(f'%;;l[.{CHESS_PIECES_FILLED}] -> .;;l%'),
        )
    ])),
    PieceOfInterestRule('♖', OneOfRule([
        Movement.rotate(i) * _CHESS_ROOK_RULE
        for i in range(4)
    ])),
])
CHESS = Game(
    rule=OneOfRule([
        CHESS_RULE,
        ChessReverseMovement() * CHESS_RULE,
    ]),
    initial_board=parse_board([
        '♜♞♝♚♛♝♞♜',
        '♟♟♟♟♟♟♟♟',
        '........',
        '........',
        '........',
        '........',
        '♙♙♙♙♙♙♙♙',
        '♖♘♗♔♕♗♘♖',
    ]),
)


_OTHELLO_RULE = PieceOfInterestRule('.', OneOfRule([
    Movement.rotate(i) * (
        parse_rule('%O -> %F') * parse_rule('FO -> XF').zero_or_more(greedy=True) * parse_rule('FX -> XX')
    )
    for i in range(4)
]).one_or_more(greedy=True) * parse_rule('% -> X'))
OTHELLO = Game(
    rule=OneOfRule([
        _OTHELLO_RULE,
        ReverseXOMovement() * _OTHELLO_RULE,
    ]),
    initial_board=parse_board([
        '........',
        '........',
        '........',
        '...XO...',
        '...OX...',
        '........',
        '........',
        '........',
    ]),
)


GAMES = {
    'tictac': TIC_TAC_TOE,
    'chess': CHESS,
    'snake': SNAKE,
    'othello': OTHELLO,
}


def play_game(game: Game):
    rule = game.rule
    board = game.initial_board
    turn_no = 1
    while True:
        print()
        print('=' * 40)
        print(f"=== TURN {turn_no}:")
        if board is None:
            print("Out of options! Game over.")
            break
        print_board(board)
        board = rule._player_choice(board)
        turn_no += 1
