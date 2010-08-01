"""
    Python Space Fighter Game - Helper class
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
import math, random
import pygame, pscreen
screenWidth = 1280
screenHeight = 800
def clearScreen():
    """Clears the screen to black"""
    pygame.draw.rect(pscreen.screenbuffer,(0,0,0), \
        (0,0,screenWidth,screenHeight),0)
def directionTowardsFromLoop(point,fromPoint,direction):
    """Returns the direction from one point to a another
       respecting scren loops"""
    possible = directionTowardsFrom(point,fromPoint)
    if abs(screenWidth + point[0] - fromPoint[0]) < \
        abs(fromPoint[0] - point[0]):
        point = (screenWidth + point[0],point[1])
    elif abs(screenWidth - point[0]) + fromPoint[0] < \
        abs(fromPoint[0] - point[0]):
        point = (0 - point[0],point[1])
    if abs(screenHeight + point[1] - fromPoint[1]) < \
        abs(fromPoint[1] - point[1]):
        point = (point[0],screenHeight + point[1])
    elif abs(screenHeight - point[1]) + fromPoint[1] < \
        abs(fromPoint[1] - point[1]):
        point = (point[0],0 - point[1])
    probable = directionTowardsFrom(point,fromPoint)
    if (abs(probable - direction) < abs(possible - direction)):
        return probable
    else:
        return possible
def directionTowardsFrom(point,fromPoint):
    """Returns the direction from one point to another,
       without respecting screen loops"""
    if point[1] > fromPoint[1]:
        return math.asin((fromPoint[0] - point[0]) / math.sqrt((fromPoint[0] \
            - point[0])**2 + (fromPoint[1] - point[1])**2)) + math.pi / 2.0
    if point[1] < fromPoint[1]:
        return  math.pi - (math.asin((fromPoint[0] - point[0]) / \
            math.sqrt((fromPoint[0] - point[0])**2 + (fromPoint[1] - \
            point[1])**2))) + math.pi / 2.0
    if point[0] < fromPoint[0]:
        return math.pi
    return 0.0
def distanceBetween(pointa, pointb):
    """ Point-to-point distance"""
    return math.sqrt((pointa[0] - pointb[0])**2 + (pointa[1] - pointb[1])**2)
