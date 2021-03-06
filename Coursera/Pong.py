# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(120, 240) / 60, - random.randrange(60, 180) / 60]
    
    if(direction == LEFT):
        ball_vel[0] = -ball_vel[0]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    paddle1_pos = [[HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT], [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    direction = random.randrange(0,2)
    if(direction == 1):
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'WHITE', 'WHITE')
    
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0][1] < 0:
        paddle1_pos[0][1] = 0
        paddle1_pos[1][1] = PAD_HEIGHT
    elif paddle1_pos[1][1] > HEIGHT:
        paddle1_pos[0][1] = HEIGHT - PAD_HEIGHT
        paddle1_pos[1][1] = HEIGHT
    else:
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
        
    if paddle2_pos[0][1] < 0:
        paddle2_pos[0][1] = 0
        paddle2_pos[1][1] = PAD_HEIGHT
    elif paddle2_pos[1][1] > HEIGHT:
        paddle2_pos[0][1] = HEIGHT - PAD_HEIGHT
        paddle2_pos[1][1] = HEIGHT
    else:
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
            
    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, 'WHITE')
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, 'WHITE')
    
    # determine whether paddle and ball collide    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS and (ball_pos[1] >= paddle1_pos[0][1] and ball_pos[1] <= paddle1_pos[1][1]):
        ball_vel[0] = - (ball_vel[0] * 1.1)
        ball_vel[1] = (ball_vel[1] * 1.1)
    elif ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        score2 += 1
        spawn_ball(RIGHT)

    if ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS) and (ball_pos[1] >= paddle2_pos[0][1] and ball_pos[1] <= paddle2_pos[1][1]):
        ball_vel[0] = - (ball_vel[0] * 1.1)
        ball_vel[1] = (ball_vel[1] * 1.1)
    elif ball_pos[0] >= WIDTH - (PAD_WIDTH + BALL_RADIUS):
        score1 += 1
        spawn_ball(LEFT)

    if ball_pos[1] >= HEIGHT - BALL_RADIUS or ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # draw scores
    canvas.draw_text(str(score1), (80, 60), 25, 'White')
    canvas.draw_text(str(score2), (520, 60), 25, 'White')
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -4
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -4
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 4
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 4

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', new_game, 100)

# start frame
new_game()
frame.start()
