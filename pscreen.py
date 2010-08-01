#pscreen2 - a simple module for making 2d graphics and
#           performing simple keyboard and mouse input.
#
#  By Paul W. Yost for the ETGG102 class at Shawnee State University.
#
#  This module requires the pygame module to be installed.
#  pygame is available at www.pygame.org.

import pygame

#########  Sprite Functions

def SpriteLoad(Filename,spriteSlot,size=None):
   """SpriteLoad(Filename,spriteSlot,size=None)"""
   if size==None :
       sprite[spriteSlot]=pygame.image.load(sprite_dir + Filename)
   else:
       if len(size)==2:
           sprite[spriteSlot]=pygame.transform.scale(pygame.image.load(sprite_dir + Filename),size)

def SpriteRender(centerx, centery, spriteSlot, rotationAngle=0, scaleFactor=1, flipH=False, flipV=False):
   """SpriteRender(centerx, centery, spriteSlot, rotationAngle=0, scaleFactor=1, flipH=False, flipV=False)"""
   if sprite[spriteSlot] != None:
       #newsurf=pygame.transform.rotate(sprite[spriteSlot],rotationAngle)
       newsurf=pygame.transform.flip(sprite[spriteSlot],flipH,flipV)
       newsurf2=pygame.transform.rotozoom(newsurf, rotationAngle, scaleFactor) 
       (x1,y1)=newsurf2.get_size()
       x=x1/2
       y=y1/2
       rectangle=screenbuffer.blit(newsurf2,(centerx-x,centery-y))
       return rectangle 
       #screenbuffer.blit(pygame.transform.rotate(pygame.transform.flip(self.frames[self.frame],self.flipH,self.flipV),self.angle),(float(self.col)*32,float(self.row)*32))

def SpriteDirectory(path):
    global sprite_dir
    sprite_dir = path


#########  Music/Sound Functions
def MusicLoad( filename ):
    """ MusicLoad( Filename ) - loads the background music file."""
    pygame.mixer.music.load( filename )

def MusicPlay():
    """MusicPlay() - plays the loaded background music file."""
    pygame.mixer.music.play(-1)

def MusicPause():
    """MusicPause() - pauses the background music."""
    pygame.mixer.music.pause()

def MusicUnPause():
    """MusicUnPause() - resumes the background music."""
    pygame.mixer.music.unpause()

def MusicFade(seconds):
    """MusicFade( seconds ) - fades out the background music over the specified number of seconds."""
    pygame.mixer.music.fadeout(seconds*1000)

def MusicSetVolume(volumePercent):
    """MusicSetVolume(Percent) - sets the music volume to a percentage 0-100."""
    pygame.mixer.music.set_volume(volumePercent/100.0)

def MusicGetVolume():
    """MusicGetVolume() - returns the music volume percentage."""
    return pygame.mixer.music.get_volume()*100
    
def MusicStop():
    """MusicStop() - Stops the background music."""
    pygame.mixer.music.stop()
    
def SoundLoad(filename, soundSlot):
    """SoundLoad(filename, soundSlot) - loads sound file data into one of the 256 sound slots."""
    global sound
    sound[soundSlot] = pygame.mixer.Sound(filename)

def SoundSetVolume(soundSlot, volumePercent=40):
    """SoundSetVolume(soundSlot,volumePercent=40) - sets the playback volume for the sound slot
    to the the specified volume(0-100)"""
    global sound
    sound[soundSlot].set_volume(volumePercent/100.0)

def SoundGetVolume(soundSlot):
    """MusicGetVolume() - returns the music volume percentage."""
    return sound[soundSlot].get_volume()*100

def SoundPlay(soundSlot):
    """SoundPlay(soundSlot) - plays a loaded sound slot(0-255)."""
    global sound
    sound[soundSlot].play()
    
def SoundStop():
    """SoundStop() - stops all playing sounds."""
    pygame.mixer.stop()
    pygame.mixer.music.stop()

#########  General Functions
def LoadScreen(title="PScreen Module",resolution=(800,600),fullscreen=False):
    """LoadScreen(resolution=(800,600),fullscreen=False) - loads the pscreen window"""
    global screenbuffer
    if fullscreen==True:
        screenbuffer=pygame.display.set_mode(resolution,pygame.SWSURFACE+pygame.FULLSCREEN,16)
    else:    
        screenbuffer=pygame.display.set_mode(resolution,pygame.HWSURFACE+pygame.HWACCEL+pygame.DOUBLEBUF+pygame.ASYNCBLIT,16)
    pygame.display.set_caption(title)
    pygame.display.set_icon(pygame.Surface((10,10)))

        
def UnloadScreen():
    """UnLoadScreen() - closes the pscreen window"""
    pygame.display.quit()

def UpdateScreen():
    """UpdateScreen() -  move the display buffer to the screen and display it."""
    pygame.display.flip()


