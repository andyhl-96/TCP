import curses
from curses import *

def main(stdscr):
    stdscr.clear()
    shape = stdscr.getmaxyx()
    curses.use_default_colors()
    #curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_WHITE)
    #stdscr.bkgd(" ", curses.color_pair(1) | curses.A_BOLD)
    stdscr.addstr(shape[0] // 2 - 1, shape[1] // 2 - 6, "  0 1 2 3 4 5 6 7\n"+
"0 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜\n"
"1 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟\n"
"2 ▦ □ ▦ □ ▦ □ ▦ □\n"
"3 □ ▦ □ ▦ □ ▦ □ ▦\n"
"4 ▦ □ ▦ □ ▦ □ ▦ □\n"
"5 □ ▦ □ ▦ □ ▦ □ ▦\n"
"6 ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟\n"
"7 ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜")
    stdscr.refresh()
    stdscr.getkey()
wrapper(main)
    