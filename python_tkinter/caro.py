import tkinter as tk
import tkinter.messagebox
import random

class Caro:
    GRID_SIZE = 32          # Number of rows and columns on the board
    WIN_LENGTH = 5          # Number of symbols in a row needed to win
    CELL_SIZE = 24          # Size of each cell in pixels

    def __init__(self):
        # Initialize main window
        self.window = tk.Tk()
        self.window.title("Cờ Caro - 5 in a Row (Canvas)")

        # Create canvas to draw the board
        self.canvas = tk.Canvas(
            self.window,
            width=self.GRID_SIZE * self.CELL_SIZE,
            height=self.GRID_SIZE * self.CELL_SIZE,
            bg="white"
        )
        self.canvas.grid(row=1, column=0, columnspan=self.GRID_SIZE)

        # Label to show messages like whose turn or who won
        self.message_label = tk.Label(self.window, text="", font=('normal', 14))
        self.message_label.grid(row=0, column=0, columnspan=self.GRID_SIZE, pady=5)

        # Restart button to reset the game
        self.restart_button = tk.Button(
            self.window, text="Restart Game", font=('normal', 12),
            command=self.restart_game, state=tk.NORMAL
        )
        self.restart_button.grid(row=2, column=0, columnspan=self.GRID_SIZE, pady=5)

        # Board: 2D list storing game state: 0 = empty, 1 = X, -1 = O
        self.board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_player = 1  # 1 = human (X), -1 = AI (O)
        self.game_over = False

        # Bind mouse click event to board
        self.canvas.bind("<Button-1>", self.handle_click)

        # Draw the grid and show starting message
        self.draw_grid()
        self.set_message("Your turn (X)")

    def draw_grid(self):
        # Draw the grid lines on the canvas
        self.canvas.delete("all")
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                x1 = j * self.CELL_SIZE
                y1 = i * self.CELL_SIZE
                x2 = x1 + self.CELL_SIZE
                y2 = y1 + self.CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray")

    def restart_game(self):
        # Reset the game state
        self.board = [[0 for _ in range(self.GRID_SIZE)] for _ in range(self.GRID_SIZE)]
        self.current_player = 1
        self.game_over = False
        self.draw_grid()
        self.set_message("Your turn (X)")

    def handle_click(self, event):
        # Handle player's click on the board
        if self.game_over or self.current_player != 1:
            return

        row = event.y // self.CELL_SIZE
        col = event.x // self.CELL_SIZE

        if not (0 <= row < self.GRID_SIZE and 0 <= col < self.GRID_SIZE):
            return

        if self.board[row][col] != 0:
            return  # Cell already occupied

        self.make_move(row, col, 1)  # Player makes move
        if not self.check_game_end(row, col):
            self.set_message("AI's turn (O)")
            self.window.after(300, self.ai_move)  # AI makes move after delay

    def ai_move(self):
        # Simple AI move logic
        if self.game_over:
            return
        move = self.best_ai_move()
        if move:
            row, col = move
            self.make_move(row, col, -1)  # AI move
            self.check_game_end(row, col)

    def make_move(self, row, col, player):
        # Place player's symbol on the board and draw it
        self.board[row][col] = player
        x = col * self.CELL_SIZE + self.CELL_SIZE // 2
        y = row * self.CELL_SIZE + self.CELL_SIZE // 2
        symbol = "X" if player == 1 else "O"
        color = "black" if player == 1 else "blue"
        self.canvas.create_text(x, y, text=symbol, font=('normal', 14, 'bold'),
                                fill=color)
        self.current_player *= -1  # Switch turn

    def check_game_end(self, row, col):
        # Check if the game is over (win or draw)
        if self.check_win(row, col):
            winner = "X" if self.board[row][col] == 1 else "O"
            self.set_message(f"Game over! Player {winner} wins!")
            self.game_over = True
            return True

        # Check for draw
        if all(self.board[i][j] != 0 for i in range(self.GRID_SIZE) for j in range(self.GRID_SIZE)):
            self.set_message("Game over! It's a draw.")
            self.game_over = True
            return True

        # Otherwise, continue
        self.set_message("Your turn (X)" if self.current_player == 1 else "AI's turn (O)")
        return False

    def set_message(self, text):
        # Display a message above the board
        self.message_label.config(text=text)

    def check_win(self, row, col):
        # Check if there's a winning line from this cell
        return any(
            1 + self.count_in_direction(row, col, dr, dc) +
            self.count_in_direction(row, col, -dr, -dc) >= self.WIN_LENGTH
            for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]  # Horizontal, Vertical, Diagonal
        )

    def count_in_direction(self, row, col, dr, dc):
        # Count how many same symbols in a direction (excluding the starting cell)
        count = 0
        player = self.board[row][col]
        r, c = row + dr, col + dc
        while 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE and self.board[r][c] == player:
            count += 1
            r += dr
            c += dc
        return count

    def best_ai_move(self):
        # AI selects best move based on evaluation
        best_score = float('-inf')
        best_move = None
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if self.board[i][j] == 0:
                    # Heuristic: favor own moves more, but slightly consider blocking player
                    score = self.evaluate_cell(i, j, -1) + self.evaluate_cell(i, j, 1) * 0.9
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

    def evaluate_cell(self, row, col, player):
        # Evaluate a cell’s potential for the specified player
        total = 0
        for dr, dc in [(0, 1), (1, 0), (1, 1), (1, -1)]:
            count, blocks = self.count_sequence(row, col, dr, dc, player)
            total += self.score_pattern(count, blocks)
        return total

    def count_sequence(self, row, col, dr, dc, player):
        # Count number of player's symbols and blockages around a point
        count = 1
        blocks = 0

        # Forward direction
        r, c = row + dr, col + dc
        while 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE:
            if self.board[r][c] == player:
                count += 1
            elif self.board[r][c] == 0:
                break
            else:
                blocks += 1
                break
            r += dr
            c += dc

        # Backward direction
        r, c = row - dr, col - dc
        while 0 <= r < self.GRID_SIZE and 0 <= c < self.GRID_SIZE:
            if self.board[r][c] == player:
                count += 1
            elif self.board[r][c] == 0:
                break
            else:
                blocks += 1
                break
            r -= dr
            c -= dc

        return count, blocks

    def score_pattern(self, count, blocks):
        # Assign a score to a pattern based on count and blockages
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
        # Start the GUI event loop
        self.window.mainloop()


if __name__ == "__main__":
    app = Caro()
    app.run()
