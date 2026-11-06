import curses
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch


spec = importlib.util.spec_from_file_location("picker", Path(__file__).resolve().parents[1] / "picker.py")
picker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(picker)


class Screen:
    def __init__(self, keys, height=10, width=90):
        self.keys = iter(keys)
        self.size = (height, width)
        self.frames = []
        self.lines = {}

    def getmaxyx(self):
        return self.size

    def keypad(self, enabled):
        pass

    def erase(self):
        self.lines = {}

    def addstr(self, y, x, text, style):
        self.lines[y] = text

    def refresh(self):
        self.frames.append(dict(self.lines))

    def getch(self):
        return next(self.keys)


class PickerTests(unittest.TestCase):
    def run_picker(self, keys, count=8, **dimensions):
        rows = [[str(i), f"Team {i} vs Opponent", "3-2", "8:42 - 3rd", f"https://example.com/{i}"] for i in range(1, count + 1)]
        screen = Screen(keys, **dimensions)
        with patch.object(picker.curses, "curs_set"):
            result = picker.pick(screen, rows)
        return result, screen

    def test_launches_exact_nonconsecutive_selections_after_scrolling(self):
        result, screen = self.run_picker([curses.KEY_DOWN, 32, curses.KEY_NPAGE, 32, curses.KEY_END, 32, 10])
        self.assertEqual(result, "2 6 8")
        self.assertIn("Games 5–8 of 8", str(screen.frames))

    def test_fifth_selection_is_rejected(self):
        keys = [32, curses.KEY_DOWN] * 5 + [10]
        result, screen = self.run_picker(keys)
        self.assertEqual(result, "1 2 3 4")
        self.assertIn("Four games selected", str(screen.frames))

    def test_select_all_for_four_or_fewer(self):
        for count in (1, 3, 4):
            with self.subTest(count=count):
                result, _ = self.run_picker([ord("a"), 10], count=count)
                self.assertEqual(result, " ".join(str(i) for i in range(1, count + 1)))

    def test_select_all_does_not_choose_arbitrary_four(self):
        result, screen = self.run_picker([ord("a"), curses.KEY_END, 32, 10])
        self.assertEqual(result, "8")
        self.assertIn("More than four games", str(screen.frames))

    def test_clear_and_deselect(self):
        result, _ = self.run_picker([ord("a"), ord("c"), 32, 32, curses.KEY_END, 32, 10], count=4)
        self.assertEqual(result, "4")

    def test_enter_without_selection_does_not_launch(self):
        result, screen = self.run_picker([10, ord("q")])
        self.assertIsNone(result)
        self.assertIn("Select at least one game", str(screen.frames))

    def test_small_terminal_and_navigation_boundaries(self):
        result, _ = self.run_picker([curses.KEY_UP, curses.KEY_PPAGE, curses.KEY_END, curses.KEY_DOWN, 32, 10], height=4, width=12)
        self.assertEqual(result, "8")

    def test_escape_cancels(self):
        result, _ = self.run_picker([32, 27])
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
