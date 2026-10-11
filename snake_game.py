import tkinter as tk
import random

CELL = 20
COLS = 30
ROWS = 20
START_DELAY = 120  # milliseconds between moves (lower = faster)

KEYS = {
    "Up": (0, -1), "w": (0, -1),
    "Down": (0, 1), "s": (0, 1),
    "Left": (-1, 0), "a": (-1, 0),
    "Right": (1, 0), "d": (1, 0),
}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        root.title("Snake")
        root.resizable(False, False)

        self.score_label = tk.Label(root, font=("Arial", 14))
        self.score_label.pack(pady=4)

        self.canvas = tk.Canvas(
            root, width=COLS * CELL, height=ROWS * CELL,
            bg="#1e1e1e", highlightthickness=0,
        )
        self.canvas.pack()

        self.high_score = 0
        root.bind("<Key>", self.on_key)
        self.start()

    def start(self):
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.running = True
        self.place_food()
        self.update_score()
        self.tick()

    def place_food(self):
        free = [(x, y) for x in range(COLS) for y in range(ROWS)
                if (x, y) not in self.snake]
        self.food = random.choice(free)

    def update_score(self):
        self.score_label.config(
            text=f"Score: {self.score}    Best: {self.high_score}")

    def on_key(self, event):
        key = event.keysym
        if not self.running:
            if key in ("space", "Return", "r"):
                self.start()
            return
        if key in KEYS:
            new_dir = KEYS[key]
            # Don't allow reversing straight into yourself
            if (new_dir[0] + self.direction[0], new_dir[1] + self.direction[1]) != (0, 0):
                self.next_direction = new_dir

    def tick(self):
        if not self.running:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        hit_wall = not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS)
        hit_self = new_head in self.snake
        if hit_wall or hit_self:
            self.game_over()
            return

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 10
            self.high_score = max(self.high_score, self.score)
            self.update_score()
            self.place_food()
        else:
            self.snake.pop()

        self.draw()
        delay = max(50, START_DELAY - (self.score // 50) * 10)
        self.root.after(delay, self.tick)

    def draw(self):
        self.canvas.delete("all")

        fx, fy = self.food
        self.canvas.create_oval(
            fx * CELL + 2, fy * CELL + 2,
            (fx + 1) * CELL - 2, (fy + 1) * CELL - 2,
            fill="#ff4d4d", outline="",
        )

        for i, (x, y) in enumerate(self.snake):
            color = "#7CFC00" if i == 0 else "#2e9e2e"
            self.canvas.create_rectangle(
                x * CELL + 1, y * CELL + 1,
                (x + 1) * CELL - 1, (y + 1) * CELL - 1,
                fill=color, outline="",
            )

    def game_over(self):
        self.running = False
        self.high_score = max(self.high_score, self.score)
        self.update_score()
        self.draw()
        cx, cy = COLS * CELL // 2, ROWS * CELL // 2
        self.canvas.create_text(
            cx, cy - 15, text="GAME OVER",
            fill="white", font=("Arial", 32, "bold"))
        self.canvas.create_text(
            cx, cy + 25, text="Press SPACE to play again",
            fill="#cccccc", font=("Arial", 14))


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()
