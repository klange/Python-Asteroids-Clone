"""
    Python Space Fighter Game - Target class
    Copyright 2008-2010 Kevin Lange <kevin.lange@phpwnage.com>
    Written for the Strongsville High School Computer Club
    
    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
"""
import pscreen, pygame, math, random
from Helper import *

class Target:
    def __init__(self, pos, value, direction=-1000, velocity=-1):
        self.position = [pos[0], pos[1]]    # Initial position
        self.value = value                  # Value when destroyed
        self.radius = 24 * value / 20.0     # Size
        if direction == -1000:              # If direction=-1000, make random
            direction = random.Random().randint(0,100) / 50.0 * math.pi
        self.direction = direction          # Finalized direction
        self.age = 0.0                      # Age (only used when destroyed)
        self.damage = 0                     # Damage
        if velocity == -1:                  # Initial velocity is random
            self.velocity = random.Random().randint(1,4)
        else:                               # Initial velocity is specified
            self.velocity = velocity
        # Render direction is random
        self.directionRender = random.Random().randint(0,100) / 50.0 * math.pi
        # Rotation speed is random, within a range
        self.rotateSpeed = (random.Random().randint(0,1) * 2 - 1) * 0.05
    def hit(self, damage):
        # Called when we've been hit by something
        self.damage += damage * 40 / self.radius    # Bigger = less damage
        if self.damage >= 1.0:                      # If damage > 1, we're dead
            self.age = 1000                         # Set age > 100 - dead
    def update(self, multi=1.0):
        self.position[0] += self.velocity * math.cos(self.direction) * multi
        self.position[1] += self.velocity * math.sin(self.direction) * multi
        self.directionRender += self.rotateSpeed    # Spin
        if self.position[0] < 0 - self.radius:      # Screen wrap
            self.position[0] = screenWidth + self.radius
        elif self.position[0] > screenWidth + self.radius:
            self.position[0] = 0 - self.radius      # ...
        if self.position[1] < 0 - self.radius:      # ...
            self.position[1] = screenHeight + self.radius
        elif self.position[1] > screenHeight + self.radius:
            self.position[1] = 0 - self.radius      # ...
    def distanceFrom(self,point):
        return distanceBetween(self.position, point)
    def directionTowards(self,point):
        return directionTowardsFrom(point, self.position)
    def render(self):
        if (self.radius <= 6):      # Select the correct sprite to render
            slot = 5
        elif (self.radius > 6 and self.radius < 20):
            slot = 4
        elif (self.radius >= 20):
            slot = 3
        renDir = -self.directionRender * 180 / math.pi - 90
        pscreen.SpriteRender(self.position[0],self.position[1], slot, renDir)
