import pygame
from abc import ABC, abstractmethod
from Bullet import *
import sys
import random
pygame.mixer.pre_init(44100, -16, 2, 512)
# Importing information from other python files and pre initializing the sounds.

sys.path.append("/resources/images")  # All images are found in the images folder inside of the resources folder
WEAPON_SPRITES = {
    "AK": {
        "left": "resources/images/AK47_Left.png",
        "right": "resources/images/AK47_Right.png"
    },
    "Pistol": {
        "left": "resources/images/Beretta92_Left.png",
        "right": "resources/images/Beretta92_Right.png"
    },
    "SMG": {
        "left": "resources/images/Tec9_Left.png",
        "right": "resources/images/Tec9_Right.png"
    },
    "AWM": {
        "left": "resources/images/AWM_Left.png",
        "right": "resources/images/AWM_Right.png"
    },
    "Shotgun": {
        "left": "resources/images/SPAS12_Left.png",
        "right": "resources/images/SPAS12_Right.png"
    }
}
# Loading the sprites into a dictionary

YELLOW = (255, 200, 110)
PURPLE = (85, 25, 180)
GREEN = (0, 255, 60)
BLUE = (90, 130, 255)
RED = (200, 0, 0)
COLOURS = [YELLOW, PURPLE, GREEN, BLUE, RED]
# Setting variables to colours for future use.
# All sounds come from https://www.youtube.com/watch?v=RZbeQjO7oW4
# The shotgun has not been enabled for this version of the game.
# Loading in the sounds and setting them to their own variables.

SOUNDSOURCES = {"AK": pygame.mixer.Sound("resources/audio/AK47_Sound.wav"),
                "Pistol": pygame.mixer.Sound("resources/audio/Beretta92_Sound.wav"),
                "SMG": pygame.mixer.Sound("resources/audio/Tec9_Sound.wav"),
                "AWM": pygame.mixer.Sound("resources/audio/AWM_Sound.wav"),
                "Shotgun": pygame.mixer.Sound("resources/audio/SPAS12_Sound.wav")}


class Weapon(ABC):  # Creating a class through which every weapon operates.
    def __init__(self, dir):
        self.direction = dir
        self.ammo_count = 0
        self.image = None
        self.imagebox = None
        self.speed = None
        self.damage = None
        self.weapon_type = None
        self.last_time_fired = -3000
        self.fire_rate = 1
        self.images = {"left":"",
                       "right":""}
        # Setting variables to be modified by each weapon individually later on.

    def change_direction(self):  # function used to change the direction of the sprite.
        if self.direction == "left":
            self.direction = "right"
            # If direction is already left when change direction command is activated, it changes direction to right.
        else:
            self.direction = "left"
            #  Does opposite of the 'if' statement.
        self.image = self.images[self.direction]  # Setting the new sprite to the image it takes from the dictionary.

    def fire(self, screen):  # Funtion used to fire a bullet.
        if pygame.time.get_ticks() - self.last_time_fired <= 1/self.fire_rate * 1000:
            return
        # Doesn't allow weapon to fire if it is before their fire rate.
        if self.ammo_count == 0:
            return
        # Doesn't allow the weapon to fire if it is out of ammo.
        self.last_time_fired = pygame.time.get_ticks()
        self.ammo_count -= 1
        # Sets the new last time fired, used for the firing rate, and reduces ammo count.
        pygame.mixer.Channel(0).play(SOUNDSOURCES[self.weapon_type])
        # Plays a sound based off of the weapon fired to its own individual channel.
        return self.display_action(screen)
        # Displays a bullet on the screen based off of the 'display_action' function for each weapon.

    def load_images(self):  # Funciton used to load the images into the game and scale their sizes
        temp_dict = {}
        for direction, image_name in WEAPON_SPRITES[self.weapon_type].items():
            temp = pygame.image.load(image_name)
            # Loading the weapon sprite and setting it to varible 'temp'
            temp_dict[direction] = pygame.transform.scale(temp, (round(temp.get_width()/1.25), round(temp.get_height()/1.25))).convert_alpha()
            # Adding the image to the dictionary and shrinking the image.
        return temp_dict

    @abstractmethod
    def display_action():
        pass

class AK(Weapon):  # Creating a class for the assault rifle.
    """docstring for AK."""
    def __init__(self, dir, posX, posY):
        super().__init__(dir)
        self.ammo_count = 20  # Amount of ammo in the magazine to begin with.
        self.speed = 20
        self.damage = 33  # Damage of each bullet.
        self.weapon_type = "AK"
        self.fire_rate = 8  # Amount of bullets that can be fired every second.
        self.images = self.load_images()
        self.image = self.images[dir]
        self.imagebox = self.image.get_rect(x=posX, y=posY)
        # Setting variables to modify Weapon(abc).

    def display_action(self, screen):  # Defining the display action function for the assault rifle.
        if self.direction == "left":
            return Bullet.createBullet(self.imagebox.x + 15, self.imagebox.y + 5, self.direction, "Rifle_bullet", self.damage)
        # Loading the left bullet sprite and adjusting it to appear at the barrel of the gun.
        else:
            return Bullet.createBullet(self.imagebox.x + self.imagebox.width - 25, self.imagebox.y + 5, self.direction, "Rifle_bullet", self.damage)
        # Loading the right bullet sprite and adjusting it to appear the barrel of the gun.


