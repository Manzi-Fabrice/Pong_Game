# Purpose: Python code for creating pong game with enhanced Q-learning AI

from cs1lib import *
import random
import numpy as np

# Keys for the movement of paddle
MOVE_UP_LEFT_PADDLE = 'a'
MOVE_DOWN_LEFT_PADDLE = 'z'

# Keys for directing the game
QUIT = 'q'
START = ' '

# Radius of the circle
RADIUS = 15

# window size
WIN_SIZE = 500

# width and height of the paddles
WIDTH = 20
HEIGHT = 80

# movement in pixel of paddle when the key is pressed
MOVEMENT = 20

# movement in pixel for AI
MOVEMENT_AI = 15

# the x_coordinates of the paddles
XLEFT = 0
XRIGHT = WIN_SIZE - WIDTH

# setting the value of key pressed to False
a_pressed = False
z_pressed = False

# Other variables
# the y_coordinates of the paddles
ya_left = 0
ya_right = WIN_SIZE // 2 - HEIGHT // 2

# start
start_pong = False

# end game
end_game = False

# starting position
ball_x = WIN_SIZE // 2
ball_y = WIN_SIZE // 2

# Ball velocities
BALL_SPEED = 15
vx = 0
vy = 0

# Q-learning parameters
q_table = {}  # Initialize Q-table
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate
epsilon_decay = 0.995  # Decay rate for epsilon

# Performance metrics
successful_hits = 0
total_games = 0
wins = 0
game_durations = []
hits_per_game = []

# Current game metrics
current_game_duration = 0
current_game_hits = 0


def get_state():
    return (int(ball_x), int(ball_y), int(ya_right))


def choose_action(state):
    if random.random() < epsilon:  # Exploration
        return random.choice(['up', 'down'])
    else:  # Exploitation
        if state not in q_table:
            q_table[state] = {'up': 0, 'down': 0}
        return max(q_table[state].items(), key=lambda x: x[1])[0]


def update_q_table(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = {'up': 0, 'down': 0}
    if next_state not in q_table:
        q_table[next_state] = {'up': 0, 'down': 0}
    q_table[state][action] = q_table[state][action] + alpha * (
            reward + gamma * max(q_table[next_state].values()) - q_table[state][action]
    )


def ai_control_paddle():
    global ya_right, q_table, epsilon, successful_hits, current_game_hits
    state = get_state()  # Define game state
    action = choose_action(state)  # Choose action using Q-table
    reward = 0  # Initialize reward

    # Check ball's direction and move paddle accordingly
    if ball_y < ya_right + HEIGHT // 2 and ya_right > 0:
        ya_right -= MOVEMENT_AI
    elif ball_y > ya_right + HEIGHT // 2 and ya_right < WIN_SIZE - HEIGHT:
        ya_right += MOVEMENT_AI

    next_state = get_state()

    # Rewards and penalties
    if ball_x + RADIUS >= XRIGHT and ya_right <= ball_y <= ya_right + HEIGHT:
        reward = 1  # Reward for hitting the ball
        successful_hits += 1
        current_game_hits += 1
    elif ball_x + RADIUS >= XRIGHT:
        reward = -1  # Penalty for missing the ball

    reward += 0.01  # Small reward for keeping the ball in play

    update_q_table(state, action, reward, next_state)
    epsilon = max(epsilon * epsilon_decay, 0.01)  # Decay epsilon


# function that will draw the paddles
def drawing_paddles():
    set_fill_color(0, 0, 1)  # Blue color for paddles
    draw_rectangle(XRIGHT, ya_right, WIDTH, HEIGHT)  # Right paddle
    draw_rectangle(XLEFT, ya_left, WIDTH, HEIGHT)  # Left paddle


# function that draws the ball
def draw_ball():
    set_fill_color(0, 1, 0)  # Green color for ball
    draw_circle(ball_x, ball_y, RADIUS)


# function that update the ball position
def updated_position():
    global ball_y, ball_x
    ball_y += vy
    ball_x += vx


# checking the collision with the ceiling or the floor
def check_horizontal_collision():
    global vy
    if ball_y - RADIUS <= 0 or ball_y + RADIUS >= WIN_SIZE:
        vy = -vy


# this function will reset the game
def reset_game():
    global ball_x, ball_y, end_game, start_pong, ya_right, ya_left, epsilon, total_games, wins, current_game_duration, current_game_hits
    ball_x = WIN_SIZE // 2
    ball_y = WIN_SIZE // 2
    ya_left = 0
    ya_right = WIN_SIZE // 2 - HEIGHT // 2
    start_pong = False
    end_game = False
    epsilon = 0.1  # Reset epsilon
    total_games += 1
    game_durations.append(current_game_duration)
    hits_per_game.append(current_game_hits)
    current_game_duration = 0
    current_game_hits = 0


# this function will check wall collision and end the game
def wall_collision():
    global end_game, wins
    if ball_x - RADIUS <= 0:
        wins += 1
        reset_game()
    elif ball_x + RADIUS >= WIN_SIZE:
        reset_game()


# this function will check paddle collision
def check_paddle_collision():
    global vx
    # Check collision with left paddle
    if ball_x - RADIUS <= XLEFT + WIDTH and ya_left <= ball_y <= ya_left + HEIGHT:
        vx = BALL_SPEED
    # Check collision with right paddle
    elif ball_x + RADIUS >= XRIGHT and ya_right <= ball_y <= ya_right + HEIGHT:
        vx = -BALL_SPEED


# this function detect the key pressed and change global key pressed to True
def key_pressed(key):
    global ya_left, a_pressed, z_pressed, vx, vy, start_pong, terminate

    if key == MOVE_UP_LEFT_PADDLE:
        a_pressed = True
    if key == MOVE_DOWN_LEFT_PADDLE:
        z_pressed = True

    # starting the game and checking the flag of start pong to ensure that the space bar has effect only one time
    if key == START and not start_pong:
        vx = BALL_SPEED
        vy = BALL_SPEED
        start_pong = True

    # this will quit the game
    if key == QUIT:
        cs1_quit()


# This function detect the key release and set the global key pressed to false
def key_released(key):
    global ya_left, a_pressed, z_pressed

    if key == MOVE_UP_LEFT_PADDLE:
        a_pressed = False
    if key == MOVE_DOWN_LEFT_PADDLE:
        z_pressed = False


def main_draw():
    global start_pong, end_game, ya_left, vx, vy, current_game_duration

    # setting the background to black
    set_clear_color(0, 0, 0)

    # clearing the screen everytime
    clear()

    # if the key is pressed this will direct the motion
    if z_pressed and (ya_left < WIN_SIZE - HEIGHT):
        ya_left += MOVEMENT
    if a_pressed and (ya_left > 0):
        ya_left -= MOVEMENT

    # AI control for the right paddle
    ai_control_paddle()

    if not end_game:
        drawing_paddles()
        draw_ball()

    if start_pong:
        check_horizontal_collision()
        check_paddle_collision()
        wall_collision()
        updated_position()
        current_game_duration += 1


start_graphics(main_draw, height=WIN_SIZE, width=WIN_SIZE, key_press=key_pressed, key_release=key_released)
