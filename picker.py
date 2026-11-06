#!/usr/bin/env python3
"""Scrollable game picker; read listing TSV on stdin, write chosen numbers on stdout."""

import curses
import os
import sys
import unicodedata


def clean(value):
    return "".join(c for c in value if not unicodedata.category(c).startswith("C"))


def draw_line(screen, y, text, style=0):
    height, width = screen.getmaxyx()
    if y >= height or width < 2:
        return
    # Account for wide characters and avoid writing the bottom-right cell.
    clipped, used = [], 0
    for char in clean(text):
        size = 0 if unicodedata.combining(char) else (2 if unicodedata.east_asian_width(char) in "WF" else 1)
        if used + size > width - 1:
            break
        clipped.append(char)
        used += size
    try:
        screen.addstr(y, 0, "".join(clipped), style)
    except curses.error:
        pass  # A resize may invalidate the dimensions between reads.


def pick(screen, rows):
    screen.keypad(True)
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    cursor, offset, selected, message = 0, 0, [], ""
    while True:
        height, width = screen.getmaxyx()
        page = max(1, height - 6)
        offset = min(offset, max(0, len(rows) - page))
        if cursor < offset:
            offset = cursor
        elif cursor >= offset + page:
            offset = cursor - page + 1
        screen.erase()
        draw_line(screen, 0, f"Mosaic | {len(rows)} games | {len(selected)}/4 selected", curses.A_BOLD)
        draw_line(screen, 1, "Up/Down: move  Space: select  Enter: launch  q: quit")
        draw_line(screen, 2, "a: select all (up to 4)  c: clear  PgUp/PgDn: scroll  Home/End: first/last")
        for y, index in enumerate(range(offset, min(len(rows), offset + page)), 3):
            number, matchup, score, status, _url = rows[index]
            marker = "[x]" if index in selected else "[ ]"
            # Keep scores and status visible on typical terminal widths.
            matchup_width = max(8, min(56, width - len(score) - len(status) - 16))
            label = matchup if len(matchup) <= matchup_width else matchup[:matchup_width - 1] + "…"
            text = f"{marker} {number:>3}  {label:<{matchup_width}}  {score or '—'}  {status}"
            draw_line(screen, y, text, curses.A_REVERSE if index == cursor else 0)
        draw_line(screen, height - 2, message or "Select up to four games with Space, then press Enter to launch.")
        draw_line(screen, height - 1, f"Games {offset + 1}–{min(len(rows), offset + page)} of {len(rows)}")
        screen.refresh()
        key = screen.getch()
        message = ""
        if key in (ord("q"), ord("Q"), 27):
            return None
        if key in (curses.KEY_UP, ord("k")):
            cursor = max(0, cursor - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            cursor = min(len(rows) - 1, cursor + 1)
        elif key == curses.KEY_PPAGE:
            cursor = max(0, cursor - page)
        elif key == curses.KEY_NPAGE:
            cursor = min(len(rows) - 1, cursor + page)
        elif key == curses.KEY_HOME:
            cursor = 0
        elif key == curses.KEY_END:
            cursor = len(rows) - 1
        elif key in (ord("a"), ord("A")):
            if len(rows) <= 4:
                selected = list(range(len(rows)))
            else:
                message = "More than four games available. Use Space to choose any four."
        elif key in (ord("c"), ord("C")):
            selected.clear()
        elif key == ord(" "):
            if cursor in selected:
                selected.remove(cursor)
            elif len(selected) < 4:
                selected.append(cursor)
            else:
                message = "Four games selected. Deselect one before adding another."
        elif key in (10, 13, curses.KEY_ENTER):
            if selected:
                return " ".join(rows[i][0] for i in selected)
            message = "Select at least one game with Space before launching."


def main():
    rows = [line.split("\t") for line in sys.stdin.read().splitlines() if not line.startswith("MODE\t")]
    if not rows or any(len(row) != 5 for row in rows):
        return 3
    saved_out = os.dup(1)
    result = None
    code = 0
    try:
        # Listing data arrives over a pipe; curses reads and draws on the terminal.
        terminal = os.open("/dev/tty", os.O_RDWR)
        try:
            os.dup2(terminal, 0)
            os.dup2(terminal, 1)
            result = curses.wrapper(pick, rows)
        finally:
            os.close(terminal)
    except (curses.error, OSError):
        code = 3  # Let the launcher fall back to the numbered menu.
    except KeyboardInterrupt:
        code = 130
    finally:
        os.dup2(saved_out, 1)
        os.close(saved_out)
    if result is not None:
        print(result)
    return code if code else (0 if result is not None else 130)


if __name__ == "__main__":
    sys.exit(main())
