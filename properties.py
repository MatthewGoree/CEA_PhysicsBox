# All values at 25C
# Why are there so many kinds of syrup
import pygame

class liquid:
    def __init__(self, density, color, viscosity):
        self.density = density
        self.color = color
        self.viscosity = viscosity


# Estimated coefficients of restitution, can be changed
class ball_material:
    def __init__(self, density, color, CoR):
        self.density = density
        self.color = color
        self.CoR = CoR


def color_surface(surface, color):
    arr = pygame.surfarray.pixels3d(surface)
    arr[:,:,0] = color[0]
    arr[:,:,1] = color[1]
    arr[:,:,2] = color[2]


# Units converted using 100 pixels = 1 m
water = liquid(1000, (0, 255, 255), .089)
olive_oil = liquid(900, (204, 204, 0), 8.4)
syrup = liquid(1320, (204, 102, 0), 200000)
molasses = liquid(1600, (128, 43, 0), 750000)

silicon = ball_material(2328, (224, 224, 224), .95)
aluminum = ball_material(2720, (191, 191, 191), .8)
copper = ball_material(8940, (204, 102, 0), .3)
lead = ball_material(11340, (51, 51, 51), .2)
