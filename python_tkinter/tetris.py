import tkinter as tk
import random

class Tetris:
    COLS = 10
    ROWS = 20
    CELL = 30
    TICK_MS = 500  # base gravity (milliseconds between automatic drops)

    # Editable key bindings
    # NOTE: Space now ROTATES clockwise; hard drop is on Shift (left/right).
    KEYS = {
        "left":        ["Left", "a", "A"],
        "right":       ["Right", "d", "D"],
        "down":        ["Down", "s", "S"],            # soft drop
        "rotate_cw":   ["Up", "x", "X", "space"],     # rotate clockwise  (now includes Space)
        "rotate_ccw":  ["z", "Z"],                    # rotate counter-clockwise
        "hard_drop":   ["Shift_L", "Shift_R"],        # instant drop to bottom
        "pause":       ["p", "P"],
        "restart":     ["r", "R"],
    }

    # Tetromino definitions as rotation states (1 = filled cell)
    SHAPES = {
        'I': [
            [[1,1,1,1]],
            [[1],[1],[1],[1]],
        ],
        'O': [
            [[1,1],
             [1,1]]
        ],
        'T': [
            [[0,1,0],
             [1,1,1]],
            [[1,0],
             [1,1],
             [1,0]],
            [[1,1,1],
             [0,1,0]],
            [[0,1],
             [1,1],
             [0,1]],
        ],
        'S': [
            [[0,1,1],
             [1,1,0]],
            [[1,0],
             [1,1],
             [0,1]],
        ],
        'Z': [
            [[1,1,0],
             [0,1,1]],
            [[0,1],
             [1,1],
             [1,0]],
        ],
        'J': [
            [[1,0,0],
             [1,1,1]],
            [[1,1],
             [1,0],
             [1,0]],
            [[1,1,1],
             [0,0,1]],
            [[0,1],
             [0,1],
             [1,1]],
        ],
        'L': [
            [[0,0,1],
             [1,1,1]],
            [[1,0],
             [1,0],
             [1,1]],
            [[1,1,1],
             [1,0,0]],
            [[1,1],
             [0,1],
             [0,1]],
        ],
    }

    COLORS = {
        'I': "#00FFFF",
        'O': "#FFFF00",
        'T': "#800080",
        'S': "#00FF00",
        'Z': "#FF0000",
        'J': "#0000FF",
        'L': "#FFA500",
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tetris")
        self.root.resizable(False, False)

        w = self.COLS * self.CELL
        h = self.ROWS * self.CELL

        self.canvas = tk.Canvas(self.root, width=w, height=h, bg="#111")
        self.canvas.grid(row=0, column=0, padx=8, pady=8)

        self.side = tk.Frame(self.root)
        self.side.grid(row=0, column=1, sticky="ns")

        # Side panel stats & status
        self.score_var = tk.StringVar()
        self.level_var = tk.StringVar()
        self.lines_var = tk.StringVar()
        self.status_var = tk.StringVar()
        tk.Label(self.side, textvariable=self.score_var, font=("Consolas", 14)).pack(pady=4)
        tk.Label(self.side, textvariable=self.level_var, font=("Consolas", 14)).pack(pady=4)
        tk.Label(self.side, textvariable=self.lines_var, font=("Consolas", 14)).pack(pady=4)
        tk.Label(self.side, text="Next:", font=("Consolas", 12)).pack(pady=(10,2))
        self.preview_canvas = tk.Canvas(self.side, width=6*self.CELL, height=6*self.CELL, bg="#222")
        self.preview_canvas.pack(pady=4)
        tk.Label(self.side, textvariable=self.status_var, font=("Consolas", 11),
                 fg="#ccc", wraplength=180, justify="left").pack(pady=8)

        # Controls help
        ctrl = tk.LabelFrame(self.side, text="Controls", padx=6, pady=4)
        ctrl.pack(pady=8, fill="x")
        tk.Label(
            ctrl,
            text="←/→: Move\n↓: Soft drop\n↑ / X / Space: Rotate CW\nZ: Rotate CCW\nShift: Hard drop\nP: Pause, R: Restart",
            justify="left"
        ).pack(anchor="w")

        # Buttons
        self.btn_frame = tk.Frame(self.side)
        self.btn_frame.pack(pady=10)
        tk.Button(self.btn_frame, text="Restart", command=self.restart).grid(row=0, column=0, padx=4)
        tk.Button(self.btn_frame, text="Pause/Resume", command=self.toggle_pause).grid(row=0, column=1, padx=4)

        self.bind_keys()
        self.restart()

    # -------------------- Input Binding --------------------
    def bind_keys(self):
        # Helper to bind multiple key strings to one function
        def bind_list(keys, fn):
            for k in keys:
                if k == "space":
                    self.root.bind("<space>", fn)
                elif len(k) == 1 and k.isalnum():
                    self.root.bind(f"<Key-{k}>", fn)
                else:
                    self.root.bind(f"<{k}>", fn)

        bind_list(self.KEYS["left"],        lambda e: self.try_move(-1, 0))
        bind_list(self.KEYS["right"],       lambda e: self.try_move(1, 0))
        bind_list(self.KEYS["down"],        lambda e: self.soft_drop())
        bind_list(self.KEYS["rotate_cw"],   lambda e: self.rotate(+1))
        bind_list(self.KEYS["rotate_ccw"],  lambda e: self.rotate(-1))
        bind_list(self.KEYS["hard_drop"],   lambda e: self.hard_drop())
        bind_list(self.KEYS["pause"],       lambda e: self.toggle_pause())
        bind_list(self.KEYS["restart"],     lambda e: self.restart())

    # -------------------- Game Lifecycle --------------------
    def restart(self):
        # Logical playfield: None = empty, otherwise a color string
        self.grid = [[None for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.gravity = self.TICK_MS
        self.paused = False
        self.game_over = False

        # 7-bag randomizer state
        self.bag = []

        # Active/next piece & UI status
        self.current = None
        self.next_piece = self.random_piece()
        self.rotate_flash = 0  # short-lived visual highlight after rotation
        self.status_var.set("Ready. Good luck!")

        self.spawn_new_piece()
        self.update_side()
        self.draw()
        self.schedule_tick()

    def random_piece(self):
        # 7-bag: refill with all 7 types in random order when empty
        if not self.bag:
            self.bag = list(self.SHAPES.keys())
            random.shuffle(self.bag)
        t = self.bag.pop()
        return {'type': t, 'rot': 0, 'x': 0, 'y': 0}

    def spawn_new_piece(self):
        # Bring in next piece and center it horizontally based on its width
        self.current = self.next_piece
        self.current['rot'] = 0
        mat0 = self.SHAPES[self.current['type']][0]
        piece_w = len(mat0[0])
        self.current['x'] = (self.COLS - piece_w) // 2  # center by width
        self.current['y'] = 0
        self.next_piece = self.random_piece()

        # Immediate collision at spawn = game over
        if self.collides(self.current['x'], self.current['y'], self.current['rot']):
            self.game_over = True
            self.set_title("Game Over! Press Restart.")
            self.status_var.set("Game Over.")
        self.update_side()

    # -------------------- Movement & Rotation --------------------
    def rotate(self, dir_):
        """Rotate current piece with simple wall-kick. dir_=+1 (CW), -1 (CCW)."""
        if self.paused or self.game_over:
            return

        t = self.current['type']
        # O-piece has only one state; still allow 'flash' so the key feels responsive
        rot = (self.current['rot'] + dir_) % len(self.SHAPES[t])

        # Try rotating in place; if blocked, nudge left/right (naive wall-kick)
        for dx in (0, -1, 1, -2, 2):
            if not self.collides(self.current['x'] + dx, self.current['y'], rot):
                self.current['rot'] = rot
                self.current['x'] += dx
                self.rotate_flash = 6
                self.status_var.set("Rotated CW" if dir_ > 0 else "Rotated CCW")
                self.draw()
                return

        # All kicks failed → no rotation
        self.root.bell()
        self.status_var.set("Rotation blocked")

    def try_move(self, dx, dy):
        """Attempt to move active piece by (dx, dy)."""
        if self.paused or self.game_over:
            return
        nx, ny = self.current['x'] + dx, self.current['y'] + dy
        if not self.collides(nx, ny, self.current['rot']):
            self.current['x'], self.current['y'] = nx, ny
            self.draw()

    def soft_drop(self):
        """One-row drop; if blocked, lock the piece."""
        if self.paused or self.game_over:
            return
        if not self.step_down():
            self.lock_piece()

    def hard_drop(self):
        """Instantly drop to the floor; reward small points per row."""
        if self.paused or self.game_over:
            return
        dropped = 0
        while not self.collides(self.current['x'], self.current['y'] + 1, self.current['rot']):
            self.current['y'] += 1
            dropped += 1
        if dropped:
            self.score += dropped
        self.lock_piece()

    # -------------------- Gravity / Tick --------------------
    def schedule_tick(self):
        if not self.game_over:
            self.root.after(self.gravity, self.tick)

    def tick(self):
        # Gravity step each tick (unless paused); then reschedule
        if self.paused or self.game_over:
            self.schedule_tick()
            return

        if not self.step_down():
            self.lock_piece()

        if self.rotate_flash > 0:
            self.rotate_flash -= 1

        self.schedule_tick()

    def step_down(self):
        """Internal helper: try moving active piece down by 1 row."""
        if not self.collides(self.current['x'], self.current['y'] + 1, self.current['rot']):
            self.current['y'] += 1
            self.draw()
            return True
        return False

    # -------------------- Collision / Lock / Clear --------------------
    def shape_matrix(self, t, r):
        return self.SHAPES[t][r]

    def collides(self, x, y, r):
        """Return True if piece at (x,y,r) would overlap walls or settled blocks."""
        mat = self.shape_matrix(self.current['type'], r)
        for i, row in enumerate(mat):
            for j, cell in enumerate(row):
                if not cell:
                    continue
                gx, gy = x + j, y + i
                if gx < 0 or gx >= self.COLS or gy < 0 or gy >= self.ROWS:
                    return True
                if self.grid[gy][gx] is not None:
                    return True
        return False

    def lock_piece(self):
        """Merge active piece into the grid, clear lines, update score/level, then spawn next."""
        t = self.current['type']
        col = self.COLORS[t]
        mat = self.shape_matrix(t, self.current['rot'])

        # Paint current piece onto the grid
        for i, row in enumerate(mat):
            for j, cell in enumerate(row):
                if cell:
                    gx, gy = self.current['x'] + j, self.current['y'] + i
                    if 0 <= gy < self.ROWS and 0 <= gx < self.COLS:
                        self.grid[gy][gx] = col

        # Clear complete lines and award points (classic-ish table)
        lines = self.clear_lines()
        if lines:
            self.lines_cleared += lines
            self.score += [0, 100, 300, 500, 800][lines]  # 0, single, double, triple, tetris

            # Level up every 10 lines; speed up gravity but never below 80ms
            new_level = 1 + self.lines_cleared // 10
            if new_level != self.level:
                self.level = new_level
                self.gravity = max(80, self.TICK_MS - (self.level - 1) * 40)

        self.spawn_new_piece()
        self.update_side()
        self.draw()

    def clear_lines(self):
        """Remove filled rows and return how many were cleared."""
        kept = [row for row in self.grid if any(cell is None for cell in row)]
        cleared = self.ROWS - len(kept)
        for _ in range(cleared):
            kept.insert(0, [None] * self.COLS)  # add empty rows at top
        self.grid = kept
        return cleared

    # -------------------- Rendering --------------------
    def draw(self):
        self.canvas.delete("all")

        # Draw background grid and settled blocks
        for r in range(self.ROWS):
            for c in range(self.COLS):
                x1 = c * self.CELL; y1 = r * self.CELL
                x2 = x1 + self.CELL; y2 = y1 + self.CELL
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="#333", fill="#111")
                if self.grid[r][c]:
                    self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                                 outline="", fill=self.grid[r][c])

        # Draw active piece
        t = self.current['type']
        col = self.COLORS[t]
        mat = self.shape_matrix(t, self.current['rot'])
        for i, row in enumerate(mat):
            for j, cell in enumerate(row):
                if not cell:
                    continue
                gx = self.current['x'] + j
                gy = self.current['y'] + i
                if 0 <= gx < self.COLS and 0 <= gy < self.ROWS:
                    x1 = gx * self.CELL; y1 = gy * self.CELL
                    x2 = x1 + self.CELL; y2 = y1 + self.CELL
                    self.canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                                 outline="", fill=col)
                    # Thin outline flash after a rotation so you can SEE the event
                    if self.rotate_flash > 0:
                        self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 - 3, y2 - 3,
                                                     outline="#FFF")

    def update_side(self):
        self.score_var.set(f"Score: {self.score}")
        self.level_var.set(f"Level: {self.level}")
        self.lines_var.set(f"Lines: {self.lines_cleared}")

        # Draw "next" preview at a fixed offset
        self.preview_canvas.delete("all")
        t = self.next_piece['type']
        col = self.COLORS[t]
        mat = self.shape_matrix(t, 0)
        offx = 1; offy = 1
        for i, row in enumerate(mat):
            for j, cell in enumerate(row):
                if cell:
                    x1 = (offx + j) * self.CELL; y1 = (offy + i) * self.CELL
                    x2 = x1 + self.CELL; y2 = y1 + self.CELL
                    self.preview_canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                                                         outline="", fill=col)

    # -------------------- Misc --------------------
    def set_title(self, msg):
        self.root.title(f"Tetris — {msg}")

    def toggle_pause(self):
        if self.game_over:
            return
        self.paused = not self.paused
        self.set_title("Paused" if self.paused else "Running")
        self.status_var.set("Paused" if self.paused else "Running")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    Tetris().run()
