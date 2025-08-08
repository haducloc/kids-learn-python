import tkinter as tk
import tkinter.messagebox

class Caro:
    GRID_SIZE = 24
    WIN_LENGTH = 5
    CELL_SIZE = 32

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Cờ Caro - 5 in a Row (Canvas)")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(
            self.window,
            width=self.GRID_SIZE * self.CELL_SIZE,
            height=self.GRID_SIZE * self.CELL_SIZE,
            bg="white"
        )
        self.canvas.grid(row=1, column=0, columnspan=self.GRID_SIZE)

        self.message_label = tk.Label(self.window, text="", font=('normal', 14))
        self.message_label.grid(row=0, column=0, columnspan=self.GRID_SIZE, pady=5)

        self.restart_button = tk.Button(
            self.window, text="Restart Game", font=('normal', 12),
            command=self.restart_game, state=tk.NORMAL
        )
        self.restart_button.grid(row=2, column=0, columnspan=self.GRID_SIZE, pady=5)

        self.board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_player = 1  # 1 = human (X), -1 = AI (O)
        self.game_over = False
        self.pressed_cell = None  # remember where mouse went down

        # Mouse Down = pressed visual; Mouse Up = confirm move
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.draw_board()
        self.set_message("Your turn (X)")

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                x1 = j * self.CELL_SIZE
                y1 = i * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

                v = self.board[i][j]
                if v != 0:
                    cx = x1 + self.CELL_SIZE // 2
                    cy = y1 + self.CELL_SIZE // 2
                    self.canvas.create_text(
                        cx, cy,
                        text=("X" if v == 1 else "O"),
                        font=('normal', 14, 'bold'),
                        fill=("black" if v == 1 else "blue")
                    )

        # pressed feedback overlay (only on empty cell and human turn)
        if self.pressed_cell and not self.game_over and self.current_player == 1:
            r, c = self.pressed_cell
            if self.board[r][c] == 0:
                x1 = c * self.CELL_SIZE
                y1 = r * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#e6e6e6", outline="gray")

    def restart_game(self):
        self.board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_player = 1
        self.game_over = False
        self.pressed_cell = None
        self.draw_board()
        self.set_message("Your turn (X)")

    def on_press(self, event):
        # ignore during AI turn or after game end; don't show pressed on occupied cells
        if self.game_over or self.current_player != 1:
            return
        r = event.y // self.CELL_SIZE
        c = event.x // self.CELL_SIZE
        if not (0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE):
            return
        if self.board[r][c] != 0:
            self.pressed_cell = None
            self.draw_board()
            return
        self.pressed_cell = (r, c)
        self.draw_board()

    def on_release(self, event):
        # commit only if release matches press; otherwise (if there was a press) beep
        if self.game_over or self.current_player != 1:
            self.pressed_cell = None
            return
        r = event.y // self.CELL_SIZE
        c = event.x // self.CELL_SIZE

        # If release is outside the board, just clear the visual
        if not (0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE):
            self.pressed_cell = None
            self.draw_board()
            return

        if self.pressed_cell is not None and self.pressed_cell == (r, c):
            self.handle_move(r, c)
        elif self.pressed_cell is not None:
            self.window.bell()

        self.pressed_cell = None
        self.draw_board()

    def handle_move(self, row, col):
        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return
        if self.board[row][col] != 0:
            return
        self.make_move(row, col, 1)
        if not self.check_game_end(row, col):
            self.set_message("AI's turn (O)")
            self.window.after(300, self.ai_move)

    def ai_move(self):
        if self.game_over:
            return
        move = self.best_ai_move()
        if not move:
            # AI has no valid move → pass turn back to human
            self.set_message("AI has no move. Your turn (X)")
            self.current_player = 1
            return
        r, c = move
        self.make_move(r, c, -1)
        self.check_game_end(r, c)

    def make_move(self, row, col, player):
        self.board[row][col] = player
        x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = row * self.CELL_SIZE + self.CELL_SIZE // 2
        self.canvas.create_text(
            x, y,
            text=("X" if player == 1 else "O"),
            font=('normal', 14, 'bold'),
            fill=("black" if player == 1 else "blue")
        )
        self.current_player *= -1  # swap turns

    def check_game_end(self, row, col):
        if self.check_win(row, col):
            winner = "X" if self.board[row][col] == 1 else "O"
            self.set_message(f"Game over! Player {winner} wins!")
            self.game_over = True
            return True

        if all(self.board[i][j] != 0 for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE)):
            self.set_message("Game over! It's a draw.")
            self.game_over = True
            return True

        self.set_message("Your turn (X)" if self.current_player == 1 else "AI's turn (O)")
        return False

    def set_message(self, text):
        self.message_label.config(text=text)

    def check_win(self, row, col):
        # 5-in-a-row if current cell connects to >= WIN_LENGTH across any axis
        return any(
            1 + self.count_in_direction(row, col, dr, dc) +
            self.count_in_direction(row, col, -dr, -dc) >= self.WIN_LENGTH
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]
        )

    def count_in_direction(self, row, col, dr, dc):
        count = 0
        player = self.board[row][col]
        r, c = row + dr, col + dc
        while 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    def best_ai_move(self):
        # evaluate every empty cell; slight weight on blocking opponent
        best_score = float('-inf')
        best_move = None
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.board[i][j] == 0:
                    score = self.evaluate_cell(i, j, -1) + self.evaluate_cell(i, j, 1) * 0.9
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def evaluate_cell(self, row, col, player):
        total = 0
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count, blocks = self.count_sequence(row, col, dr, dc, player)
            total += self.score_pattern(count, blocks)
        return total

    def count_sequence(self, row, col, dr, dc, player):
        # count contiguous stones including hypothetical at (row,col); track edge/stone blocks
        count = 1
        blocks = 0

        r, c = row + dr, col + dc
        while 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE:
            if self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            elif self.board[r][c] == 0:
                break
            else:
                blocks += 1
                break
        if not (0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE):
            blocks += 1

        r, c = row - dr, col - dc
        while 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE:
            if self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            elif self.board[r][c] == 0:
                break
            else:
                blocks += 1
                break
        if not (0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE):
            blocks += 1

        return count, blocks

    def score_pattern(self, count, blocks):
        # high score for open-ended longer runs; reduced when blocked
        if count >= 5:
            return 100000
        if count == 4:
            return 10000 if blocks == 0 else 1000
        if count == 3:
            return 500 if blocks == 0 else 100
        if count == 2:
            return 10
        if count == 1:
            return 1
        return 0

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Caro()
    app.run()
