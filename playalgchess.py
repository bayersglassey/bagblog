import locale
from typing import Optional
from collections import defaultdict
from argparse import ArgumentParser
from functools import reduce

from curtsies import FullscreenWindow, Input, FSArray, FmtStr
from curtsies.fmtfuncs import (
    red,
    blue,
    dark,
    green,
    on_blue,
    on_dark,
    yellow,
    invert,
    fmtstr,
)

from algchess import (
    Board,
    Game,
    get_board_lines,
    get_board_bounds,
    board_diff,
    GAMES,
)


fmtstr_join = fmtstr('').join


# See: https://curtsies.readthedocs.io/en/latest/Input.html#input-keypress-strings
ENTER = '<Ctrl-j>'


_apply = lambda x, f: f(x)
def compose(*ff):
    """Function composition!

        >>> f = compose(
        ...     lambda x: x + 1,
        ...     lambda x: x * 10,
        ... )

        >>> f(1)
        20

        >>> f(2)
        30

    """
    return lambda x: reduce(_apply, ff, x)


def play_game(game: Game):
    rule = game.rule
    board = game.initial_board
    with FullscreenWindow() as window, Input() as input:

        # Cursor's position, i.e. the thing user moves around with the
        # arrow keys
        cx = 0
        cy = 0

        # Turn number, i.e. player's first turn, second, third, etc.
        turn_no = 1

        while True:

            # Lines of text to be rendered at the top of the screen
            header_lines = []
            header_lines.append('=' * 40)
            header_lines.append(f"=== TURN {turn_no}:")

            # Find all possible "next" boards among which user can choose
            # this turn
            next_boards = rule(board)

            # If player has no moves, they lose
            if not next_boards:
                lines = header_lines.copy()
                lines += get_board_lines(board)
                lines.append("Can't make any moves! Game over.")
                lines.append("Press Enter to continue...")
                window.render_to_terminal(lines)
                for key in input:
                    if key == ENTER:
                        break
                break

            # Locations player has "selected", i.e. put the cursor on and
            # pressed Enter
            selected_locations = set()

            # Subset of next_boards whose diffs with board overlap with
            # selected_locations
            selectable_boards = []

            # Subset of selectable_boards whose diffs with board overlap with
            # (cx, cy)
            cursor_adjacent_boards = []

            # All locations in the diffs between board and cursor_adjacent_boards
            cursor_adjacent_locations = set()

            # Index into selectable_boards: if there are more than one, player
            # can cycle through them with the page up/down keys
            board_i = None

            def update_selectable_boards():
                """Should be called when any of selected_locations, cx, or cy
                are changed"""

                selectable_boards.clear()
                cursor_adjacent_boards.clear()
                cursor_adjacent_locations.clear()

                cp = (cx, cy)

                for next_board in next_boards:
                    d = board_diff(board, next_board)
                    is_selectable = selected_locations and all(
                        k in d for k in selected_locations)
                    if is_selectable:
                        selectable_boards.append(next_board)
                    if (not selected_locations or is_selectable) and cp in d:
                        cursor_adjacent_boards.append(next_board)
                        cursor_adjacent_locations.update(d)

            update_selectable_boards()

            # Loop until user selects a "next" board for their turn
            selected = False
            while not selected:

                # Lines of text to be displayed
                lines = header_lines.copy()

                lines.append(f"{board_i=} {len(next_boards)=} {len(selectable_boards)=} {len(cursor_adjacent_boards)=}")

                # Determine selected_board
                if board_i is not None:
                    # Player used page up/down to manually select a board
                    lines.append(f"Choose this move? ({board_i + 1} / {len(selectable_boards)})")
                    selected_board = selectable_boards[board_i]
                elif len(selectable_boards) == 1:
                    lines.append("Choose this move?")
                    selected_board = selectable_boards[0]
                elif len(cursor_adjacent_boards) == 1:
                    lines.append("Choose this move?")
                    selected_board = cursor_adjacent_boards[0]
                else:
                    lines.append(f"{len(cursor_adjacent_boards)} possible moves")
                    selected_board = None

                # Figure out which board to display
                if selected_board is not None:
                    display_board = selected_board
                else:
                    display_board = board

                # Make sure the cursor is displayed, even if it's off the board
                if (cx, cy) not in display_board:
                    display_board = display_board.copy()
                    display_board[(cx, cy)] = '?'

                # Figure out which board locations will be highlighted
                highlights = {}
                def highlight(k, *ff):
                    if k in highlights:
                        g = highlights[k]
                        highlights[k] = compose(g, *ff)
                    else:
                        highlights[k] = compose(*ff)
                for k in cursor_adjacent_locations:
                    highlight(k, blue)
                for k in selected_locations:
                    highlight(k, on_dark, on_blue)
                if selected_board:
                    for k in board_diff(board, selected_board):
                        highlight(k, green)
                if (cx, cy) in highlights:
                    highlights[(cx, cy)] = on_blue
                else:
                    highlights[(cx, cy)] = invert

                # Render the board (to lines)
                lines += get_board_lines(display_board,
                    str_join=fmtstr_join,
                    highlights=highlights)

                # TODO: display the controls.
                # The message will be slightly different depending on whether
                # Enter will just add to selected_locations, or actuall choose
                # a final board.

                # Render the lines of text we've built up
                window.render_to_terminal(lines)

                # Loop over keypresses until we find a significant one,
                # then handle it, then loop back up to where we render the
                # board etc
                for key in input:
                    if key == '<LEFT>':
                        cx -= 1
                        update_selectable_boards()
                        board_i = None
                        break
                    elif key == '<RIGHT>':
                        cx += 1
                        update_selectable_boards()
                        board_i = None
                        break
                    elif key == '<UP>':
                        cy += 1
                        update_selectable_boards()
                        board_i = None
                        break
                    elif key == '<DOWN>':
                        cy -= 1
                        update_selectable_boards()
                        board_i = None
                        break
                    elif key == '<ESC>':
                        selected_locations.clear()
                        update_selectable_boards()
                        board_i = None
                        break
                    elif key == '<PAGEUP>':
                        selected_locations.add((cx, cy))
                        update_selectable_boards()
                        if selectable_boards:
                            if board_i is None:
                                board_i = 0
                            else:
                                board_i = (board_i + 1) % len(selectable_boards)
                        break
                    elif key == '<PAGEDOWN>':
                        selected_locations.add((cx, cy))
                        update_selectable_boards()
                        if selectable_boards:
                            if board_i is None:
                                board_i = 0
                            else:
                                board_i = (board_i - 1) % len(selectable_boards)
                        break
                    elif key == ENTER:
                        if selected_board is not None:
                            board = selected_board
                            selected = True
                            break
                        else:
                            selected_locations.add((cx, cy))
                            update_selectable_boards()
                            board_i = None
                            break

            turn_no += 1


def main():
    locale.setlocale(locale.LC_ALL, '')

    parser = ArgumentParser()
    parser.add_argument('-g', '--game', choices=GAMES, default='chess')
    args = parser.parse_args()

    game = GAMES[args.game]
    try:
        play_game(game)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
