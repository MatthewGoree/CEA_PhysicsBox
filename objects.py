import numpy as np
from properties import * 
def sphere_volume(radius):
    return (4.0 / 3.0) * np.pi * radius**3

class MassObject:
    def __init__(self, image_file, radius, material):
        self.image = pygame.transform.scale(pygame.image.load(image_file), (2 * radius, 2 * radius))
        self.radius = radius
        self.volume = sphere_volume(self.radius)
        self.rect = self.image.get_rect()
        self.mass = material.density * self.volume
        self.material = material
        #self.speed = initial_speed
        

def ball_bounce_wall(mass_object, size, speed):
    if mass_object.rect.left <= 0 or mass_object.rect.right >= size[0]:
        speed[0] = -mass_object.material.CoR * speed[0]
    if mass_object.rect.top <= 0 or mass_object.rect.bottom >= size[1]:
        speed[1] = -mass_object.material.CoR * speed[1]


def balls_dont_move_thru_walls(mass_object, size, speed):
    # Sets a temporary variable which can be altered w/out affecting speed
    temp_move = []
    temp_move.append(speed[0])
    temp_move.append(speed[1])
    # Checks that the distance being moved in one iteration is not greater than the distance from the wall
    if speed[0] < 0:
        if speed[0] < -mass_object.rect.left:
            temp_move[0] = -mass_object.rect.left
    else:
        x_dist_right = size[0] - mass_object.rect.right
        if speed[0] > x_dist_right:
            temp_move[0] = x_dist_right
    if speed[1] < 0:
        if speed[1] < -mass_object.rect.top:
            temp_move[1] = -mass_object.rect.top
    else:
        y_dist_bottom = size[1] - mass_object.rect.bottom
        if speed[1] > y_dist_bottom:
            temp_move[1] = y_dist_bottom
    return temp_move
