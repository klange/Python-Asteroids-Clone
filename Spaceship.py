"""
    Python Space Fighter Game - Spaceship class
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
import Particle
from Helper import *

class Spaceship:
    """ The Spaceship class defines an object that can move annd be
        rendered and much more """
    def __init__(self, pos, direc):
        self.velocity = [0.0,0.0]           # Velocity
        self.position = [pos[0], pos[1]]    # Position
        self.direction = direc              # Direction
        self.age = 0                        # (not actually used here)
        self.triggerlock = 100              # Trigger lock
        self.missilelock = 100              # Missile trigger lock
        self.shieldlock = 100               # Shield "lock"
        self.minelock = 100                 # Mine trigger lock
        self.score = 0                      # Score
        self.radius = 5                     # Radius
        self.powerups = {}                  # Powerup dictionary
        self.ghosted = 0                    # Ghost timeout
    def render(self):
        if self.ghosted > 0:
            if int(self.ghosted) % 2 == 1:
                pscreen.SpriteRender(self.position[0], self.position[1], 0, \
                    -self.direction * 180 / math.pi - 90)
        else:
            pscreen.SpriteRender(self.position[0], self.position[1], 0, \
                -self.direction * 180 / math.pi - 90)
    def update(self):
        self.ghosted -= 0.2                     # Tick the ghost timer
        self.position[0] += self.velocity[0]    # Update position by velocity
        self.position[1] += self.velocity[1]    # ...
        self.velocity[0] *= 0.9999              # Slow us down a tiny bit
        self.velocity[1] *= 0.9999              # (not much, though)
        if self.position[0] < 0:                # Screen looping
            self.position[0] = screenWidth      # ...
        if self.position[0] > screenWidth:
            self.position[0] = 0
        if self.position[1] < 0:
            self.position[1] = screenHeight
        if self.position[1] > screenHeight:
            self.position[1] = 0
        if self.direction > 2 * math.pi:        # Direction fixing
            self.direction = self.direction - 2 * math.pi 
        elif self.direction < 0:
            self.direction = 2 * math.pi + self.direction
        self.triggerlock += 1                   # Tick trigger lock timer
        self.missilelock += 1                   # missile lock
        self.shieldlock += 1                    # shield "lock"
        self.minelock += 1                      # mine lock
    def accelerate(self, amount, angle=0):
        """ Accelerate forward, or at a given angle """
        if math.sqrt(self.velocity[1] ** 2 + self.velocity[0] ** 2) < 10:
            self.velocity[0] = self.velocity[0] + amount * \
                math.cos(self.direction + angle)
            self.velocity[1] = self.velocity[1] + amount * \
                math.sin(self.direction + angle)
    def face(self, point=[0.0,0.0]):
        """ Turn to face the given point (gradually) """
        newdir = self.directionTowards(point)
        if (self.direction < 0):
            self.direction = 2 * math.pi + self.direction
        if abs(2 * math.pi + self.direction - newdir) < \
            abs(self.direction - newdir):
            self.direction = self.direction + 2 * math.pi
        if abs(self.direction - (2 * math.pi + newdir)) < \
            abs(self.direction - newdir):
            newdir = newdir + 2 * math.pi
        self.direction = (self.direction * 4 + newdir) / 5
    def distanceFrom(self,point):
        """ Quick helper to give distance from the ship to a point """
        return distanceBetween(self.position, point)
    def directionTowards(self,point):
        return directionTowardsFrom(point, self.position)
    def addPowerup(self, ptype, value):
        """ Append a powerup to our list with the given value """
        if not self.powerups.has_key(ptype):
            self.powerups[ptype] = value        # If we don't have it, add it.
        else:
            self.powerups[ptype] += value       # If we do, add to it.
    def usePowerup(self, ptype):
        if not self.powerups.has_key(ptype):
            return False    # If we don't have it, we can't use it
        elif self.powerups[ptype] == 0:
            return False    # Again, if we don't have it...
        else:
            self.powerups[ptype] -= 1
            return True     # If we do, take some - we can do this.
    def hasPowerup(self, ptype):
        if not self.powerups.has_key(ptype):
            return False    # We've never even seen this powerup
        elif self.powerups[ptype] == 0:
            return False    # We don't have any of this powerup
        else:
            return True     # We have this powerup!
    def numPowerup(self, ptype):
        if self.hasPowerup(ptype):
            return self.powerups[ptype] # We have this many
        else:
            return 0    # We don't have any of this.
    def ghost(self):
        self.ghosted = 30.0     # Ghost us so we can't get hit by anything    
    # Begin weapon definitions
    def shoot(self, objects):   # Primary
        if (self.triggerlock > 3):
            if self.usePowerup("triple"):
                objects.append(Particle.Particle(self.position, \
                    self.direction, self, self.velocity))
                objects.append(Particle.Particle(self.position, \
                    self.direction + math.pi / 8, self, self.velocity))
                objects.append(Particle.Particle(self.position, \
                    self.direction - math.pi / 8, self, self.velocity))
                self.triggerlock = 0
            else:
                objects.append(Particle.Particle(self.position, \
                    self.direction, self, self.velocity))
                self.triggerlock = 0
    def shootMissile(self, objects, target): # Missile
        if (self.missilelock > 30):
            if self.usePowerup("missilequad"):
                objects.append(Particle.Missile(self.position, \
                    self.direction + math.pi / 4, self, self.velocity, target))
                objects.append(Particle.Missile(self.position, \
                    self.direction - math.pi / 4, self, self.velocity, target))
                objects.append(Particle.Missile(self.position, \
                    self.direction - 3 * math.pi / 4, self, \
                    self.velocity, target))
                objects.append(Particle.Missile(self.position, \
                    self.direction + 3 * math.pi / 4, self, \
                    self.velocity, target))
                self.missilelock = 0
            elif self.usePowerup("missile"):
                objects.append(Particle.Missile(self.position, \
                    self.direction, self, self.velocity, target))
                self.missilelock = 0
    def shootMissileMultiple(self, objects, targets):   # Targetting
        if (self.missilelock > 30):
            if self.usePowerup("tracking"):
                for tar in targets:
                    objects.append(Particle.Missile(self.position, \
                        self.direction, self, self.velocity, tar.position))
                self.missilelock = 0
    def shield(self, objects, closest): # Shield
        if (self.shieldlock > 1):
            if self.usePowerup("hypershield"):
                for i in range(0,4):
                    newDir = self.directionTowards(closest.position)
                    objects.append(Particle.HyperShield(self.position, \
                        newDir, self, self.velocity))
                self.shieldlock = 2
            elif self.usePowerup("supershield"):
                objects.append(Particle.SuperShield(self.position, \
                    self.directionTowards(closest.position), \
                        self, self.velocity))
                self.shieldlock = 1
            elif self.usePowerup("shield"):
                objects.append(Particle.Shield(self.position, \
                    self.directionTowards(closest.position), \
                        self, self.velocity))
                self.shieldlock = 0
    def dropMine(self, objects):    # Mine
        if (self.minelock > 10):
            if self.usePowerup("mine"):
                objects.append(Particle.Mine(self.position, self))
                self.minelock = 0
