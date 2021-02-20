import argparse
import curses
from datetime import datetime
from pathlib import Path

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border("|", "|", "-", "-", "#", "#", "#", "#")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        # for pos_x, row in enumerate(self.life.curr_generation):
        #     for pos_y, value in enumerate(row):
        for pos_y in range(self.life.cols):
            for pos_x in range(self.life.rows):
                symbol = arguments.symbol if self.life.curr_generation[pos_x][pos_y] else " "
                try:
                    screen.addstr(pos_x + 1, pos_y + 1, symbol, curses.A_STANDOUT)
                except curses.error:
                    continue

    def run(self) -> None:
        win = curses.initscr()
        curses.curs_set(0)
        limits = win.getmaxyx()
        if arguments.rows > limits[0] - 1 or arguments.cols > limits[1] - 1:
            raise ValueError(f'Невозможно отрисовать картинку такого размера. Максимальный размер {limits[0]}x{limits[1]}.')
        curses.noecho()
        win = curses.newwin(self.life.rows + 2, self.life.cols + 2, 0, 0)
        win.nodelay(True)
        running = True
        pause = False
        while running:
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            char = win.getch()
            if char == ord(' '):
                pause = not pause
            if char == ord('s'):
                save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.life.save(Path(f"saves/life_{save_time}.txt"))
            if char == ord('q'):
                running = False
            if not pause:
                win.clear()
                curses.delay_output(200)
                self.draw_borders(win)
                self.draw_grid(win)
                self.life.step()
                win.refresh()
        curses.endwin()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GameOfLife")
    parser.add_argument("--rows", type=int, default=10, help="Enter number of rows in grid")
    parser.add_argument("--cols", type=int, default=30, help="Enter number of columns in grid")
    parser.add_argument("--speed", type=int, default=1, help="Enter game speed")
    parser.add_argument(
        "--maxgenerations", type=int, default=1000, help="Enter max number of generations"
    )
    parser.add_argument("--randomize", type=int, default=1, help="Should grid be randomized?")
    parser.add_argument("--grid_path", type=Path, default=None, help="Load grid from file")
    parser.add_argument(
        "--symbol", type=str, default="@", help="Select a symbol to display live cells"
    )
    arguments = parser.parse_args()
    if arguments.grid_path is not None:
        gui = Console(GameOfLife.from_file(arguments.grid_path))
    else:
        gui = Console(
            GameOfLife(
                (arguments.rows, arguments.cols), arguments.randomize, arguments.maxgenerations
            )
        )
    gui.run()