class Pistol(Weapon):  # Creating a class for the pistol.
    def __init__(self, dir, posX, posY):
        super().__init__(dir)
        self.ammo_count = 7  # Amount of ammo in the magazine to begin with.
        self.speed = 14
        self.damage = 20  # Damage of each bullet.
        self.weapon_type = "Pistol"
        self.fire_rate = 6  # Amount of bullets that can be fired every second.
        self.images = self.load_images()
        self.image = self.images[dir]
        self.imagebox = self.image.get_rect(x=posX, y=posY)
        # Setting variables to modify Weapon(abc).

    def display_action(self, screen):  # Defining the display action function for the pistol.
        if self.direction == "left":
            return Bullet.createBullet(self.imagebox.x + 3, self.imagebox.y + 1, self.direction, "Nine_mm", self.damage)
        # Loading the left bullet sprite and adjusting it to appear at the barrel of the gun.
        else:
            return Bullet.createBullet(self.imagebox.x + self.imagebox.width - 9, self.imagebox.y + 1, self.direction, "Nine_mm", self.damage)
        # Loading the right bullet sprite and adjusting it to appear the barrel of the gun.


class SMG(Weapon):  # Creating a class for the sub machine gun.
    def __init__(self, dir, posX, posY):
        super().__init__(dir)
        self.ammo_count = 20  # Amount of ammo in the magazine to begin with.
        self.speed = 11
        self.damage = 13  # Damage of each bullet.
        self.weapon_type = "SMG"
        self.fire_rate = 12  # Amount of bullets that can be fired every second.
        self.images = self.load_images()
        self.image = self.images[dir]
        self.imagebox = self.image.get_rect(x=posX, y=posY)
        # Setting variables to modify Weapon(abc).

    def display_action(self, screen):  # Defining the display action function for the sub machine gun.
        if self.direction == "left":
            return Bullet.createBullet(self.imagebox.x + 2, self.imagebox.y + 3, self.direction, "Nine_mm", self.damage)
        # Loading the left bullet sprite and adjusting it to appear at the barrel of the gun.
        else:
            return Bullet.createBullet(self.imagebox.x + self.imagebox.width - 10, self.imagebox.y + 3, self.direction, "Nine_mm", self.damage)
        # Loading the right bullet sprite and adjusting it to appear the barrel of the gun.

class AWM(Weapon):  # Creating a class for the sniper rifle.
    def __init__(self, dir, posX, posY):
        super().__init__(dir)
        self.ammo_count = 3  # Amount of ammo in the magazine to begin with.
        self.damage = 105  # Damage of each bullet.
        self.fire_rate = 3/7  # Amount of bullets that can be fired every second.
        self.weapon_type = "AWM"
        self.images = self.load_images()
        self.image = self.images[dir]
        self.imagebox = self.image.get_rect(x=posX, y=posY)
        # Setting variables to modify Weapon(abc).

    def display_action(self, screen):  # Defining the display action function for the sniper rifle.
        if self.direction == "left":
            pygame.draw.line(screen, COLOURS[0], (self.imagebox.x, self.imagebox.y + 13), (self.imagebox.x - 1260, self.imagebox.y + 13), 2)
            return ((self.imagebox.x - 1260, self.imagebox.y + 13), (self.imagebox.x, self.imagebox.y + 13))
        # Drawing a 'laser' (yellow rectangle) to act as a bullet and adjusting it to appear at the barrel of the gun when facing the left direction.
        else:
            pygame.draw.line(screen, COLOURS[0], (self.imagebox.x + self.imagebox.width, self.imagebox.y + 13), (self.imagebox.x + 125 + 1260, self.imagebox.y + 13), 2)
            return ((self.imagebox.x + self.imagebox.width, self.imagebox.y + 13), (self.imagebox.x + 125 + 1260, self.imagebox.y + 13))
        # Same as above, but the adjustment is modified to appear at the barrel of the gun facing the right direction.

class Shotgun(Weapon):  # Creating a class for the shotgun.
    '''THE SHOTGUN IS STILL IN DEVELOPMENT AND IS CURRENTLY DISABLED'''
    def __init__(self, dir, posX, posY):
        super().__init__(dir)
        self.ammo_count = 6  # Amount of ammo in the magazine to begin with.
        self.speed = 12
        self.damage = 16  # Damage of each bullet.
        self.weapon_type = "Shotgun"
        self.fire_rate = 1  # Amount of bullets fired every second.
        self.images = self.load_images()
        self.image = self.images[dir]
        self.imagebox = self.image.get_rect(x=posX, y=posY)
        # Setting variables to modify Weapon(abc).

    def display_action(self, screen):  # Sefining the display action function for the shotgun.
        if self.direction == "left":
            return Bullet.createBullet(self.imagebox.x - 2, self.imagebox.y + 10, self.direction, "Pellet", self.damage)
        # Loading the pellet sprite to appear at the barrel of the gun when facing left.
        else:
            return Bullet.createBullet(self.imagebox.x + 78, self.imagebox.y + 10, self.direction, "Pellet", self.damage)
        # Loading the pellet sprite to appear the the barrel of the gun when facing right.
