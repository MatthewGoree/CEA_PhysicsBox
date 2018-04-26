# Conversions:
# atm 100 pixels = 1 m; 1 iteration = 1 sec
# Decide on uniform framerate?

import random
import sys
from objects import *
from speed_and_acceleration import *
from properties import *
clock = pygame.time.Clock()
pygame.init()

size = width, height = 600, 600
### TO GET RID OF LIQUID SET THIS TO ZERO ###
amount_liquid = 600*600*.4
liquid_height = height - amount_liquid / width # pixels

liquid = syrup
liquids = [water, olive_oil, syrup, molasses]
x = random.randint(0, len(liquids)-1)
liquid = liquids[x]
#material = copper
materials = [silicon, aluminum, copper, lead]
gravity_init = 2
gravity = gravity_init
counter = -1

# Coefficient of friction on the floor
friction = 0.01
temp_speed = [0,0]
mouse_bool = []

screen = pygame.display.set_mode(size)

number_of_particles = random.randint(3, 10)
my_particles = []

for n in range(number_of_particles):
    speed = []
    radius = random.randint(20, 50)
    material = materials[random.randint(0, len(materials)-1)]
    x = 50#random.randint(radius, width - radius)
    y = 50#random.randint(radius, height - radius)
    speed.append(random.randint(0,10))
    speed.append(random.randint(0,1))

    particle = MassObject(x, y, radius, material, speed, counter)
    my_particles.append(particle)

selected_particle = None



running = True
X = []
Y = []
while running:

    # Arbitrary framerate
    dt = clock.tick(30)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None


    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, liquid.color, (0, liquid_height, width, height))
    pygame.draw.line(screen, (0, 0, 0), (0, liquid_height), (width, liquid_height), 1)


    for i, particle in enumerate(my_particles):

        if i == selected_particle:
            particle.counter += 1
            (mouseX, mouseY) = pygame.mouse.get_pos()
            particle.x = mouseX
            particle.y = mouseY
            X.append(mouseX)
            Y.append(mouseY)
            gravity = 0
        if particle.counter > 0 and mouse_bool[i] == False:
            if particle.counter < 10:
                speed_x = ((X[particle.counter] - X[0]) / particle.counter)
                speed_y = ((Y[particle.counter] - Y[0]) / particle.counter)
            else:
                speed_x = ((X[particle.counter] - X[particle.counter-10])/10)
                speed_y = ((Y[particle.counter] - Y[particle.counter - 10])/10)
            X = []
            Y = []
            particle.speed[0] = speed_x
            particle.speed[1] = speed_y
            particle.counter = -1



        # Makes ball bounce off walls
        ball_bounce_wall(particle, size, particle.speed)


        # Calculates accelerations due to various forces
        speed_change(particle, liquid, height, liquid_height, friction, particle.speed, gravity)


        # Temporary moving variable
        tmove = balls_dont_move_thru_walls(particle, size, particle.speed)


        particle.x += tmove[0]
        particle.y += tmove[1]


        particle.update_boundaries(particle.x, particle.y)
        particle.display(screen)

        gravity = gravity_init

        mouse_bool = []
        for counter in range(number_of_particles):
            mouse_bool.append(False)

        if selected_particle != None:
            mouse_bool[selected_particle] = True



    pygame.display.flip()
    clock.tick()