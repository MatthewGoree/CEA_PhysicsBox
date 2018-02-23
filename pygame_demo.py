# Conventions:
# atm 1 pixel = 1 m; 1 iteration = 1 sec
# Decide on uniform framerate?

import sys, pygame
import numpy as np
from properties import *
from objects import *
clock = pygame.time.Clock()
pygame.init()

size = width, height = 600, 600
ball_size = 100, 100 # Must be even to have an int ball.radius
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
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("ball.png")
ball = pygame.transform.scale(ball, ball_size)
radius = 50


#ball.mass = material.density * ball.volume
# ball.rect = ball.get_rect()

ball = MassObject("ball.png", 50, copper)

#buoyancy = ball.volume * gravity * liquid.density

while 1:

    # Arbitrary framerate
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ball.rect = ball.rect.move(tmove)

    # Makes ball bounce off walls
    if ball.rect.left <= 0 or ball.rect.right >= width:
        speed[0] = -material.CoR * speed[0]
    if ball.rect.top <= 0 or ball.rect.bottom >= height:
        speed[1] = -material.CoR * speed[1]

    # Adds acceleration due to gravity
    if ball.rect.top >= 0:
        speed[1] = speed[1] + gravity

    # Buoyancy and drag force in liquid
    if ball.rect.bottom > liquid_height:
        # Allows for buoyancy/drag of partially submerged ball.masses
        if ball.rect.top < liquid_height:
            h = ball.rect.bottom - liquid_height
            if ball.radius >= h:
                r_submerged = (2*h*ball.radius - h**2)**(1/2)
                vol_submerged = np.pi * h ** 2 / 3 * (3 * ball.radius - h)
                # Central angle of partial circle
                theta = 2 * np.arccos((ball.radius - h) / ball.radius)
            else:
                h_temp = 2 * ball.radius - h
                r_submerged = 2 * np.tan(np.arccos((h - ball.radius) / ball.radius)) * (h - ball.radius)
                vol_submerged = ball.volume - np.pi * h_temp ** 2 / 3 * (3 * ball.radius - h_temp)
                # Central angle of partial circle
                theta = 2 * np.arccos(h_temp / ball.radius)
            #area_submerged = np.pi * r_submerged**2
            # Ratio of area submerged to total area
            ratio = (ball.radius**2 / 2 * (theta - np.sin(theta))) / (np.pi * ball.radius**2)
            buoy_submerged = vol_submerged * liquid.density * gravity
            acc_b = buoy_submerged / ball.mass
            # Modified Stokes' flow
            Fdx = 6 * np.pi * liquid.viscosity * ball.radius * speed[0] * ratio
            Fdy = 6 * np.pi * liquid.viscosity * r_submerged * speed[1]
        else:
            acc_b = buoyancy(ball, liquid, gravity) / ball.mass
            # Stokes' flow
            Fdx = 6 * np.pi * liquid.viscosity * ball.radius * speed[0]
            Fdy = 6 * np.pi * liquid.viscosity * ball.radius * speed[1]
        if ball.rect.bottom == height:
            if speed[0] > 0:
                acc_fric = friction * gravity
            else:
                acc_fric = -friction * gravity
        else:
            acc_fric = 0
        acc_dx = Fdx / ball.mass
        acc_dy = Fdy / ball.mass
        speed[0] = speed[0] - acc_dx - acc_fric
        speed[1] = speed[1] - acc_dy - abs(acc_b)

    # Prevents ball from moving through walls
    tmove[0] = speed[0]
    tmove[1] = speed[1]
    if speed[0] < 0:
        if speed[0] < -ball.rect.left:
            tmove[0] = -ball.rect.left
    else:
        x_dist_right = width - ball.rect.right
        if speed[0] > x_dist_right:
            tmove[0] = x_dist_right
    if speed[1] < 0:
        if speed[1] < -ball.rect.top:
            tmove[1] = -ball.rect.top
    else:
        y_dist_bottom = height - ball.rect.bottom
        if speed[1] > y_dist_bottom:
            tmove[1] = y_dist_bottom




    screen.fill(black)
    pygame.draw.rect(screen, liquid.color, (0, liquid_height, width, height))
    color_surface(ball.image, material.color)
    # Adds a black border to the circle
    pygame.draw.circle(ball.image, (0,0,0), (ball.radius,ball.radius), ball.radius, 2)
    screen.blit(ball.image, ball.rect)
    pygame.display.flip()
    clock.tick()
