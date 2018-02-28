import numpy as np
from properties import *


def acc_buoyancy(mass_object, liquid, liquid_height, gravity):
    # Checks if mass is submerged or partially submerged in liquid
    if mass_object.rect.top < liquid_height:
        # Distance ball is underwater
        h = mass_object.rect.bottom - liquid_height
        if mass_object.radius >= h:
            vol_submerged = np.pi * h ** 2 / 3 * (3 * mass_object.radius - h)
        else:
            h_temp = 2 * mass_object.radius - h
            vol_submerged = mass_object.volume - np.pi * h_temp ** 2 / 3 * (3 * mass_object.radius - h_temp)
        buoy_submerged = vol_submerged * liquid.density * gravity
        acc_b = buoy_submerged / mass_object.mass
    else:
        acc_b = mass_object.volume * liquid.density * gravity / mass_object.mass
    return acc_b


def acc_drag(mass_object, liquid, liquid_height, speed):
    h = mass_object.rect.bottom - liquid_height

    # Checks if ball is submerged or partially submerged in the liquid
    if mass_object.rect.top < liquid_height:
        # Checks how far the ball is submerged
        if mass_object.radius >= h:
            # Central angle of partial circle
            theta = 2 * np.arccos((mass_object.radius - h) / mass_object.radius)
        else:
            # Distance from the radius to the liquid height
            h_temp = 2 * mass_object.radius - h
            # Central angle of partial circle
            theta = 2 * np.arccos(h_temp / mass_object.radius)
        # Ratio of area submerged to total area
        ratio = (mass_object.radius ** 2 / 2 * (theta - np.sin(theta))) / (np.pi * mass_object.radius ** 2)
    else:
        ratio = 1

    # Modified Stokes' Flow
    Fd = 6 * np.pi * liquid.viscosity * mass_object.radius * speed * ratio
    acc_d = Fd / mass_object.mass
    return acc_d


def acc_friction(mass_object, height, friction, speed, acc_b, gravity):
    if mass_object.rect.bottom == height:
        # Equations obtained from equilibrium eq of ball rolling on the floor underwater
        if speed > 0:
            acc_fric = friction * (gravity - acc_b)
        else:
            acc_fric = -friction * (gravity - acc_b)
    else:
        acc_fric = 0
    return acc_fric


def speed_change(mass_object, liquid, height, liquid_height, friction, speed, gravity):

    # Adds acceleration due to gravity
    if mass_object.rect.top >= 0:
        speed[1] = speed[1] + gravity

    # Buoyancy, friction, and drag if submerged
    if mass_object.rect.bottom > liquid_height:
        # Buoyancy
        acc_b = acc_buoyancy(mass_object, liquid, liquid_height, gravity)
        # Drag (vertical and horizontal)
        acc_drag_x = acc_drag(mass_object, liquid, liquid_height, speed[0])
        acc_drag_y = acc_drag(mass_object, liquid, liquid_height, speed[1])
        # Friction
        acc_fric = acc_friction(mass_object, height, friction, speed[0], acc_b, gravity)

        speed[0] = speed[0] - acc_drag_x - acc_fric
        speed[1] = speed[1] - acc_drag_y - abs(acc_b)
