import numpy as np
from properties import *
def sphere_volume(radius):
    print("sphere volume func, radius is ", radius)
    print(4.0 / 3.0 * np.pi * radius**3)
    return (4.0 / 3.0) * np.pi * radius**3

class MassObject:
    def __init__(self, image_file, radius, material):
        print("MATERIAL DENSITY IS, " , material.density)

        self.image = pygame.transform.scale(pygame.image.load(image_file), (2 * radius, 2 * radius))
        self.radius = radius
        self.volume = sphere_volume(self.radius)
        print("INITIAL VOLUME IS ", self.volume)
        self.rect = self.image.get_rect()
        self.mass = material.density * self.volume
        print("INITIAL MASS IS ", self.mass)
        self.material = copper
        #self.speed = initial_speed
