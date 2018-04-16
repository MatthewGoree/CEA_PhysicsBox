
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

liquid = molasses
material = silicon
gravity = 5
# Coefficient of friction on the floor
friction = 0.01
speed = [6,0]
tmove = speed

screen = pygame.display.set_mode(size)


number_of_particles = 1
my_particles = []

for n in range(number_of_particles):
    radius = 25#random.randint(20, 50)
    x = 250#random.randint(radius, width - radius)
    y = 250#random.randint(radius, height - radius)

    particle = MassObject(x, y, radius, material)
    my_particles.append(particle)

    print "x: " + str(particle.x)
    print "y: " + str(particle.y)
    print "top: " + str(particle.top)
    print "bottom: " + str(particle.bottom)
    print "right: " + str(particle.right)
    print "left: " + str(particle.left)
    print "liquid height: " + str(liquid_height)

selected_particle = None




def findParticle(particles, x, y):
    for p in particles:
        #if the distance between the mouse and the particle is less than the
        #particle's radius, then the mouse is selecting it
        if math.hypot(p.x-x, p.y-y) <= p.radius:
            print "distance "
            print math.hypot(p.x-x, p.y-y)
            return p
    return None

running = True
while running:

    # Arbitrary framerate
    dt = clock.tick(30)



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            selected_particle = findParticle(my_particles, mouseX, mouseY)
            if selected_particle:
                selected_particle.color = (50,50,50)
        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_particle != None:
                selected_particle.color = (0,0,255)
            selected_particle = None




    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y


    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, liquid.color, (0, liquid_height, width, height))


    for i, particle in enumerate(my_particles):

        # Makes ball bounce off walls
        ball_bounce_wall(particle, size, speed)

        # Calculates accelerations due to various forces
        particle.speed = speed_change(particle, liquid, height, liquid_height, friction, speed, gravity)

        # Temporary moving variable
        tmove = balls_dont_move_thru_walls(particle, size, speed)

        #particle.x = tmove[0]
        #particle.y = tmove[1]

        particle.display(screen)


    pygame.display.flip()
    clock.tick()