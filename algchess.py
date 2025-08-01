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
    |p...|
    |..K.|
    |.ppp|
    |....|
    +----+
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
    |.p..|
    |..K.|
    |p.pp|
    |....|
    +----+
    +----+
    |....|
    |.pKp|
    |p.p.|
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


RULE_TOKEN_REGEX = re.compile(r'[()|*+]|%.:|->|{.*}|[^(){}|*+:\->]+')


Location = Tuple[int, int]
LocationContents = str
Board = Dict[Location, LocationContents]
BoardKey = FrozenSet[Tuple[Location, LocationContents]]


def board_key(board: Board) -> BoardKey:
    """Returns a hashable representation of a Board"""
    return frozenset(board.items())


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
        key = board_key(board)
        if key in found:
            continue
        found[key] = board
    return list(found.values())


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

    """
    f = {}
    if isinstance(lines_or_text, str):
        text = lines_or_text
        x = x0
        y = y0
        for c in text:
            if c in (' ', '1'):
                continue
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
        l^2(rP;K.;r.)
        l^3 d^2(rK;..P)
        d^3(.;.K;P)

    """
    if not f:
        return '0'
    min_x = min(x for x, y in f)
    min_y = min(y for x, y in f)
    max_x = max(x for x, y in f)
    max_y = max(y for x, y in f)
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    lines = []
    for y in range(min_y, max_y + 1):
        line = ''.join(
            f.get((x, y), 'r')
            for x in range(min_x, max_x + 1))
        lines.append(line.rstrip('r'))
    s = ';'.join(lines)
    if min_x != 0 or min_y != 0:
        s = f'{Movement.slide(min_x, min_y)}({s})'
    return s


def print_board(f: Board, *, file=None, border=True):
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
        for y in range(min_y, max_y + 1):
            lines.append(''.join(
                f.get((x, y), ' ')
                for x in range(min_x, max_x + 1)))
        lines.reverse()
    if border:
        print('+' + '-' * w + '+', file=file)
    for line in lines:
        if border:
            line = f'|{line}|'
        print(line, file=file)
    if border:
        print('+' + '-' * w + '+', file=file)


def parse_rule(text: str, *, debug=False) -> 'Rule':
    """Parses a Rule, should be more or less the inverse of Rule.__str__

        >>> print(parse_rule('(p;. -> .;p) | (p;rK -> .;rp) | (rp;K -> r.;p)'))
        (p;. -> .;p) | (p;rK -> .;rp) | (rp;K -> r.;p)

        >>> print(parse_rule('%p: (%;. -> .;%)(%;. -> .;%)'))
        %p: (%;. -> .;%)(%;. -> .;%)

        >>> print(parse_rule('%p: (l^2(.%) -> l^2(%.))+'))
        %p: (l^2(.%) -> l^2(%.))+

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
        else:
            raise TypeError(type(other))


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

    return [
        Movement.slide(x2 - x, y2 - y)
        for (x2, y2), c2 in g.items()
        if c2 == c and match(f, g, x2 - x, y2 - y)]


def replace(f: Board, g: Board) -> Board:
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
    h = g.copy()
    h.update(f)
    return h


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
    return [replace(m(g), h) for m in find(f, h)]


class Rule(metaclass=ABCMeta):
    """A rule is a function which maps a board to a set of possible boards,
    i.e. a set of possible "moves" a player might make, taking the board
    from one position to another.

    This is an abstract base class; only its subclasses should be
    instantiated.
    """

    def __init__(self):
        raise NotImplementedError("To be implemented by subclasses")

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

    def zero_or_more(self) -> 'RepeatRule':
        return RepeatRule(self, 0)

    def one_or_more(self) -> 'RepeatRule':
        return RepeatRule(self, 1)

    def repeat(self, n: int) -> 'RepeatRule':
        return RepeatRule(self, n, n)

    def between(self, at_least: int, at_most: Optional[int] = None) -> 'RepeatRule':
        # NOTE: an at_most of None is interpreted as infinity
        return RepeatRule(self, at_least, at_most)

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
    def _distribute(self, m: Movement) -> 'Rule': ...


class FindAndReplaceRule(Rule):
    """A rule which consists of finding a given board fragment (the "pattern")
    and replacing it with another (the "replacement").
    """

    def __init__(self, pattern: Board, replacement: Board):
        self.pattern = pattern
        self.replacement = replacement

    def __str__(self):
        return f'{board_repr(self.pattern)} -> {board_repr(self.replacement)}'

    def __repr__(self):
        return f'{self.__class__.__name__}({self.pattern!r}, {self.replacement!r})'

    def _apply(self, board: Board) -> List[Board]:
        return find_and_replace(self.pattern, self.replacement, board)

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

    def _apply(self, board: Board) -> List[Board]:
        if any(v == '%' for v in board.values()):
            return self.rule(board)
        boards = []
        keys = list(board)
        for k in keys:
            if board[k] != self.piece:
                continue
            board[k] = '%'
            try:
                boards.extend(
                    replace_piece('%', self.piece, board)
                    for board in self.rule(board))
            finally:
                board[k] = self.piece
        return boards

    def _distribute(self, m: Movement) -> 'Rule':
        return PieceOfInterestRule(self.piece, m * self.rule)


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

    def __init__(self, rule: Rule, at_least: int, at_most: Optional[int] = None):
        if at_most is not None and at_most < at_least:
            raise TypeError(f"Invalid args: {at_most} < {at_least}")
        self.rule = rule
        self.at_least = at_least
        self.at_most = at_most

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
        if self.at_most is not None:
            # We have already applied our rule self.at_least times, resulting
            # in all_boards.
            # Now we apply our rule (self.at_most - self.at_least) more times,
            # extending all_boards each time.
            for i in range(self.at_most - self.at_least):
                boards = self.rule(boards)
                all_boards.extend(boards)
        else:
            # We apply our rule "forever"!.. except, to avoid an infinite
            # loop, we actually only apply our rule while we find new boards
            # which we haven't seen yet.
            board_keys = {board_key(b) for b in boards}
            while True:
                new_boards = []
                for new_board in self.rule(boards):
                    key = board_key(new_board)
                    if key in board_keys:
                        continue
                    new_boards.append(new_board)
                    board_keys.add(key)
                if not new_boards:
                    break
                all_boards.extend(new_boards)
                boards = new_boards
        return unique_boards(all_boards)

    def _distribute(self, m: Movement) -> 'Rule':
        return RepeatRule(m * self.rule, self.at_least, self.at_most)
