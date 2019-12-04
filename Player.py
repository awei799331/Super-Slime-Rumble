#import modules
import pygame
import sys
pygame.mixer.pre_init(44100, -16, 2, 512)
#source
sys.path.append("/resources/images")
# adjusted weapon placement
weapon_move_array = {"Pistol": [25, 10, 40, -40],
                     "AK": [25,18,11,-12],
                     "Shotgun": [19, 6, 25, -25],
                     "AWM": [13, 5, 12, -12],
                     "SMG": [21, 10, 15, -15]}
# sprites
BLOBS = {
    "RED": {
        "normal" : {
            "move": {
                "right": "resources/images/Red_Blob_Move_Right.Png",
                "left": "resources/images/Red_Blob_Move_Left.Png"
            },
            "jump": {
                "right": "resources/images/Red_Blob_Jump_Right.Png",
                "left": "resources/images/Red_Blob_Jump_Left.Png"
            },
            "fall": {
                "right": "resources/images/Red_Blob_Fall_Right.Png",
                "left": "resources/images/Red_Blob_Fall_Left.Png"
            }
        },
        "hurt":{
            "move": {
                "right": "resources/images/Red_Below_50_Move_Right.Png",
                "left": "resources/images/Red_Below_50_Move_Left.Png"
            },
            "jump": {
                "right": "resources/images/Red_Below_50_Jump_Right.Png",
                "left": "resources/images/Red_Below_50_Jump_Left.Png"
            },
            "fall": {
                "right": "resources/images/Red_Below_50_Fall_Right.Png",
                "left": "resources/images/Red_Below_50_Fall_Left.Png"
            }
        }
    },
    "BLUE": {
        "normal": {
            "move": {
                "right": "resources/images/Blue_Blob_Move_Right.Png",
                "left": "resources/images/Blue_Blob_Move_Left.Png"
            },
            "jump": {
                "right": "resources/images/Blue_Blob_Jump_Right.Png",
                "left": "resources/images/Blue_Blob_Jump_Left.Png"
            },
            "fall": {
                "right": "resources/images/Blue_Blob_Fall_Right.Png",
                "left": "resources/images/Blue_Blob_Fall_Left.Png"
            }
        },
        "hurt": {
            "move": {
                "right": "resources/images/Blue_Below_50_Move_Right.Png",
                "left": "resources/images/Blue_Below_50_Move_Left.Png"
            },
            "jump": {
                "right": "resources/images/Blue_Below_50_Jump_Right.Png",
                "left": "resources/images/Blue_Below_50_Jump_Left.Png"
            },
            "fall": {
                "right": "resources/images/Blue_Below_50_Fall_Right.Png",
                "left": "resources/images/Blue_Below_50_Fall_Left.Png"
            }
        }
    }
}
# constants
SCREEN_L = 1280
SCREEN_H = 720
GRAV_ACC = 1
BLACK = (0, 0, 0)

