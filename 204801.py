import tkinter as tk
import tkinter.messagebox as messagebox
import random


class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game - Mouse Control")
        self.game_running = True
        self.board_size = 4
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
            256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        self.score = 0

        self.init_ui()
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

        # Привязка событий мыши
        self.window.bind("<Button-1>", self.mouse_down)
        self.window.bind("<B1-Motion>", self.mouse_move)
        self.window.bind("<ButtonRelease-1>", self.mouse_up)

        self.mouse_start_x = 0
        self.mouse_start_y = 0
        self.window.mainloop()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.tiles = []
        self.score_label = tk.Label(
            self.window, text=f"Score: {self.score}", font=("Helvetica", 18, "bold"),
            bg="#bbada0", fg="#ffffff", padx=10, pady=5
        )
        self.score_label.grid(row=0, column=0, columnspan=self.board_size, pady=10)

        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                tile = tk.Label(
                    self.window, text="", bg="#cdc1b4", font=("Helvetica", 30, "bold"),
                    width=4, height=2, borderwidth=4, relief="ridge"
                )
                tile.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(tile)
            self.tiles.append(row)

    def update_ui(self):
        """Обновленный пользовательский интерфейс"""
        self.score_label.config(text=f"Score: {self.score}")
        for i in range(self.board_size):
            for j in range(self.board_size):
                value = self.board[i][j]
                self.tiles[i][j].config(
                    text=str(value) if value != 0 else "",
                    bg=self.colors.get(value, "#3c3a32"),
                    fg="#776e65" if value < 8 else "#f9f6f2"
                )

    def add_new_tile(self):
        """Случайно добавьте новые 2 или 4 в пустые места"""
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == 0]
        if not empty_cells:
            return
        i, j = random.choice(empty_cells)
        self.board[i][j] = 2 if random.random() < 0.9 else 4

    def slide_row_left(self, row):
        """Проведите пальцем влево и объедините строки"""
        new_row = [i for i in row if i != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row[i + 1] = 0
        return [i for i in new_row if i != 0] + [0] * (self.board_size - len(new_row))

    def move_left(self):
        changed = False
        for i in range(self.board_size):
            new_row = self.slide_row_left(self.board[i])
            if new_row != self.board[i]:
                changed = True
                self.board[i] = new_row
        return changed

    def move_right(self):
        changed = False
        for i in range(self.board_size):
            new_row = self.slide_row_left(self.board[i][::-1])[::-1]
            if new_row != self.board[i]:
                changed = True
                self.board[i] = new_row
        return changed

    def move_up(self):
        self.board = self.transpose(self.board)
        changed = self.move_left()
        self.board = self.transpose(self.board)
        return changed

    def move_down(self):
        self.board = self.transpose(self.board)
        changed = self.move_right()
        self.board = self.transpose(self.board)
        return changed

    def transpose(self, matrix):
        return [list(row) for row in zip(*matrix)]

    def check_game_over(self):
        """Проверьте, закончилась ли игра"""
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 0:
                    return False
                if i < self.board_size - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False
                if j < self.board_size - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
        return True

    def mouse_down(self, event):
        self.mouse_start_x = event.x
        self.mouse_start_y = event.y

    def mouse_move(self, event):
        pass

    def mouse_up(self, event):
        dx = event.x - self.mouse_start_x
        dy = event.y - self.mouse_start_y
        if abs(dx) > abs(dy):
            if dx > 0:
                moved = self.move_right()
            else:
                moved = self.move_left()
        else:
            if dy > 0:
                moved = self.move_down()
            else:
                moved = self.move_up()

        if moved:
            self.add_new_tile()
            self.update_ui()
            if self.check_game_over():
                self.game_running = False
                messagebox.showinfo("Game Over", "Game Over! No more moves available.")


if __name__ == "__main__":
    Game2048()
