"""
    Python Space Fighter Game - Particle classes
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
import pscreen, pygame, math
from Helper import *

class Particle:
    """Something you can shoot"""
    def __init__(self, pos, direc, own, velo, initage=0.0):
        self.velocity = 15                  # Magnitude of velocity
        self.velinit = [velo[0], velo[1]]   # Intial velocity (from our source)
        self.position = [pos[0], pos[1]]    # Position vector
        self.direction = direc              # Direction
        self.age = initage                  # Initial age
        self.owner = own                    # Owner (what shot us?)
        self.damage = 0.05                  # Damage we cause
        self.radius = 5                     # Collision radius
    def hitfinal(self):
        self.age = 200                      # Kill us
        self.damage = 0.0                   # Don't do more damage
    def update(self):
        self.position[0] += self.velinit[0] # Update position by init velocity
        self.position[1] += self.velinit[1] # ...
        self.position[0] += self.velocity * math.cos(self.direction) # etc.
        self.position[1] += self.velocity * math.sin(self.direction) # ...
        self.age = self.age + 2.0                   # Get older
        if self.position[0] < 0 - self.radius:      # Looping
            self.position[0] = screenWidth + self.radius 
        elif self.position[0] > screenWidth + self.radius:
            self.position[0] = 0 - self.radius
        if self.position[1] < 0 - self.radius:
            self.position[1] = screenHeight + self.radius 
        elif self.position[1] > screenHeight + self.radius:
            self.position[1] = 0 - self.radius      # ...
    def render(self):
        # Render our sprite, which is by default #1
        pscreen.SpriteRender(self.position[0], self.position[1], 1, \
            -self.direction * 180 / math.pi - 90)
    def distanceFrom(self,point):
        # Just a quicky time saver for returning distance from something
        return distanceBetween(self.position, point)
class Missile(Particle):
    def __init__(self, pos, direc, own, velo, target):
        Particle.__init__(self, pos, direc, own, velo)  # We're a particle
        self.target = target                            # But we have a target
        self.damage = 0.25                              # Do more damage
        self.velocity = 5                               # And go a lot slower.
    def render(self):
        pscreen.SpriteRender(self.position[0], self.position[1], 2, \
            -self.direction * 180 / math.pi - 90)
    def update(self):
        self.velinit[0] = self.velinit[0] * 0.9 # Slowly overcome init velocity
        self.velinit[1] = self.velinit[1] * 0.9 # (without actually turning)
        # Find the direction towards our target
        newdir = directionTowardsFromLoop(self.target, \
            self.position, self.direction)
        if (self.direction < 0):    # Do some trig fixes
            self.direction = 2 * math.pi + self.direction
        # More trig to get a gradual rotation...
        if abs(2 * math.pi + self.direction - newdir) < abs(self.direction - \
            newdir):
            self.direction = self.direction + 2 * math.pi
        if abs(self.direction - (2 * math.pi + newdir)) < abs(self.direction - \
            newdir):
            newdir = newdir + 2 * math.pi
        self.direction = (self.direction * 10 + newdir) / 11    # Then turn us
        Particle.update(self)                  # Update position, looping, etc.
        self.age -= 1                          # But take a bit longer to die
        if self.distanceFrom(self.target) < 3: # And destroy us if hit
            self.age = 200      # (this is more for mouse-controlled missiles)
class Shield(Particle):
    def __init__(self, pos, direc, own, velo):
        Particle.__init__(self, pos, direc, own, velo)  # Shield is a particle
        self.velocity = 0.1                             # A very slow particle
        self.radius = 20                          # Which a much higher radius
        self.age = 95                             # That dies almost instantly
        self.damage = 0.3                         # And does a lot more damage
    def hitfinal(self):
        self.damage = 0.0 # Damage = 0, but don't kill us - fade out
    def render(self):
        pscreen.SpriteRender(self.position[0], self.position[1], 6, \
            -self.direction * 180 / math.pi - 90)
class SuperShield(Shield):
    def __init__(self, pos, direc, own, velo):
        Shield.__init__(self,pos,direc,own,velo)       # Same as with a shield,
        self.radius = 22                               # But bigger
        self.damage = 0.7                              # And more damaging
    def render(self):
        pscreen.SpriteRender(self.position[0], self.position[1], 20, \
             -self.direction * 180 / math.pi - 90)
class HyperShield(Shield):
    def __init__(self, pos, direc, own, velo):
        Shield.__init__(self,pos,direc,own,velo)        # Again, same deal
        self.radius = 40                                # But bigger
        self.damage = 0.8                               # and stronger
    def hitfinal(self):
        self.damage = self.damage * 0.9                 # Live on!
    def render(self):
        pscreen.SpriteRender(self.position[0], self.position[1], 21, \
            -self.direction * 180 / math.pi - 90)
class Mine(Particle):
    def __init__(self, pos, own):
        Particle.__init__(self, pos, (random.Random().randint(0,100) / \
            50.0 * math.pi), own, (0,0))
        self.velocity = 0.1     # Mines float in random direction, slowly
        self.age = -100         # Last longer
        self.damage = 0.4       # and do more damage
        self.radius = 10        # (and are a bit bigger)
    def explode(self, objects):
        for i in range(0,16):   # When a mine dies, it explodes awesomely
            objects.append(Particle(self.position, self.direction + i * \
                math.pi / 8, self.owner, (0,0), initage=80))
    def render(self):
        renderFrame = 9         # Mines also have an animation
        if self.age > -50:      # with four frames
            renderFrame = 10    # that acts as a countdown timer
        if self.age > 0:        # when it runs out
            renderFrame = 11    # the mine automatically explodes
        if self.age > 50:       # 4... 3... 2... 1...
            renderFrame = 12    # (boom)
        pscreen.SpriteRender(self.position[0], self.position[1], renderFrame, \
            -self.direction * 180 / math.pi - 90)
class Star():   # Note: The star is NOT a particle
    def __init__(self, pos, size):
        self.position = pos         # Stars just sit there
        self.size = size * 0.5      # And have random sizes
    def render(self):
        pscreen.SpriteRender(self.position[0],self.position[1],13,0,self.size)
class Explosion():
    def __init__(self, pos, size):
        self.position = pos         # Explosions stay where they are
        self.size = size            # Have certain sizes
        self.frame = 0.0            # And animate
    def update(self):
        self.frame += 0.2           # Update the current frame...
    def render(self):
        pscreen.SpriteRender(self.position[0],self.position[1],14 + \
            int(self.frame),0,self.size)
