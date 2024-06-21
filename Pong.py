# Purpose: Python code for creating pong game


from cs1lib import *

# Keys for the movement of paddle
MOVE_UP_LEFT_PADDLE = 'a'
MOVE_DOWN_LEFT_PADDLE = 'z'
MOVE_UP_RIGHT_PADDLE = 'k'
MOVE_DOWN_RIGHT_PADDLE = 'm'

# Keys for directing the game
QUIT = 'q'
START = ' '

# Radius of the circle
RADIUS = 15

# window size
# since I consider my window as square the height and the width of the window are equal to window size
WIN_SIZE = 400


# width and height of the paddles
WIDTH = 20
HEIGHT = 80

# movement in pixel of paddle when the key is pressed
MOVEMENT = 20

# the x_coordinates of the paddles
XLEFT = 0
XRIGHT = WIN_SIZE - WIDTH

# setting the value of key pressed to False
a_pressed = False
z_pressed = False
k_pressed = False
m_pressed = False

# Other variables
# the y_coordinates of the paddles
ya_left = 0
ya_right = WIN_SIZE - HEIGHT

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


# function that will draw the paddles
def drawing_paddles():
    # setting the color of paddles to blue
    set_fill_color(0, 0, 1)

    # drawing the right paddle
    draw_rectangle(XRIGHT, ya_right, WIDTH, HEIGHT)

    # drawing the left paddle
    draw_rectangle(XLEFT, ya_left, WIDTH, HEIGHT)


# function that draws the ball
def draw_ball():
    set_fill_color(0, 1, 0)
    draw_circle(ball_x, ball_y, RADIUS)


# function that update the ball function
def updated_position():
    global ball_y, ball_x
    ball_y = ball_y + vy
    ball_x = ball_x + vx


# checking the collision with the ceiling or the floor
def check_horizontal_collision():
    global vy
    if ball_y - RADIUS <= 0 or ball_y + RADIUS >= WIN_SIZE:
        vy = -vy


# this function will reset the game
def reset_game():
    global ball_x, ball_y, end_game, start_pong, ya_right, ya_left
    ball_x = WIN_SIZE // 2
    ball_y = WIN_SIZE // 2
    ya_left = 0
    ya_right = WIN_SIZE - HEIGHT
    start_pong = False
    end_game = False


# this function will check wall collision and end the game
def wall_collision():
    global end_game
    if ball_x - RADIUS <= 0 or ball_x + RADIUS >= WIN_SIZE:
        end_game = True
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


# this function detect they key pressed and change global key pressed to True
def key_pressed(key):
    global ya_left, ya_right, a_pressed, k_pressed, m_pressed, z_pressed, vx, vy, start_pong, terminate

    if key == MOVE_UP_LEFT_PADDLE:
        a_pressed = True
    if key == MOVE_DOWN_LEFT_PADDLE:
        z_pressed = True
    if key == MOVE_DOWN_RIGHT_PADDLE:
        m_pressed = True
    if key == MOVE_UP_RIGHT_PADDLE:
        k_pressed = True

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
    global ya_left, ya_right, a_pressed, k_pressed, m_pressed, z_pressed

    if key == MOVE_UP_LEFT_PADDLE:
        a_pressed = False
    if key == MOVE_DOWN_LEFT_PADDLE:
        z_pressed = False
    if key == MOVE_DOWN_RIGHT_PADDLE:
        m_pressed = False
    if key == MOVE_UP_RIGHT_PADDLE:
        k_pressed = False


def main_draw():
    global start_pong, end_game, ya_left, ya_right, vx, vy

    # setting the background to black
    set_clear_color(0, 0, 0)

    # clearing the screen everytime
    clear()

    # if the key is pressed this will direct the motion
    if z_pressed and (ya_left < WIN_SIZE - HEIGHT):
        ya_left += MOVEMENT
    if a_pressed and (ya_left > 0):
        ya_left -= MOVEMENT
    if m_pressed and (ya_right < WIN_SIZE - HEIGHT):
        ya_right += MOVEMENT
    if k_pressed and (ya_right > 0):
        ya_right -= MOVEMENT

    if not end_game:
        drawing_paddles()
        draw_ball()

    if start_pong:
        check_horizontal_collision()
        check_paddle_collision()
        wall_collision()
        updated_position()

start_graphics(main_draw, height=WIN_SIZE, width=WIN_SIZE, key_press=key_pressed, key_release=key_released)