class Player(object):
    '''
    the player class takes in four parameters:
    1. the colour of the player, "RED" or "BLUE"
    2. the map
    3. the initial xPos
    4. the initial yPos
    '''
    def __init__(self, colour, map, xPos, yPos): # return a player class object
        # instance variables
        self.speed = 7
        self.weapon = 0
        self.colour = colour
        self.width = 45
        self.height = 45
        self.yVel = 0
        self.movement_type = "move" # movement type: "move", "fall", or "jump"
        self.health = 100
        self.last_time_switching_weapon = -500
        self.map = map
        self.health_condition = "normal"
        self.sprite_dictionary = {}
        self.load_sprites(colour)

        if colour == "RED":
            self.direction = "right"
            #adjust the position
            self.posX = xPos
            self.posY = yPos - self.height
            # set the image
            self.image = self.sprite_dictionary[self.health_condition][self.movement_type][self.direction]
            # set the hitbox
            self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)
        else:
            self.direction = "left"
            #adjust the position
            self.posX = xPos - self.width - 20
            self.posY = yPos - self.height
            #set the image
            self.image = self.sprite_dictionary[self.health_condition][self.movement_type][self.direction]
            #set the hitbox
            self.imagebox = self.image.get_rect(x=self.posX, y=self.posY)


        # Movement possibility
        self.jumped = False

    def exist(self): # the exist method is called every single frame.
        # constantly check the movement type
        if self.yVel < 0:
            self.movement_type = "fall"
        elif self.yVel > 0:
            self.movement_type = "jump"
        elif self.yVel == 0:
            self.movement_type = "move"

        # check whether or not it's on a platform
        if not self.check_on_platform():
            if self.yVel <= 0:
                self.movement_type = "fall"
            else:
                self.movement_type = "jump"
        else: self.jumped = False

        #GRAVITY is implemented here
        if self.movement_type == "fall":
            self.yVel -= GRAV_ACC
            self.imagebox.y = self.check_landing()
        elif self.movement_type == "jump":
            self.yVel -= GRAV_ACC
            self.imagebox.y = self.check_head()
        else:
            pass

        #set the image
        self.image = self.sprite_dictionary[self.health_condition][self.movement_type][self.direction]

    def move(self, direction):
        #reset the direction
        self.direction = direction

        if direction == "right":
            temp = self.check_horizontal_move("right") # check if the move is allowed
            if temp == 9999:
                self.imagebox.x += self.speed
            else:
                self.imagebox.x = temp - self.width + 1
        elif direction == "left":
            temp = self.check_horizontal_move("left") # check if the move is allowed
            if temp == 9999:
                self.imagebox.x -= self.speed
            else:
                self.imagebox.x = temp

    def jump(self):
        # check if the player is already in the air
        if self.jumped == False:
            # Set Jump Values
            self.yVel = 20
            self.jumped = True
            return True

    def hurt(self, damage):
        self.health -= damage # takes the damage out of the player's health
        if  0 < self.health <= 49:
            self.health_condition = "hurt"
            #set the new image
            self.image = self.sprite_dictionary[self.health_condition][self.movement_type][self.direction]
        # die
        if self.health <= 0:
            self.health = 0

    #pick up the weapon, return the old weapon. When there's no old_weapon, return 0
    def pick(self, weapon):
        #pick up the weapon, return the reference to the old weapon
        old_weapon = self.weapon
        self.weapon = weapon
        self.last_time_switching_weapon = pygame.time.get_ticks() # set the next time the player is allowed to pick up the weapon
        self.adjust()
        return old_weapon

    def adjust(self):
        #adjust the image and the imagebox of the weapon so that it looks cool
        if self.weapon.direction != self.direction:
            self.weapon.change_direction()
        if self.jumped != True:
            self.weapon.imagebox.y = self.imagebox.y + weapon_move_array[self.weapon.weapon_type][0]
        else:
            self.weapon.imagebox.y = self.imagebox.y + weapon_move_array[self.weapon.weapon_type][1]
        if self.direction == "right":
            self.weapon.imagebox.x = self.imagebox.x + weapon_move_array[self.weapon.weapon_type][2]
        else:
            self.weapon.imagebox.x = self.imagebox.x + self.imagebox.width - self.weapon.imagebox.width + weapon_move_array[self.weapon.weapon_type][3]

    def fire(self, screen):
        #click the trigger
        return self.weapon.fire(screen)

    def check_horizontal_move(self, direction):
        '''
        the movement checks whether or not the move is legal. returns the place the character can move to.
        if the move is legal, return 9999(not a possible return value if the move isn't legal)
        '''
        #left/right
        if direction == "left":
            #if the player goes into a wall
            for y in range(0, self.height, 4):
                if self.map.get_at((self.imagebox.x - self.speed, self.imagebox.y + y)) == BLACK:
                    i = self.imagebox.x - self.speed
                    #push the player back if it's not a legal move. Find the last legal place and return the x coordinate
                    while self.map.get_at((i, self.imagebox.y + y)) == BLACK:
                        i += 1
                    return i

        elif direction == "right":
            for y in range(0, self.height, 4):
                if self.map.get_at((self.imagebox.x + self.imagebox.width + self.speed, self.imagebox.y + y)) == BLACK:
                    i = self.imagebox.x + self.imagebox.width + self.speed
                    while self.map.get_at((i, self.imagebox.y + y)) == BLACK:
                        i -= 1
                    return i
        return 9999

    def check_landing(self):
        # check whether or not the player is landing on a platform
        if self.direction == "right":
            for x in range(9, self.width, 7):
                for y in range(0, -self.yVel):
                    # if the player is approaching a platform
                    if self.map.get_at((self.imagebox.x + x, self.imagebox.y + self.imagebox.height + 1 + y)) == BLACK:
                        # allow the player to jump again
                        self.jumped = False
                        # the player shouldn't fall throught the platform
                        self.yVel = 0
                        # return the place of the platform
                        return self.imagebox.y + y + 1
        #similar to the previous section
        elif self.direction == "left":
            for x in range(0, self.width - 9, 7):
                for y in range(0, -self.yVel):
                    if self.map.get_at((self.imagebox.x + x, self.imagebox.y + self.imagebox.height + 1 + y)) == BLACK:
                        self.jumped = False
                        self.yVel = 0
                        return self.imagebox.y + y + 1
        return self.imagebox.y - self.yVel

    def check_on_platform(self):
        # check if the player is on a platform. If yes, return False.
        if self.direction == "left":
            for x in range(0, self.width - 9, 7):
                if self.map.get_at((self.imagebox.x + x, self.imagebox.y + self.imagebox.height + 1)) == BLACK:
                    return True
        else:
            for x in range(9, self.width, 7):
                if self.map.get_at((self.imagebox.x + x, self.imagebox.y + self.imagebox.height + 1)) == BLACK:
                    return True
        self.jumped = True
        return False

    def check_head(self):
        # check whether or not the player hits its head
        for x in range(0, self.width, 4):
            for y in range(0, self.yVel):
                if self.map.get_at((self.imagebox.x + x, self.imagebox.y - 1 - y)) == BLACK:
                    self.yVel = 0
                    return self.imagebox.y - y
        return self.imagebox.y - self.yVel

    def load_sprites(self, colour):
        # load all the images into a nested dictionary
        temp_dict0 = {}
        for health_condition, inside_health_condition in BLOBS[colour].items():
            temp_dict1 = {}
            for movement_type, inside_movement_type in inside_health_condition.items():
                temp_dict2 = {}
                for direction, sprite_name in inside_movement_type.items():
                    temp_dict2[direction] = pygame.image.load(sprite_name)
                    temp_dict2[direction] = pygame.transform.scale(temp_dict2[direction], (round(temp_dict2[direction].get_width()/1.25), round(temp_dict2[direction].get_height()/1.25))).convert_alpha()
                temp_dict1[movement_type] = temp_dict2
            temp_dict0[health_condition] = temp_dict1
        self.sprite_dictionary = temp_dict0
