from cs1lib import *
import random

MOVE_UP_LEFT_PADDLE = 'a'
MOVE_DOWN_LEFT_PADDLE = 'z'

# Keys for directing the game
QUIT = 'q'
START = ' '

# Radius of the circle
RADIUS = 15

# Window size
WIN_SIZE = 500

# Width and height of the paddles
WIDTH = 20
HEIGHT = 80

# Movement in pixel of paddle when the key is pressed
MOVEMENT = 20

# Movement in pixel for heuristic-based intuition
MOVEMENT_COMP= 15

# The x_coordinates of the paddles
XLEFT = 0
XRIGHT = WIN_SIZE - WIDTH

# Setting the value of key pressed to False
a_pressed = False
z_pressed = False

# The y_coordinates of the paddles
ya_left = 0
ya_right = WIN_SIZE // 2 - HEIGHT // 2

# Start
start_pong = False

# End game
end_game = False

# Starting position
ball_x = WIN_SIZE // 2
ball_y = WIN_SIZE // 2

# Ball velocities
BALL_SPEED = 15
vx = 0
vy = 0

# Prediction factor: how many frames ahead to predict
PREDICT_FRAMES = 10

# Initialize wins and other counters
wins = 0  
total_games = 0

def drawing_paddles():
    set_fill_color(0, 0, 1)  
    draw_rectangle(XRIGHT, ya_right, WIDTH, HEIGHT)  
    draw_rectangle(XLEFT, ya_left, WIDTH, HEIGHT) 
    
def draw_ball():
    set_fill_color(0, 1, 0) 
    draw_circle(ball_x, ball_y, RADIUS)

def updated_position():
    global ball_y, ball_x
    ball_y += vy
    ball_x += vx

def check_horizontal_collision():
    global vy
    if ball_y - RADIUS <= 0 or ball_y + RADIUS >= WIN_SIZE:
        vy = -vy

def reset_game():
    global ball_x, ball_y, end_game, start_pong, ya_right, ya_left, total_games, wins
    ball_x = WIN_SIZE // 2
    ball_y = WIN_SIZE // 2
    ya_left = 0
    ya_right = WIN_SIZE // 2 - HEIGHT // 2
    start_pong = False
    end_game = False
    total_games += 1

def wall_collision():
    global end_game, wins
    if ball_x - RADIUS <= 0:
        wins += 1
        reset_game()
    elif ball_x + RADIUS >= WIN_SIZE:
        reset_game()

def check_paddle_collision():
    global vx
    
    if ball_x - RADIUS <= XLEFT + WIDTH and ya_left <= ball_y <= ya_left + HEIGHT:
        vx = BALL_SPEED
    elif ball_x + RADIUS >= XRIGHT and ya_right <= ball_y <= ya_right + HEIGHT:
        vx = -BALL_SPEED

def key_pressed(key):
    global ya_left, a_pressed, z_pressed, vx, vy, start_pong, terminate

    if key == MOVE_UP_LEFT_PADDLE:
        a_pressed = True
    if key == MOVE_DOWN_LEFT_PADDLE:
        z_pressed = True
    if key == START and not start_pong:
        vx = BALL_SPEED
        vy = BALL_SPEED
        start_pong = True

    if key == QUIT:
        cs1_quit()

def key_released(key):
    global ya_left, a_pressed, z_pressed

    if key == MOVE_UP_LEFT_PADDLE:
        a_pressed = False
    if key == MOVE_DOWN_LEFT_PADDLE:
        z_pressed = False

def heuristic_control_paddle():
    global ya_right

    predicted_ball_y = ball_y + vy * PREDICT_FRAMES
    paddle_center_y = ya_right + HEIGHT / 2

    if predicted_ball_y > paddle_center_y and ya_right < WIN_SIZE - HEIGHT:
        ya_right += MOVEMENT_COMP
    elif predicted_ball_y < paddle_center_y and ya_right > 0:
        ya_right -= MOVEMENT_COMP

def main_draw():
    global start_pong, end_game, ya_left, vx, vy

    set_clear_color(0, 0, 0)
    clear()
    
    if z_pressed and (ya_left < WIN_SIZE - HEIGHT):
        ya_left += MOVEMENT
    if a_pressed and (ya_left > 0):
        ya_left -= MOVEMENT

    heuristic_control_paddle()

    if not end_game:
        drawing_paddles()
        draw_ball()

    if start_pong:
        check_horizontal_collision()
        check_paddle_collision()
        wall_collision()
        updated_position()

start_graphics(main_draw, height=WIN_SIZE, width=WIN_SIZE, key_press=key_pressed, key_release=key_released)
