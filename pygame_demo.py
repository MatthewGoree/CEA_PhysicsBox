# Conventions:
# atm 1 pixel = 1 m; 1 iteration = 1 sec
# Decide on uniform framerate?

import sys, pygame, numpy
from properties import *
clock = pygame.time.Clock()
pygame.init()

size = width, height = 600, 600
ball_size = 100, 100 # Must be even to have an int radius
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
radius = int(ball_size[0] / 2)
volume = 4 / 3 * numpy.pi * radius**3

buoyancy = volume * gravity * liquid.density
mass = material.density * volume
ballrect = ball.get_rect()


while 1:

    # Arbitrary framerate
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    ballrect = ballrect.move(tmove)

    # Makes ball bounce off walls
    if ballrect.left <= 0 or ballrect.right >= width:
        speed[0] = -material.CoR * speed[0]
    if ballrect.top <= 0 or ballrect.bottom >= height:
        speed[1] = -material.CoR * speed[1]

    # Adds acceleration due to gravity
    if ballrect.top >= 0:
        speed[1] = speed[1] + gravity

    # Buoyancy and drag force in liquid
    if ballrect.bottom > liquid_height:
        # Allows for buoyancy/drag of partially submerged masses
        if ballrect.top < liquid_height:
            h = ballrect.bottom - liquid_height
            if radius >= h:
                r_submerged = (2*h*radius - h**2)**(1/2)
                vol_submerged = numpy.pi * h ** 2 / 3 * (3 * radius - h)
                # Central angle of partial circle
                theta = 2 * numpy.arccos((radius - h) / radius)
            else:
                h_temp = 2 * radius - h
                r_submerged = 2 * numpy.tan(numpy.arccos((h - radius) / radius)) * (h - radius)
                vol_submerged = volume - numpy.pi * h_temp ** 2 / 3 * (3 * radius - h_temp)
                # Central angle of partial circle
                theta = 2 * numpy.arccos(h_temp / radius)
            #area_submerged = numpy.pi * r_submerged**2
            # Ratio of area submerged to total area
            ratio = (radius**2 / 2 * (theta - numpy.sin(theta))) / (numpy.pi * radius**2)
            buoy_submerged = vol_submerged * liquid.density * gravity
            acc_b = buoy_submerged / mass
            # Modified Stokes' flow
            Fdx = 6 * numpy.pi * liquid.viscosity * radius * speed[0] * ratio
            Fdy = 6 * numpy.pi * liquid.viscosity * r_submerged * speed[1]
        else:
            acc_b = buoyancy / mass
            # Stokes' flow
            Fdx = 6 * numpy.pi * liquid.viscosity * radius * speed[0]
            Fdy = 6 * numpy.pi * liquid.viscosity * radius * speed[1]
        if ballrect.bottom == height:
            if speed[0] > 0:
                acc_fric = friction * (gravity - buoyancy/mass)
            else:
                acc_fric = -friction * (gravity - buoyancy/mass)
        else:
            acc_fric = 0
        acc_dx = Fdx / mass
        acc_dy = Fdy / mass
        speed[0] = speed[0] - acc_dx - acc_fric
        speed[1] = speed[1] - acc_dy - abs(acc_b)

    # Prevents ball from moving through walls
    tmove[0] = speed[0]
    tmove[1] = speed[1]
    if speed[0] < 0:
        if speed[0] < -ballrect.left:
            tmove[0] = -ballrect.left
    else:
        x_dist_right = width - ballrect.right
        if speed[0] > x_dist_right:
            tmove[0] = x_dist_right
    if speed[1] < 0:
        if speed[1] < -ballrect.top:
            tmove[1] = -ballrect.top
    else:
        y_dist_bottom = height - ballrect.bottom
        if speed[1] > y_dist_bottom:
            tmove[1] = y_dist_bottom


    screen.fill(black)
    pygame.draw.rect(screen, liquid.color, (0, liquid_height, width, height))
    color_surface(ball, material.color)
    # Adds a black border to the circle
    pygame.draw.circle(ball, (0,0,0), (radius,radius), radius, 2)
    screen.blit(ball, ballrect)
    pygame.display.flip()
    clock.tick()
