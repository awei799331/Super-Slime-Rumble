#import modules
import pygame
import sys
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
#image sources --------------------------------------------------------------------------------------
sys.path.append("/resources/images")

BULLETS = {
    "Pellet": {
        "left": "resources/images/Pellet.png",
        "right": "resources/images/Pellet.png"
    },
    "Nine_mm": {
        "left": "resources/images/9mm_Left.png",
        "right": "resources/images/9mm_Right.png"
    },
    "Rifle_bullet": {
        "left": "resources/images/Rifle_Bullet_Left.png",
        "right": "resources/images/Rifle_Bullet_Right.png"
    }
}

#constant
BLACK = (0, 0, 0)

class Bullet(object):
    def __init__(self, Xpos, Ypos, direction, type, damage):
        self.posX = Xpos
        self.posY = Ypos
        self.direction = direction
        self.speed = None
        self.image = pygame.image.load(BULLETS[type][direction]).convert_alpha()
        self.imagebox = self.image.get_rect(x=Xpos, y=Ypos)
        self.initial_pos = (self.posX, self.posY)
        self.damage = damage

    def move(self, map):
        if self.posX >= 1260 or self.posX <= 0:
            return False
        if self.direction == "left":
             # check if the player is going into a wall. If the player is going into a wall,
             # move is illegal
            for x in range(self.posX, self.posX - self.speed - 1, -10):
                for y in range(self.posY, self.posY + self.imagebox.height + 1):
                    if map.get_at((x, y)) == BLACK:
                        return False
            self.imagebox.x -= self.speed
            self.posX -= self.speed
            return True
        else:
            for x in range(self.posX, self.posX + self.speed + 1, 10):
                for y in range(self.posY, self.posY +self.imagebox.height + 1):
                    if map.get_at((x, y)) == BLACK:
                        return False
            self.imagebox.x += self.speed
            self.posX += self.speed
            return True

    # a static method that creates bullets
    def createBullet(Xpos, Ypos, direction, type, damage):
        if type == "Pellet":
            return Pellet(Xpos, Ypos, direction, damage)
        elif type == "Rifle_bullet":
            return Rifle_bullet(Xpos, Ypos, direction, damage)
        elif type == "Nine_mm":
            return Nine_mm(Xpos, Ypos, direction, damage)


class Pellet(Bullet):
    def __init__(self, x, y, direction, damage):
        super().__init__(x, y, direction, "Pellet", damage)
        self.speed = 40 # bullet speed

class Nine_mm(Bullet):
    def __init__(self, x, y, direction, damage):
        super().__init__(x, y, direction, "Nine_mm", damage)
        self.speed = 40 # bullet speed

class Rifle_bullet(Bullet):
    def __init__(self, x, y, direction, damage):
        super().__init__(x, y, direction, "Rifle_bullet", damage)
        self.speed = 45 # bullet speed
