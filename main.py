import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Welcome to the Speed Typing Test!")
    stdscr.addstr("\nPress any key to begin!")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        if i < len(target):
            correct_char = target[i]
            color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
            stdscr.addstr(0, i, char, color)


def load_text():
    try:
        with open("text.txt", "r") as f:
            lines = f.readlines()
            return random.choice(lines).strip()
    except FileNotFoundError:
        return "Suleman"

def wpm_test(stdscr):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()   # ⏱ start measuring time
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, wpm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            end_time = time.time()   # ⏱ stop measuring
            total_time = round(end_time - start_time, 2)
            return wpm, total_time   # return both wpm and time

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            return None, None

        if key in ("KEY_BACKSPACE", '\b', "\x7f", "\x08"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)
    while True:
        wpm, total_time = wpm_test(stdscr)

        if wpm is None:  # ESC pressed
            break

        minutes = int(total_time // 60)
        seconds = int(total_time % 60)

        stdscr.addstr(2, 0, f"You completed the text in {minutes}m {seconds}s!")
        stdscr.addstr(3, 0, f"Your typing speed was {wpm} WPM.")
        stdscr.addstr(5, 0, "Press any key to try again or ESC to quit.")
        key = stdscr.getkey()
        
        if ord(key) == 27:
            break

wrapper(main)
