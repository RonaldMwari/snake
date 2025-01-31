from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 650
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 40, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    restart_button = Button(window, text="Restart", font=('consolas', 20), command=start_game, bg=BACKGROUND_COLOR, fg=SNAKE_COLOR)
    canvas.create_window(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 40, window=restart_button)

def start_game():
    global snake, food, score, direction
    menu_frame.pack_forget()
    game_frame.pack()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    next_turn(snake, food)

def quit_game():
    window.quit()

# Create main window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Set fixed size for the window
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT + 80}")

# Menu frame
menu_frame = Frame(window, width=GAME_WIDTH, height=GAME_HEIGHT + 80, bg=BACKGROUND_COLOR)
menu_frame.pack_propagate(False)
menu_frame.pack()

menu_label = Label(menu_frame, text="Snake by Ronald", font=('consolas', 40), bg=BACKGROUND_COLOR, fg=SNAKE_COLOR)
menu_label.pack(pady=20)

start_button = Button(menu_frame, text="Start", font=('consolas', 20), command=start_game, bg=BACKGROUND_COLOR, fg=SNAKE_COLOR)
start_button.pack(pady=10)

quit_button = Button(menu_frame, text="Quit", font=('consolas', 20), command=quit_game, bg=BACKGROUND_COLOR, fg=SNAKE_COLOR)
quit_button.pack(pady=10)

# Center-align the buttons
start_button.pack(anchor=CENTER)
quit_button.pack(anchor=CENTER)

# Game frame
game_frame = Frame(window, width=GAME_WIDTH, height=GAME_HEIGHT + 80)
game_frame.pack_propagate(False)

label = Label(game_frame, text="Score:{}".format(0), font=('consolas', 40))
label.pack()

canvas = Canvas(game_frame, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Start the application
window.mainloop()
