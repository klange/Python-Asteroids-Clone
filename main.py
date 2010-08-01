#!/usr/bin/python
"""
    Python Space Fighter Game
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
import pscreen, time, math, random, pygame, string, sys, random
from Modules import Spaceship, Particle, Powerup, Target
from Modules.Helper import *
import threading
objects = []        # All objects in the environment (player, rocks, etc.)
targetlist = []     # List of targets for multiple-target missiles (a powerup)
stars = []          # Stars in the background
explosions = []     # Explosions to render
powerupList = []    # Powerups the system can choose from (with repeats)
powerupVals = []    # Values for those powerups

player = Spaceship.Spaceship((screenWidth / 2,screenHeight / 2),0.3)
objects.append(player)  # But still remains in the objects list for rendering

deathCount = 0          # Player death count
killCount = 0           # Player kill count
newtargetcount = 4      # Kills required to spawn a new rock.
game_is_paused = False  # Is the game paused?
paused_time = 30        # Pause button time out
mouse = [0.0,0.0]       # We track the mouse location with this

# Start up our pygame instance with pscreen
pscreen.LoadScreen(title="SHS Computer Club Spaceship Game",\
    resolution=(screenWidth,screenHeight)) # Full screen will default, btw.
# Load up our sprites
pscreen.SpriteDirectory("Sprites/")
pscreen.SpriteLoad("Spaceship.png",0)               # Player
pscreen.SpriteLoad("Particle.png",1)                # Regular projectiles
pscreen.SpriteLoad("Missile.png", 2)                # Missiles
pscreen.SpriteLoad("AsteroidBig.png",3)             # Large asteroid
pscreen.SpriteLoad("AsteroidMed.png",4)             # Medium asteroid
pscreen.SpriteLoad("AsteroidSmall.png",5)           # Small asteroid
pscreen.SpriteLoad("Shield.png",6)                  # Standard shielding (blue)
pscreen.SpriteLoad("TargettingTriangle.png",7)      # Red targetting triangle
pscreen.SpriteLoad("TargettingTriangleBlue.png",8)  # Blue targetting triangle
pscreen.SpriteLoad("MineFull.png",9)                # Mine with full counter
pscreen.SpriteLoad("MineThree.png",10)              # Mine w/ 3/4 counter
pscreen.SpriteLoad("MineHalf.png",11)               # Mine w/ 1/2 counter
pscreen.SpriteLoad("MineQuarter.png",12)            # Mine w/ 1/4 counter
pscreen.SpriteLoad("Star.png",13)                   # Background star
pscreen.SpriteLoad("Explosion1.png",14)             # Explosion frame 1
pscreen.SpriteLoad("Explosion2.png",15)             #           frame 2
pscreen.SpriteLoad("Explosion3.png",16)             #           frame 3
pscreen.SpriteLoad("Explosion4.png",17)             #           frame 4
pscreen.SpriteLoad("Explosion5.png",18)             #           frame 5
pscreen.SpriteLoad("Explosion6.png",19)             #           frame 6
pscreen.SpriteLoad("SuperShield.png",20)            # Shield - super (white)
pscreen.SpriteLoad("HyperShield.png",21)            # Shield - hyper (red)
# Powerup sprites make use of modified sprite library class
pscreen.SpriteLoad("PowerupUnknown.png","powerup_unknown")          # Unknown 
pscreen.SpriteLoad("PowerupTriple.png","powerup_triple")            # Triple
pscreen.SpriteLoad("PowerupMissile.png","powerup_missile")          # Missile
pscreen.SpriteLoad("PowerupMissileQuad.png","powerup_missilequad")  # Missile x4
pscreen.SpriteLoad("PowerupMissileTracking.png","powerup_tracking") # Tracking 
pscreen.SpriteLoad("PowerupShield.png","powerup_shield")            # S Standard
pscreen.SpriteLoad("PowerupSuperShield.png","powerup_supershield")  # S super
pscreen.SpriteLoad("PowerupHyperShield.png","powerup_hypershield")  # S hyper
pscreen.SpriteLoad("PowerupMine.png","powerup_mine")                # Mine

# Load fonts into modified font library class for pscreen
pscreen.FontSelect(fontName="Monospace",fontSize=15,name="powerups") # Powerup
pscreen.FontSelect(fontName="sans",fontSize=32,name="score")   # Score font
pscreen.FontSelect(fontName="sans",fontSize=18,name="hud")     # HUD text font

# Save some calls to random.Random() by making a Random() object
rand = random.Random()
player.ghost()  # Ghost the player so they don't die immediately
# Add some stars to the background
for i in range(0,100):
    stars.append(Particle.Star([rand.randint(0,screenWidth), \
        rand.randint(0,screenHeight)],rand.randint(0,3)))
# Add some asteroids
for i in range(0,15):
    position = (rand.randint(0,screenWidth),rand.randint(0,screenHeight))
    objects.append(Target.Target(position, 20)) # Add a rock at a random spot

# Set up the powerupList and powerupVals with appropriate distributions of
# the various powerups in our arsenal.
for i in range(0,5):                    # 5 Triple shot
    powerupList.append("triple")
    powerupVals.append(100)
for i in range(0,4):                    # 4 Missiles
    powerupList.append("missile")
    powerupVals.append(20)
for i in range(0,3):                    # 3 Missile Quads
    powerupList.append("missilequad")
    powerupVals.append(5)
for i in range(0,3):                    # 3 Mines
    powerupList.append("mine")
    powerupVals.append(5)
for i in range(0,3):                    # 3 Standard shields
    powerupList.append("shield")
    powerupVals.append(100)
for i in range(0,2):                    # 2 Tracking missiles
    powerupList.append("tracking")
    powerupVals.append(2)
for i in range(0,2):                    # 2 Super shields
    powerupList.append("supershield")
    powerupVals.append(200)
for i in range(0,1):                    # 1 Hyper shield
    powerupList.append("hypershield")
    powerupVals.append(200)

# Function called in game loop to update positions, etc.
def updateAll():
    global newtargetcount, killCount
    for obj in objects:
        obj.update()
        if obj.age > 100:   # If age > 0, this object is in some way dead.
            if isinstance(obj, Target.Target):
                # Dead targets explode, and if not "small", split it
                player.score += obj.value   # Add to score
                explosions.append( \
                    Particle.Explosion(obj.position,obj.radius / 20)) # boom
                killCount += 1              # Track small kills
                if killCount > 5:           # After five kills, spawn a powerup
                    killCount = 0           # (And reset the count)
                    powerup = rand.randint(0,len(powerupList) - 1) # Select
                    powerupLoc = [rand.randint(0,screenWidth), \
                        rand.randint(0,screenHeight)]  # And pick a spot for it
                    objects.append(Powerup.Powerup(powerupLoc, \
                        powerupList[powerup],powerupVals[powerup]))
                if obj.value > 5: # Not small? Add two.
                    targetLoc = (obj.position[0] + rand.randint(-5,5), \
                        obj.position[1] + rand.randint(-5,5))
                    objects.append(Target.Target(targetLoc, \
                        obj.value * 0.5, obj.direction - 0.2, obj.velocity))
                    targetLoc = (obj.position[0] + rand.randint(-5,5), \
                        obj.position[1] + rand.randint(-5,5))
                    objects.append(Target.Target(targetLoc, \
                        obj.value * 0.5, obj.direction + 0.2, obj.velocity))
                else:       # Else, decrement the count to add a new big rock
                    newtargetcount -= 1
                    if newtargetcount <= 0: # Need a new big rock
                        position = (rand.randint(0,screenWidth), \
                            rand.randint(0,screenHeight))    # Pick a spot
                        objects.append(Target.Target(position, 20)) # and add it
                        newtargetcount = 4               # reset the countdown
            if isinstance(obj, Particle.Mine):
                obj.explode(objects)    # Mines explode on impact
            objects.remove(obj)         # Regardless, it's removed.
            if obj in targetlist:       # And if they were targeted, they are
                targetlist.remove(obj)  # removed from the target list
    for expl in explosions:         # Explosions have their frame counts updated
        expl.update()
        if expl.frame > 5.4:        # And expired explosions
            explosions.remove(expl) # are removed from the scene
# Render everything
def renderAll():
    for star in stars:      # Stars
        star.render()
    for obj in objects:     # Objects (Player, rocks, projectiles, powerups)
        obj.render()
    for expl in explosions: # Explosions
        expl.render()
# Detect collision between objects
def collisionAll():
    global deathCount
    for obj in objects:
        if isinstance(obj, Target.Target):
            for obj2 in objects: 
                if isinstance(obj2, Particle.Particle):
                    # Rock hits particle (projectile, missile, shield)
                    if obj2.distanceFrom(obj.position) < obj.radius + \
                        obj2.radius:
                        if not isinstance(obj2,Particle.Shield):
                            # Don't show an explosion where the shield is
                            explosions.append(\
                                Particle.Explosion(obj2.position,0.5))
                        obj.hit(obj2.damage)    # Damage the rock
                        obj2.hitfinal()         # Kill the projectile
                if isinstance(obj2,Spaceship.Spaceship):
                    # Any hit to the player = instant death
                    if obj2.distanceFrom(obj.position) < obj.radius + \
                        obj2.radius:
                        if not obj2.ghosted > 0:        # Can't get hit if ghost
                            explosions.append(\
                                Particle.Explosion(obj2.position,1.0))
                            obj.hit(0.5)                # Damage the rock
                            obj2.ghost()                # start ghosting
                            obj2.velocity = [0,0]       # Reset our vel/pos
                            obj2.position = [screenWidth / 2,screenHeight / 2]
                            obj2.score -= 30            # and lose points
                            deathCount += 1             # increment death count
        if isinstance(obj, Powerup.Powerup):
            if player.distanceFrom(obj.position) < obj.radius + player.radius:
                # Player hits powerup
                obj.age = 100                           # Kill the powerup
                player.addPowerup(obj.type, obj.value)  # give the player the 
                objects.remove(obj)                     # powerup and remove it
            else:
                for obj2 in objects:
                    if isinstance(obj2, Particle.Particle):
                        if obj2.distanceFrom(obj.position) < obj.radius + \
                            obj2.radius:
                            # Player projectile hits powerup
                            obj.age = 100       # same deal as before
                            player.addPowerup(obj.type, obj.value)
                            objects.remove(obj)
                            obj2.hitfinal()     # but also remove the projectile
                            break               # and break the loop
# Draw targetting arrays for the multi-targetting system
def drawTargets():
    for obj in targetlist:
        pscreen.SpriteRender(obj.position[0], obj.position[1], 8, 0)
# Find the closest object to a point
# (that isn't the player, a projectile, or a powerup)
def findClosest(point):
    obj = objects[0]
    distance = distanceBetween(obj.position, point)
    for obj2 in objects:
        newdist = distanceBetween(obj2.position, point)
        if newdist < distance and not obj2 is player:
            if not isinstance(obj2, Particle.Particle) and \
                not isinstance(obj2, Powerup.Powerup):
                distance = newdist
                obj = obj2
        elif obj is player or isinstance(obj, Particle.Particle) or \
            isinstance(obj, Powerup.Powerup):
            distance = newdist
            obj = obj2
    return obj
# Find the object at this point (not really used)
def objectAt(point):
    for obj in objects:
        if obj.position == point:
            return obj
    return None
# Render the powerup HUD elements
def renderPowerups():
    x = 0   #      We want a specific order for the powerups we display
    for powerup in ['triple','missile','missilequad','tracking', \
        'mine','shield','supershield','hypershield']:
        if player.hasPowerup(powerup):
            pscreen.SpriteRender(200 + x * 52,screenHeight - 30, \
                "powerup_" + powerup) # sprite
            pscreen.FontWrite(176 + x * 52,screenHeight - 68, \
                str(player.numPowerup(powerup)).rjust(5,"0"), \
                color=(114,159,207),font="powerups")
            x += 1
framecount = 0    # Frame count (increments by 1)
tickcount = 0.0     # Time count (increments by 0.03)
fps = 0.0           # Frames per second count
endgame = False     # keeps the rendering thread in line
# Render everything in a separate thread.
class RenderThread ( threading.Thread ):
    def run ( self ):
        global game_is_paused, framecount, fps, endgame
        while not endgame:
            clearScreen()
            renderAll()
            drawTargets()
            pscreen.SpriteRender(closest.position[0], closest.position[1], 7, 0)
            if game_is_paused:
                pscreen.FontWrite(screenWidth / 2 - 60,screenHeight / 2 - 15, \
                    "Paused", color=(114,159,207), font="score")
            pscreen.FontWrite(screenWidth - 30,0,str(int(fps)).rjust(3,"0"), \
                color=(255,255,255), font="powerups")
            # Score:  Deaths: X | 00000 etc...
            # <-- 000000000 --> | XXXXX 
            pscreen.FontWrite(0,screenHeight - 60,"  Score:   Deaths: " + \
                str(int(deathCount)),color=(114,159,207),font="hud")
            pscreen.FontWrite(0,screenHeight - 40," " + \
                str(int(player.score)).rjust(9,"0"),color=(114,159,207),\
                font="score")
            # Targetting point, replace this with a sprite
            pscreen.Circle(mouse[0],mouse[1], 5, width=0)
            renderPowerups()        # Render the powerup HUD elements
            pscreen.UpdateScreen()
            framecount += 1
closest = Target.Target((-100,-100),1)
RenderThread().start()
# Game and Pause loop
while pscreen.KeyIsNotPressed("escape"):
    time.sleep(0.03)
    mouse[0] = pscreen.MouseGetX()                  # Dynamic Mouse X
    mouse[1] = pscreen.MouseGetY()                  # Dynamic Mouse Y
    mousestatic = (mouse[0],mouse[1])               # Static mouse coordinates
    closest = findClosest(mousestatic)              # Closest to mouse
    closestToPlayer = findClosest(player.position)  # Closest to player
    if not game_is_paused:  # If not paused, run the game loop
        player.face(mouse)  # Rotate towards the mouse (progressively)
        # ---- Movement controls
        # Accelerate
        if pygame.mouse.get_pressed()[0] or pscreen.KeyIsPressed("w"):
            player.accelerate(0.2)      # Adjust as necessary (speed powerups?)
        # Brake
        if pygame.mouse.get_pressed()[2] or pscreen.KeyIsPressed("s"):
            player.velocity[0] *= 0.9   # Again, adjust as necessary - ~1
            player.velocity[1] *= 0.9   # means slower braking
        # Left
        if pscreen.KeyIsPressed("a"):
            player.accelerate(0.1,-math.pi / 2) # This can also be adjusted
        # Right
        if pscreen.KeyIsPressed("d"):
            player.accelerate(0.1,math.pi / 2)  # But keep these equal
        # ---- Weapon controls
        # Basic weapon / triple shot / other standard powerups
        if pscreen.KeyIsPressed("space"):
            player.shoot(objects)
        # Mines
        if pscreen.KeyIsPressed("x"):
            player.dropMine(objects)
        # Missiles
        if pscreen.KeyIsPressed("z"):
            player.shootMissile(objects, closest.position)
        # Reset multiple targets
        if pscreen.KeyIsPressed("r"):
            targetlist = []
        # Add target to muliple targets list
        if pscreen.KeyIsPressed("t"):
            if not closest in targetlist:
                targetlist.append(closest)
        # Fire multiple targetting missiles (if we have them)
        if pscreen.KeyIsPressed("y"):
            player.shootMissileMultiple(objects,targetlist)
        # Automatic shielding
        if player.distanceFrom(closestToPlayer.position) < 40 + \
            closestToPlayer.radius:
            player.shield(objects,closestToPlayer)
        # Pause the game
        if pscreen.KeyIsPressed("p"):
            if paused_time > 10:
                game_is_paused = True
                paused_time = 0
        updateAll()     # Run .update() on all objects
        collisionAll()  # Process collision for all objects
    paused_time += 1    # Pause button timeout;
    if game_is_paused:  # Paused loop
        if pscreen.KeyIsPressed("p"):   # unpause
            if paused_time > 10:
                game_is_paused = 0
                paused_time = 0
    # Just in case, balance scores here immediately before we try to print them
    if player.score < 0: # this player's score can not go below 0
        player.score = 0
    tickcount += 0.03
    fps = framecount / tickcount
endgame = True
pscreen.UnloadScreen()
