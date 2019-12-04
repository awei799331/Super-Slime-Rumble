#import modules
import pygame
from spawners import *
from Player import *
from weapons import *
#preset the mixer
pygame.mixer.pre_init(44100, -16, 2, 512)

class Master(object):
    def __init__(self):
        # a lot of lists
        self.weapon_picked_list = [] # only contains the weapons the players are holding.  0<=length<=2
        self.weapon_on_map_list = [] # only contains the useable weapons left on the map
        self.player_list = [] # a list of the players
        self.spawner_list = [] # a list of the spawners
        self.bullet_list = [] # a list of bullets
        #score count of the two players
        self.player_R_score = 0
        self.player_B_score = 0

    def close_to(self, objectA, objectB): # check whether or not two sprites overlap
        return objectA.imagebox.colliderect(objectB.imagebox)

    def check_bullet_hit(self, bullet): # check if a bullet hits a player
        for player in self.player_list:
            if bullet.imagebox.colliderect(player.imagebox):
                player.hurt(bullet.damage)
                return True
        return False

    def check_round_end(self): # check whether or not one person's health is below 0
        for player in self.player_list:
            if player.health == 0:
                if player.colour == 'RED':
                    self.player_B_score += 1
                    return True
                else:
                    self.player_R_score += 1
                    return True

    def refresh(self): # reset all the lists
        self.weapon_picked_list = []
        self.weapon_on_map_list = []
        self.player_list = []
        self.spawner_list = []
        self.bullet_list = []

    def hitscan(self, laser, enemy): # for AWM. check if the laser hit the opposing character
        if enemy.imagebox.y <= laser[1][1] <= enemy.imagebox.y + enemy.imagebox.height:
            if  laser[0][0]<= enemy.imagebox.x <= laser[1][0] or laser[0][0]<= enemy.imagebox.x + enemy.imagebox.width <= laser[1][0]:
                enemy.health = 0
