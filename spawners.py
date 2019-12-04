import pygame
import random
from weapons import *
import sys
pygame.mixer.pre_init(44100, -16, 2, 512)
#add the image path
sys.path.append("/resources/images")
#add the source
CRATE_SPRITE = "resources/images/Legendary_Crate.png"

class Spawner(object):
    """docstring for Crate."""
    def __init__(self, posX, posY, weapon=0):
        self.posX = posX
        self.posY = posY
        self.time_the_weapon_left = -3000 # ensure the crate's weapon can be picked up at the beginning
        #crate state
        if weapon == 0:
            temp = pygame.image.load(CRATE_SPRITE) # load the image
            self.image = pygame.transform.scale(temp, (round(temp.get_width()/1.25), round(temp.get_height()/1.25))).convert() # scale the image down
            self.imagebox = self.image.get_rect(x=posX, y=posY) # create a hitbox for the crate
            self.weapon = 0 # no weapon
            self.state = "crate"
            #self.health = 50
        #weapon state
        else:
            # if a specific weapon is specified, create the weapon
            self.state = "weapon"
            if weapon == "SMG":
                self.weapon = SMG("left", posX, posY)
                self.image = self.weapon.image
                self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
            elif weapon == "AK":
                self.weapon = AK("left", posX, posY)
                self.image = self.weapon.image
                self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
            elif weapon == "Pistol":
                self.weapon = Pistol("left", posX, posY)
                self.image = self.weapon.image
                self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
            elif weapon == "AWM":
                self.weapon = AWM("left", posX, posY)
                self.image = self.weapon.image
                self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
            elif weapon == "Shotgun":
                self.weapon = Shotgun("left", posX, posY)
                self.image = self.weapon.image
                self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)

    def spawn_weapon(self):
        #spawn a random weapon
        self.state = "weapon"
        temp = random.randint(0, 100) # generate a random number

        weapons = ["AK", "Pistol", "SMG", "Shotgun", "AWM"]
        if temp < 10:
            weapon = weapons[4]
        elif temp < 00:#shotgun not yet implemented
            weapon = weapons[3]
        elif temp < 20:
            weapon = weapons[0]
        elif temp < 45:
            weapon = weapons[2]
        else:
            weapon = weapons[1]
        # create the weapon
        if weapon == "SMG":
            self.weapon = SMG("left", self.posX, self.posY)
            #self.image = self.weapon.image
            #self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
        elif weapon == "AK":
            self.weapon = AK("left", self.posX, self.posY)
            #self.image = self.weapon.image
            #self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
        elif weapon == "Pistol":
            self.weapon = Pistol("left", self.posX, self.posY)
            #self.image = self.weapon.image
            #self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
        elif weapon == "AWM":
            self.weapon = AWM("left", self.posX, self.posY)
            #self.image = self.weapon.image
            #self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
        elif weapon == "Shotgun":
            self.weapon = Shotgun("left", self.posX, self.posY)
            #self.image = self.weapon.image
            #self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)

    def respawn(self):
        # if conditions are met, change back to the crate state, enable respawn.
        if pygame.time.get_ticks() - self.time_the_weapon_left >= 3000:
            self.state = "crate"
            self.image
            return True
        else:
            return False
