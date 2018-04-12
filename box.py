import pygame
import math
import random
import numpy










'''Taken and adapted from http://www.petercollingridge.co.uk/pygame-physics-simulation/'''



(width,height) = (500,500)          #width and height of screen
background_color = (255,255,255)    #white
drag_air = 0.9995                   #aero drag
drag_water = 0.995                  #hydro drag
elasticity = 0.75                   #bounce factor
gravity = (math.pi, 0.00)          #pi is downward angle, 0.002 is estimated value of gravity in pygame


'''Function that compares the coordinates of a particle to the coordinates of the clicked mouse'''
def findParticle(particles, x, y):
    for p in particles:
        #if the distance between the mouse and the particle is less than the
        #particle's radius, then the mouse is selecting it
        if math.hypot(p.x-x, p.y-y) <= p.radius:
            return p
    return None



'''Function to calculate the x velocity and y velocity of a particle'''
'''Useful for factors that scale just one direction of an object, such as gravity'''
def addVectors(angle1, length1, angle2, length2):
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2

    angle = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)


'''Function to if two particles have collided, and to transfer energy between each'''
def collide(p1, p2):
    dx = p1.x - p2.x    #x distance of 2 particles
    dy = p1.y - p2.y    #y distance of 2 particles

    dist = math.hypot(dx, dy)   #distance between 2 particles

    #if the sum of radii between the two particles is greater than the distance between them, the particles have collided
    if dist < p1.radius + p2.radius:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2 * tangent - p1.angle
        angle2 = 2 * tangent - p2.angle
        speed1 = p2.speed * elasticity
        speed2 = p1.speed * elasticity

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


def magnetizism(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y

    dist = math.hypot(dx, dy)  # distance between 2 particles
    #tangent = math.atan2(dy, dx)   #idk how this is actually the tangent but it is
    angleTo = -math.atan((dx/dy))

    p1.angle = angleTo
    p1.speed = p2.magnetization




class Particle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = (0,0,0)
        self.thickness = 0
        self.speed = 1
        self.angle = 5
        self.angle *= (180/math.pi)
        self.drag = drag_air
        self.magnetization = 0


    def display(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, gravity[0], gravity[1])
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag



    '''Function to determine what material space the object is going through and adjust drag accordingly'''
    def spaceIn(self):
        if self.y > height - height/3:  #water is the bottom third of the screen
            self.drag = drag_water

        else:                           #air is everywhere else
            self.drag = drag_air

    def bounce(self):
        if self.x > width - self.radius:
            self.x = 2*(width - self.radius) - self.x
            self.angle = - self.angle

        elif self.x < self.radius:
            self.x = 2*self.radius - self.x
            self.angle = - self.angle

        if self.y > height - self.radius:
            self.y = 2*(height - self.radius) - self.y
            self.angle = math.pi - self.angle

        elif self.y < self.radius:
            self.y = 2*self.radius - self.y
            self.angle = math.pi - self.angle





screen = pygame.display.set_mode((width,height))
screen.fill(background_color)
pygame.draw.rect(screen, (0,0,255), (height/2,width/2, 200, 200), 10)       #body of water
pygame.display.set_caption('CEA Physics Box')

number_of_particles = 1
my_particles = []

for n in range(number_of_particles):
    radius = 40#random.randint(10, 20)
    x = random.randint(radius, width-radius)
    y = random.randint(radius, height-radius)

    particle = Particle(x, y, radius)
    particle.speed = 1#random.random()
    particle.angle = random.uniform(0, math.pi*2)

    my_particles.append(particle)

selected_particle = None



part2 = Particle(50, 50, 40)
part2.color = (100,255,100)
part2.magnetization = 2

my_particles.append(part2)



'''Infinite loop to keep the program open until the user exits'''
running = True
while running:
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
                selected_particle.color = (0,0,0)
            selected_particle = None




    if selected_particle:
        (mouseX, mouseY) = pygame.mouse.get_pos()
        dx = mouseX - selected_particle.x
        dy = mouseY - selected_particle.y
        selected_particle.angle = 0.5*math.pi + math.atan2(dy, dx)
        selected_particle.speed = math.hypot(dx, dy) * 0.1


    screen.fill(background_color)
    pygame.draw.rect(screen, (0, 0, 255), (0, height - height/3, width, height/3), 0)
    for i, particle in enumerate(my_particles):
        particle.move()
        particle.spaceIn()
        particle.bounce()
        for particle2 in my_particles[i+1:]:
            collide(particle, particle2)
            magnetizism(particle, particle2)
        particle.display()

    pygame.display.flip()