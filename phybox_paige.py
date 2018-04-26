
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
material = copper
gravity_init = 2
gravity = gravity_init
i_count = 0
# Coefficient of friction on the floor
friction = 0.01
speed = [0,0]
tmove = speed

screen = pygame.display.set_mode(size)


number_of_particles = 1
my_particles = []

for n in range(number_of_particles):
    radius = 25#random.randint(20, 50)
    x = 50#random.randint(radius, width - radius)
    y = 50#random.randint(radius, height - radius)

    particle = MassObject(x, y, radius, material, speed)
    my_particles.append(particle)

selected_particle = None




def findParticle(particles, x, y):
    for p in particles:
        #if the distance between the mouse and the particle is less than the
        #particle's radius, then the mouse is selecting it
        if math.hypot(p.x-x, p.y-y) <= p.radius:
            #print "distance "
            #print math.hypot(p.x-x, p.y-y)
            return p
    return None

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



    if selected_particle:
        #gravity = 0
        i_count += 1
        (mouseX, mouseY) = pygame.mouse.get_pos()
        selected_particle.x = mouseX
        selected_particle.y = mouseY
        X.append(mouseX)
        Y.append(mouseY)
        gravity = 0
    else:
        if i_count > 0:
            speed_x = (X[i_count-1] - X[0])/i_count
            speed_y = (Y[i_count-1] - Y[0])/i_count
            X = []
            Y = []
            particle.speed[0] += speed_x
            particle.speed[1] += speed_y
            gravity = gravity_init
        i_count = 0


    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, liquid.color, (0, liquid_height, width, height))
    pygame.draw.line(screen, (0, 0, 0), (0, liquid_height), (width, liquid_height), 1)
    #pygame.draw.test_rectangle(screen, liquid.color, (0, 50, 50, 50))

    for i, particle in enumerate(my_particles):

        # Makes ball bounce off walls
        ball_bounce_wall(particle, size, particle.speed)
        #speed = particle.speed
        # Calculates accelerations due to various forces

        speed_change(particle, liquid, height, liquid_height, friction, particle.speed, gravity)

        # Temporary moving variable

        tmove = balls_dont_move_thru_walls(particle, size, particle.speed)
        particle.x += tmove[0]
        particle.y += tmove[1]


        particle.update_boundaries(particle.x, particle.y)
        particle.display(screen)


    pygame.display.flip()
    clock.tick()