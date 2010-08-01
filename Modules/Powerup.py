"""
    Python Space Fighter Game - Powerup class
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

class Powerup:
    def __init__(self, pos, ptype="unknown",value=1):
        self.position = [pos[0], pos[1]]    # We're like a particle
        self.radius = 12                    # but we act a bit differently
        self.direction = random.Random().randint(0,100) / 50.0 * math.pi
        self.age = 0.0                      # it too has an age
        self.damage = 0                     # does no damage
        self.velocity = 2.0                 # Moves an acceptable pace
        self.type = ptype                   # Has a type
        self.value = value                  # and value assigned to it
    def update(self, multiplier=1.0):
        self.age += 0.5                     # Powerups last longer
        self.position[0] = self.position[0] + self.velocity * \
            math.cos(self.direction) * multiplier
        self.position[1] = self.position[1] + self.velocity * \
            math.sin(self.direction) * multiplier
        if self.position[0] < 0 - self.radius: # This is all basically the same
            self.position[0] = screenWidth + self.radius
        elif self.position[0] > screenWidth + self.radius:
            self.position[0] = 0 - self.radius
        if self.position[1] < 0 - self.radius:
            self.position[1] = screenHeight + self.radius
        elif self.position[1] > screenHeight + self.radius:
            self.position[1] = 0 - self.radius
    def distanceFrom(self,point):       # Distance from...
        return distanceBetween(self.position, point)
    def render(self):                   # Rendering
        pscreen.SpriteRender(self.position[0],self.position[1], \
            "powerup_" + self.type,0,0.4)