############ key input functions
def KeyGetPressedList():
    """Returns a list of the pressed keys as a sequence of strings."""
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    result=[]
    for i in range(0,len(pressed)):
        if pressed[i]!=0:
            result.append(pygame.key.name(i))
    return result        

def KeyIsPressed(KeySymbol):
    """Return a 1 if the specified key is pressed 0 if it isn't"""
    if KeySymbol in KeyGetPressedList():
        return 1
    else:
        return 0
    
def KeyIsNotPressed(KeySymbol):
    """Return a 1 if the specified key is not pressed 0 if it is"""
    if KeySymbol not in KeyGetPressedList():
        return 1
    else:
        return 0


#####Mouse Functions
def MouseGetPosition():
    """MouseGetPosition() - returns the mouse position as and (x,y) pair."""
    (x,y)=pygame.mouse.get_pos()
    return (x,y)

def MouseGetButtons():
    """MouseGetButtons() - returns the button state as a three element boolean tuple (l,m,r)."""
    return pygame.mouse.get_pressed() 

def MouseGetButtonL():
    """MouseGetButtonL() - returns the state of the left mouse button. True when pressed , False when not pressed. """
    return pygame.mouse.get_pressed()[0] 

def MouseGetButtonM():
    """MouseGetButtonM() - returns the state of the middle mouse button. True when pressed , False when not pressed. """
    return pygame.mouse.get_pressed()[1] 

def MouseGetButtonR():
    """MouseGetButtonR() - returns the state of the right mouse button. True when pressed , False when not pressed. """
    return pygame.mouse.get_pressed()[2] 

def MouseGetX():
    """MouseGetX() - returns the mouse x-coordinate."""
    (x,y)=pygame.mouse.get_pos()
    return x

def MouseGetY():
    """MouseGetY() - returns the mouse y-coordinate."""    
    (x,y)=pygame.mouse.get_pos()
    return y

###### Font Functions
def FontSelect(fontName="Arial",fontSize=24,name="default"):
    """FontSelect(fontName="Arial",fontSize=24) - sets the current font and font size."""
    global fonts
    fonts[name] = pygame.font.SysFont(fontName,fontSize)

def FontWrite(x,y,string,color=(255,255,255),font="default"):
    """FontWrite(x,y,string,color=(255,255,255)) - writes the text to the screen using the current font. """
    screenbuffer.blit(fonts[font].render(string,True,color),(x,y))        

###### Drawing Functions

def PixelSet(x,y,color=(255,255,255)):
    """PixelSet(x,y,color=(255,255,255)) - turn on the pixel at the specified location. """
    screenbuffer.set_at((x,y),color)

def PixelGet(x,y):
    """PixelGet(x,y) - get and return the color of the pixel at the specified location. """
    return screenbuffer.get_at((x,y))

def Line(x1,y1,x2,y2,color=(255,255,255),width=1):
    """Line(x1,y1,x2,y2,color=(255,255,255),width=1) - draw a line between the two specified points. """
    pygame.draw.line(screenbuffer,color,(x1,y1),(x2,y2),width)

def Circle(x,y,radius,color=(255,255,255),width=1):
    """Circle(x,y,radius,color=(255,255,255),width=1) - draw a circle with the specified center and radius. """
    pygame.draw.circle(screenbuffer,color,(int(x),int(y)),radius,width)

def Ellipse(x,y,ellipse_width,ellipse_height,color=(255,255,255),linewidth=1):
    """Ellipse(x,y,height,width,color=(255,255,255),linewidth=1) - draw an ellipse """
    pygame.draw.ellipse(screenbuffer, color, (x,y,ellipse_width,ellipse_height), linewidth)

def Rectangle(x1,y1,x2,y2,color=(255,255,255),width=1):
    """Rectangle(x1,y1,x2,y2,color=(255,255,255),width=1) - draw a rectangle using the two points as the corners. """
    if x1<x2:
        x=x1
    else:
        x=x2
    if y1<y2:
        y=y1
    else:
        y=y2
    w=abs(x2-x1)
    h=abs(y2-y1)
    pygame.draw.rect(screenbuffer,color,(x,y,w+1,h+1),width)

def Triangle(x1,y1,x2,y2,x3,y3,color=(255,255,255),width=1):
    """Triangle(x1,y1,x2,y2,x3,y3,color=(255,255,255),width=1) - draw a triangle using the three points specified"""
    pygame.draw.polygon(screenbuffer, color, [(x1,y1),(x2,y2),(x3,y3)], width)



##############  Main initialization code

#setup the display
pygame.display.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
pygame.font.init()

#setup the variables for this class
sound = [None]*256
sprite = {}
sprite_dir = ""

background=None
screenbuffer=None

fonts = {}
fonts['default'] = pygame.font.SysFont("Arial",24)

        

    





