import locale
from typing import Optional
from collections import defaultdict
from argparse import ArgumentParser

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


def play_game(game: Game):
    rule = game.rule
    board = game.initial_board
    with FullscreenWindow() as window, Input() as input:
        mx = 0
        my = 0
        turn_no = 1
        while True:

            header_lines = []
            header_lines.append('=' * 40)
            header_lines.append(f"=== TURN {turn_no}:")

            next_boards = rule(board)
            if not next_boards:
                lines = header_lines.copy()
                lines += get_board_lines(board)
                lines.append("Out of options! Game over.")
                lines.append("Press Enter to continue...")
                window.render_to_terminal(lines)
                for key in input:
                    if key == ENTER:
                        break
                break

            selected_locations = set()
            affectable_locations = set()
            selected_boards = next_boards
            board_i = 0

            def update_selected_boards():
                nonlocal selected_boards, board_i
                _selected_locations = selected_locations.copy()
                _selected_locations.add((mx, my))
                if _selected_locations:
                    selected_boards = [next_board
                        for next_board in next_boards
                        if _selected_locations.intersection(
                            board_diff(board, next_board)
                        ) == _selected_locations]
                else:
                    selected_boards = next_boards
                affectable_locations.clear()
                for b in selected_boards:
                    affectable_locations.update(board_diff(board, b))
                board_i = 0

            update_selected_boards()

            selected = False
            while not selected:

                display_board = board.copy()

                # Should we limit the cursor to the board's existing locations?..
                LIMIT_CURSOR = False
                if LIMIT_CURSOR:
                    min_x, min_y, max_x, max_y = get_board_bounds(board)
                    if mx < min_x: mx = min_x
                    if mx > max_x: mx = max_x
                    if my < min_y: my = min_y
                    if my > max_y: my = max_y
                else:
                    display_board.setdefault((mx, my), '?')

                lines = header_lines.copy()

                # Render original board
                highlights = {
                    k: blue if k in affectable_locations else dark
                    for k in display_board}
                highlights.update({k: lambda s: on_dark(on_blue(s))
                    for k in selected_locations})
                if (mx, my) in highlights:
                    highlights[(mx, my)] = on_blue
                else:
                    highlights[(mx, my)] = invert
                lines += get_board_lines(display_board,
                    str_join=fmtstr_join,
                    highlights=highlights)

                # Render next board
                if selected_boards:
                    lines.append(f'Choose next board ({board_i + 1} / {len(selected_boards)}):')
                    selected_board = selected_boards[board_i]
                    highlights = {k: green
                        for k in board_diff(board, selected_board)}
                    highlights[(mx, my)] = invert
                    lines += get_board_lines(selected_board,
                        str_join=fmtstr_join,
                        highlights=highlights)
                else:
                    selected_board = None

                window.render_to_terminal(lines)

                for key in input:
                    if key == '<LEFT>':
                        mx -= 1
                        update_selected_boards()
                        break
                    elif key == '<RIGHT>':
                        mx += 1
                        update_selected_boards()
                        break
                    elif key == '<UP>':
                        my += 1
                        update_selected_boards()
                        break
                    elif key == '<DOWN>':
                        my -= 1
                        update_selected_boards()
                        break
                    elif key == '<SPACE>':
                        # Toggle whether the location (mx, my) is selected
                        selected_locations ^= {(mx, my)}
                        update_selected_boards()
                        break
                    elif key == '<ESC>':
                        selected_locations.clear()
                        update_selected_boards()
                        break
                    elif key == '<PAGEUP>':
                        if selected_boards:
                            board_i = (board_i + 1) % len(selected_boards)
                        break
                    elif key == '<PAGEDOWN>':
                        if selected_boards:
                            board_i = (board_i - 1) % len(selected_boards)
                        break
                    elif key == ENTER:
                        if selected_board is not None:
                            board = selected_board
                            selected = True
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
