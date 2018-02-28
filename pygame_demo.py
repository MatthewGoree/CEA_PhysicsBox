# Conversions:
# atm 100 pixels = 1 m; 1 iteration = 1 sec
# Decide on uniform framerate?

import sys, pygame
import numpy as np
from properties import *
from objects import *
from speed_and_acceleration import *
clock = pygame.time.Clock()
pygame.init()

size = width, height = 600, 600
### TO GET RID OF LIQUID SET THIS TO ZERO ###
amount_liquid = 600*600*.4
liquid_height = height - amount_liquid / width # pixels

liquid = water
material = copper
gravity = 5
# Coefficient of friction on the floor
friction = 0.01
speed = [6,0]
tmove = [6,0]

screen = pygame.display.set_mode(size)

radius = 50
ball_size = [2*radius, 2*radius]
ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, ball_size)

ball = MassObject("ball.png", radius, material)

while 1:

    # Arbitrary framerate
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    # Moves ball
    ball.rect = ball.rect.move(tmove)

    # Makes ball bounce off walls
    ball_bounce_wall(ball, size, speed)

    # Calculates accelerations due to various forces
    speed_change(ball, liquid, height, liquid_height, friction, speed, gravity)

    # Temporary moving variable
    tmove = balls_dont_move_thru_walls(ball, size, speed)

    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, liquid.color, (0, liquid_height, width, height))
    color_surface(ball.image, material.color)
    # Adds a black border to the circle
    pygame.draw.circle(ball.image, (0,0,0), (ball.radius,ball.radius), ball.radius, 2)
    screen.blit(ball.image, ball.rect)
    pygame.display.flip()
    clock.tick()
