# All values at 25C
# Why are there so many kinds of syrup

class liquid:
    def __init__(self, density, color, viscosity):
        self.density = density
        self.color = color
        self.viscosity = viscosity


# Estimated coefficients of restitution
class ball_material:
    def __init__(self, density, color, CoR):
        self.density = density
        self.color = color
        self.CoR = CoR


# Units converted using 100 pixels = 1 m
water = liquid(1000, (0, 255, 255), .089)
olive_oil = liquid(900, (204, 204, 1), 8.4)
syrup = liquid(1320, (204, 102, 0), 200000)
molasses = liquid(1600, (204, 102, 0), 750000)

silicon = ball_material(2328, (224, 224, 224), .95)
copper = ball_material(8940, (204, 102, 0), .8)
