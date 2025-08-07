import tkinter as tk
import tkinter.messagebox

class Othello:
    MOVE_DELAY = 1500  # Time delay between player and AI move (in milliseconds)
    CELL_SIZE = 60     # Size of each square on the board

    # Static heuristic weights for 8x8 board
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
        """Initialize the game window, board state, and create GUI elements."""
        self.BOARD_SIZE = 8       # Can be changed to 16 etc. for larger boards
        self.show_hints = True    # Toggle whether to highlight valid moves

        # Set up main window
        self.window = tk.Tk()
        self.window.title("Othello - Developed by Loc Ha")
        self.window.resizable(False, False)

        # Display status message (e.g., player's turn or game over)
        self.message_label = tk.Label(self.window, text="", font=('normal', 16))
        self.message_label.pack(pady=10)

        # Create canvas for drawing board and pieces
        canvas_size = self.BOARD_SIZE * self.CELL_SIZE
        self.canvas = tk.Canvas(self.window, width=canvas_size, height=canvas_size, bg="green")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Restart button
        self.restart_button = tk.Button(
            self.window, text="Restart Game", font=('normal', 12),
            command=self.restart_game, state=tk.DISABLED
        )
        self.restart_button.pack(pady=10)

        # Initialize board and game state
        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        self.current_player = 1  # 1 = Black (human), -1 = White (AI)

        self.start_new_game()

    def set_message(self, msg):
        """Update the top message label."""
        self.message_label.config(text=msg)

    def restart_game(self):
        """Reset the board and state to start a new game."""
        self.start_new_game()

    def start_new_game(self):
        """Initialize starting 4 pieces and clear board."""
        self.board = [[0 for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)]
        mid = self.BOARD_SIZE // 2
        self.board[mid - 1][mid - 1] = self.board[mid][mid] = 1      # Black
        self.board[mid - 1][mid] = self.board[mid][mid - 1] = -1     # White
        self.current_player = 1
        self.restart_button.config(state=tk.DISABLED)
        self.set_message("Your turn (Black)")
        self.draw_board()

    def on_canvas_click(self, event):
        """Handle mouse click and translate it to a board position."""
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        self.player_move(row, col)

    def draw_board(self):
        """Draw the board grid, pieces, and (if enabled) highlight valid moves."""
        self.canvas.delete("all")

        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                x1 = j * self.CELL_SIZE
                y1 = i * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE

                # Draw grid square
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                # Draw player piece if present
                piece = self.board[i][j]
                if piece != 0:
                    fill = "black" if piece == 1 else "white"
                    margin = 6
                    self.canvas.create_oval(
                        x1 + margin, y1 + margin, x2 - margin, y2 - margin,
                        fill=fill, outline="gray"
                    )

        # Highlight valid moves for human player if hints are enabled
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

    def player_move(self, row, col):
        """Handle human player move, apply it, and trigger AI if valid."""
        if not self.is_valid_move(row, col, self.current_player):
            self.window.bell()
            self.set_message("Not a valid move!")
            return

        self.apply_move(row, col, self.current_player)
        self.current_player *= -1
        self.draw_board()

        # Check for opponent's valid moves
        if not self.has_valid_move(self.current_player):
            if not self.has_valid_move(-self.current_player):
                self.announce_winner()
                return
            self.set_message("No valid move. Switching to you.")
            self.current_player *= -1
            self.draw_board()
            return

        # Trigger AI move
        self.set_message("Machine's turn (White)")
        self.window.after(self.MOVE_DELAY, self.ai_turn)

    def ai_turn(self):
        """AI selects the best move and plays it."""
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

        if not self.has_valid_move(self.current_player):
            if not self.has_valid_move(-self.current_player):
                self.announce_winner()
                return
            self.set_message("No valid move. Switching to machine.")
            self.window.after(self.MOVE_DELAY, self.ai_turn)
            return

        self.set_message("Your turn (Black)")
        self.restart_button.config(state=tk.NORMAL)

    def is_valid_move(self, row, col, player):
        """Check if a move is legal by checking all directions for flips."""
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE) or self.board[row][col] != 0:
            return False
        return any(self.will_flip(row, col, player, dr, dc) for dr, dc in self.directions())

    def will_flip(self, row, col, player, dr, dc):
        """Check if a direction will cause a flip."""
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
        """Place the piece and flip opponent pieces in all valid directions."""
        self.board[row][col] = player
        for dr, dc in self.directions():
            if self.will_flip(row, col, player, dr, dc):
                self.flip_in_direction(row, col, player, dr, dc)

    def flip_in_direction(self, row, col, player, dr, dc):
        """Flip opponent pieces in one direction (used by apply_move)."""
        r, c = row + dr, col + dc
        while 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == -player:
            self.board[r][c] = player
            r += dr
            c += dc

    def get_valid_moves(self, player):
        """Return list of all valid moves for given player."""
        return [(i, j) for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE)
                if self.is_valid_move(i, j, player)]

    def has_valid_move(self, player):
        """Check if player has at least one valid move."""
        return any(self.is_valid_move(i, j, player)
                   for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE))

    def get_best_move_by_pattern(self, player):
        """AI chooses the move with the highest score based on weighted evaluation."""
        best_move = None
        best_score = float('-inf')
        for move in self.get_valid_moves(player):
            score = self.evaluate_move(move[0], move[1], player)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def evaluate_move(self, row, col, player):
        """Score a move using board weights + flip impact."""
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
        """Return all 8 compass directions."""
        return [(0, 1), (1, 0), (0, -1), (-1, 0),
                (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def announce_winner(self):
        """Count final score and declare winner."""
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

    def run(self):
        """Start the game window event loop."""
        self.window.mainloop()


# Entry point
if __name__ == "__main__":
    app = Othello()
    app.run()
