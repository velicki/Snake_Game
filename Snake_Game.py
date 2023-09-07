from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 250
SPACE_SAZE = 50
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
            square = canvas.create_rectangle(x, y, x + SPACE_SAZE, y + SPACE_SAZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SAZE)-1) * SPACE_SAZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SAZE)-1) * SPACE_SAZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SAZE, y + SPACE_SAZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    
    x, y = snake.coordinates[0]

    if direction =="up":
        y -= SPACE_SAZE

    elif direction =="down":
        y += SPACE_SAZE

    elif direction =="left":
        x -= SPACE_SAZE

    elif direction =="right":
        x += SPACE_SAZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SAZE, y + SPACE_SAZE, fill=SNAKE_COLOR)

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

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2-70, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2+20, font=('consolas', 35), text="Play Again?", fill="red", tag="gameover")

    button1 = Button(canvas, text = "Yes", command = new_game, anchor = W)
    button1.configure(width = 10, activebackground = "red", relief = FLAT)
    button1_window = canvas.create_window(canvas.winfo_width()/2-120, canvas.winfo_height()/2+75, anchor=NW, window=button1)

    button2 = Button(canvas, text = "No", command = canvas.quit, anchor = W)
    button2.configure(width = 10, activebackground = "red", relief = FLAT)
    button2_window = canvas.create_window(canvas.winfo_width()/2+20, canvas.winfo_height()/2+75, anchor=NW, window=button2)

def new_game():
    canvas.delete(ALL)
    global score
    score = 0
    label.config(text="Score:{}".format(score))
    global direction
    direction = 'down'
    snake = Snake()
    food = Food()
    next_turn(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score), font=('consolas', 15))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Up>', lambda event: change_direction('up'))

new_game()

window.mainloop()