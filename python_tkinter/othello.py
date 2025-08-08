import tkinter as tk
import tkinter.messagebox

class Othello:
    MOVE_DELAY = 1500
    CELL_SIZE = 60

    PATTERN_WEIGHTS = [
        [100, -20, 10, 5, 5, 10, -20, 100],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [5, -2, -1, -1, -1, -1, -2, 5],
        [10, -2, -1, -1, -1, -1, -2, 10],
        [-20, -50, -2, -2, -2, -2, -50, -20],
        [100, -20, 10, 5, 5, 10, -20, 100],
    ]

    def __init__(self):
        self.BOARD_SIZE = 8
        self.show_hints = False

        self.window = tk.Tk()
        self.window.title("Othello - Developed by Loc Ha")
        self.window.resizable(False, False)

        self.message_label = tk.Label(self.window, text="", font=('normal', 16))
        self.message_label.pack(pady=10)

        canvas_size = self.BOARD_SIZE * self.CELL_SIZE
        self.canvas = tk.Canvas(self.window, width=canvas_size, height=canvas_size, bg="green")
        self.canvas.pack()
        # Mouse Down gives pressed visual only; Mouse Up confirms move
        self.canvas.bind("<Button-1>", self.on_canvas_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_click)

        self.restart_button = tk.Button(
            self.window, text="Restart Game", font=('normal', 12),
            command=self.restart_game, state=tk.DISABLED
        )
        self.restart_button.pack(pady=10)

        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = 1  # 1 = human (Black), -1 = AI (White)
        self.game_over = False
        self.pressed_cell = None

        self.start_new_game()

    def set_message(self, msg):
        self.message_label.config(text=msg)

    def restart_game(self):
        self.start_new_game()

    def start_new_game(self):
        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        mid = self.BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = self.board[mid][mid] = 1
        self.board[mid - 1][mid] = self.board[mid][mid - 1] = -1
        self.current_player = 1
        self.restart_button.config(state=tk.DISABLED)
        self.set_message("Your turn (Black)")
        self.game_over = False
        self.pressed_cell = None
        self.draw_board()

    def on_canvas_press(self, event):
        # Ignore presses when it's not the human's turn or game ended
        if self.current_player != 1 or self.game_over:
            return
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        if 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE:
            self.pressed_cell = (row, col)
            self.draw_board()

    def on_canvas_click(self, event):
        # Only confirm if releasing over the same cell that was pressed
        if self.current_player != 1 or self.game_over:
            self.pressed_cell = None
            return
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        if self.pressed_cell == (row, col):
            self.player_move(row, col)
        self.pressed_cell = None
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x1 = j * self.CELL_SIZE
                y1 = i * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                piece = self.board[i][j]
                if piece != 0:
                    fill = "black" if piece == 1 else "white"
                    margin = 6
                    self.canvas.create_oval(
                        x1 + margin, y1 + margin, x2 - margin, y2 - margin,
                        fill=fill, outline="gray"
                    )

        # Optional hints only when it's the human's turn
        if self.show_hints and self.current_player == 1:
            for i in range(self.BOARD_SIZE):
                for j in range(self.BOARD_SIZE):
                    if self.is_valid_move(i, j, 1):
                        x1 = j * self.CELL_SIZE
                        y1 = i * self.CELL_SIZE
                        x2 = x1 + self.CELL_SIZE
                        y2 = y1 + self.CELL_SIZE
                        margin = 20
                        self.canvas.create_oval(
                            x1 + margin, y1 + margin, x2 - margin, y2 - margin,
                            outline="black", width=1, fill="#dddddd"
                        )

        # Overlay pressed cell for tactile feedback
        if self.pressed_cell and self.current_player == 1 and not self.game_over:
            self.draw_pressed_cell(*self.pressed_cell)

    def draw_pressed_cell(self, row, col):
        # Repaint cell with different fill to simulate a button press
        x1 = col * self.CELL_SIZE
        y1 = row * self.CELL_SIZE
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#9acd32", outline="black")
        piece = self.board[row][col]
        if piece != 0:
            fill = "black" if piece == 1 else "white"
            margin = 8
            self.canvas.create_oval(
                x1 + margin, y1 + margin, x2 - margin, y2 - margin,
                fill=fill, outline="gray"
            )

    def player_move(self, row, col):
        # Validate and apply human move; then hand turn to AI (or pass if AI blocked)
        if not self.is_valid_move(row, col, self.current_player):
            self.window.bell()
            self.set_message("Not a valid move!")
            return

        self.apply_move(row, col, self.current_player)
        self.current_player *= -1
        self.draw_board()

        # If AI has no moves: either game ends or turn passes back to human
        if not self.has_valid_move(self.current_player):
            if not self.has_valid_move(-self.current_player):
                self.announce_winner()
                return
            self.set_message("No valid move. Switching to you.")
            self.current_player *= -1
            self.draw_board()
            return

        self.set_message("Machine's turn (White)")
        self.window.after(self.MOVE_DELAY, self.ai_turn)

    def ai_turn(self):
        # AI may also be forced to pass; handle game end on double-pass
        if not self.has_valid_move(self.current_player):
            if not self.has_valid_move(-self.current_player):
                self.announce_winner()
                return
            self.set_message("No valid move. Switching to you.")
            self.current_player *= -1
            self.draw_board()
            return

        move = self.get_best_move_by_pattern(self.current_player)
        if move:
            self.apply_move(move[0], move[1], self.current_player)

        self.current_player *= -1
        self.draw_board()

        # If human has no moves, immediately pass back to AI (flip back before scheduling)
        if not self.has_valid_move(self.current_player):
            if not self.has_valid_move(-self.current_player):
                self.announce_winner()
                return
            self.set_message("No valid move. Switching to machine.")
            self.current_player *= -1
            self.window.after(self.MOVE_DELAY, self.ai_turn)
            return

        self.set_message("Your turn (Black)")
        self.restart_button.config(state=tk.NORMAL)

    def is_valid_move(self, row, col, player):
        # Legal if empty and at least one direction flips at least one opponent disc
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE) or self.board[row][col] != 0:
            return False
        return any(self.will_flip(row, col, player, dr, dc) for dr, dc in self.directions())

    def will_flip(self, row, col, player, dr, dc):
        # Scan outward: must see one or more opponent pieces then a player piece
        r, c = row + dr, col + dc
        found_opponent = False
        while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
            if self.board[r][c] == -player:
                found_opponent = True
            elif self.board[r][c] == player:
                return found_opponent
            else:
                return False
            r += dr
            c += dc
        return False

    def apply_move(self, row, col, player):
        self.board[row][col] = player
        for dr, dc in self.directions():
            if self.will_flip(row, col, player, dr, dc):
                self.flip_in_direction(row, col, player, dr, dc)

    def flip_in_direction(self, row, col, player, dr, dc):
        r, c = row + dr, col + dc
        while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == -player:
            self.board[r][c] = player
            r += dr
            c += dc

    def get_valid_moves(self, player):
        return [(i, j) for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE)
                if self.is_valid_move(i, j, player)]

    def has_valid_move(self, player):
        return any(self.is_valid_move(i, j, player)
                   for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE))

    def get_best_move_by_pattern(self, player):
        # Simple static evaluation: prioritize corners/edges by PATTERN_WEIGHTS
        best_move = None
        best_score = float('-inf')
        for move in self.get_valid_moves(player):
            score = self.evaluate_move(move[0], move[1], player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def evaluate_move(self, row, col, player):
        # Simulate flips and score by weights (or uniform if not 8x8)
        weight_grid = self.PATTERN_WEIGHTS
        score = weight_grid[row][col] if self.BOARD_SIZE == 8 else 0

        temp = [r[:] for r in self.board]
        temp[row][col] = player

        for dr, dc in self.directions():
            flips = []
            r, c = row + dr, col + dc
            while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and temp[r][c] == -player:
                flips.append((r, c))
                r += dr
                c += dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and temp[r][c] == player:
                for fr, fc in flips:
                    score += weight_grid[fr][fc] if self.BOARD_SIZE == 8 else 1

        return score

    def directions(self):
        return [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def announce_winner(self):
        # Guard future clicks by setting game_over; leave board visible
        black = sum(r.count(1) for r in self.board)
        white = sum(r.count(-1) for r in self.board)
        if black > white:
            result = "Black wins!"
        elif white > black:
            result = "White wins!"
        else:
            result = "It's a tie!"
        self.set_message(f"Game over! {result} (Black: {black}, White: {white})")
        self.restart_button.config(state=tk.NORMAL)
        self.game_over = True

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = Othello()
    app.run()
