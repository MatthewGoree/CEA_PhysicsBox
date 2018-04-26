import math
import pygame
import numpy as np

from speed_and_acceleration import *
gravity = (math.pi, 0.001)


def sphere_volume(radius):
    return (4.0 / 3.0) * np.pi * radius**3


class MassObject:
    def __init__(self, x, y, radius, material, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.material = material
        self.thickness = 0
        self.color = material.color
        self.volume = sphere_volume(self.radius)
        self.mass = material.density * self.volume
        self.speed = speed
        self.angle = 0
        self.top = self.y - self.radius
        self.bottom = self.y + self.radius
        self.right = self.x + self.radius
        self.left = self.x - self.radius

    def update_boundaries(self, x, y):
        self.top = y - self.radius
        self.bottom = y + self.radius
        self.right = x + self.radius
        self.left = x - self.radius


    def display(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius, self.thickness)

    #def move(self):
     #   speed_change(self, liquid, height, liquid_height, friction, speed, gravity)

def ball_bounce_wall(mass_object, size, speed):
    if mass_object.left <= 0 or mass_object.right >= size[0]:
        speed[0] = -mass_object.material.CoR * speed[0]
    if mass_object.top <= 0 or mass_object.bottom >= size[1]:
        speed[1] = -mass_object.material.CoR * speed[1]


def balls_dont_move_thru_walls(mass_object, size, speed):
    # Sets a temporary variable which can be altered w/out affecting speed
    temp_move = []

    temp_move.append(speed[0])
    temp_move.append(speed[1])
    # Checks that the distance being moved in one iteration is not greater than the distance from the wall
    if speed[0] < 0:
        if speed[0] < -mass_object.left:
            temp_move[0] = -mass_object.left
    else:
        x_dist_right = size[0] - mass_object.right
        if speed[0] > x_dist_right:
            temp_move[0] = x_dist_right
    if speed[1] < 0:
        if speed[1] < -mass_object.top:
            temp_move[1] = -mass_object.top
    else:
        y_dist_bottom = size[1] - mass_object.bottom
        if speed[1] > y_dist_bottom:
            temp_move[1] = y_dist_bottom

    #print temp_move

    return temp_move