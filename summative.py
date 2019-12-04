#import modules
import pygame
from spawners import *
from weapons import *
from Player import *
from Master import *
from moviepy.editor import VideoFileClip
import random
import sys
pygame.mixer.pre_init(44100, -16, 2, 512)
#adding paths
sys.path.append("/resources/images")
sys.path.append("/resources/audio")
sys.path.append("/resources")
pygame.init()

# --------------------IMAGES-------------------------
BACKGROUND = ["resources/images/leaves.jpg",      #https://wallhere.com/en/wallpaper/1076275
              "resources/images/landscape.jpg",   #https://wallhere.com/en/wallpaper/100799
              "resources/images/city.jpg"]        #https://www.youtube.com/watch?v=XIXYk6xIhZs
MAP = ["resources/images/map_1.png",
       "resources/images/map_2.png",
       "resources/images/map_3.png"]

WELCOME = "resources/images/Default_Title.png"
WELCOME_OVERLAY = ["resources/images/Hover_Start_Title.png",
                   "resources/images/Hover_Controls_Title.png",
                   "resources/images/Hover_Instructions_Title.png",
                   "resources/images/Hover_Credits_Title.png",
                   "resources/images/Hover_Exit_Title.png"]
CONTROLS = "resources/images/Controls_Page.png"
INSTRUCTIONS = "resources/images/Instructions.png"
CREDITS = "resources/images/Credits.png"
WIN_BANNER = ["resources/images/Player_1_Win.png",
              "resources/images/Player_2_Win.png"]
# the spawning postions of spawner/player on each map
PLAYER_POS = [[20,600,SCREEN_L,600],[20,100,SCREEN_L,100], [20,300,SCREEN_L,300]]
SPAWNER_POS = [[[4], [142, 128], [1004, 32], [950, 468], [20, 412]],
               [[4], [592, 644], [524, 516], [592, 220], [652, 516]],
               [[4], [528, 60], [644,60], [585, 276], [585, 376]]]
TRAILER = "resources/Trailer.mp4" #music source: https://www.youtube.com/watch?v=LuwrQ_RtkGI

#screen settings----------------------------------------------------------------
SCREEN_L = 1280
SCREEN_H = 720
screen_height = 760
screen = pygame.display.set_mode((SCREEN_L,screen_height))

#Arts---------------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW=(255, 200, 110)
consistentFont = pygame.font.SysFont('Calibri', 25, True, False)  # import font

GAMENAME = "Super Slime Rumble!"
pygame.display.set_caption(GAMENAME)

#clock
clock = pygame.time.Clock()


def main():

    running = True
    clip = VideoFileClip(TRAILER)
    clip.preview() # play the trailer
    pygame.quit()
    pygame.init() # resetting the music player
    pygame.mixer.init(44100, -16, 2, 512)
    screen = pygame.display.set_mode((SCREEN_L,screen_height)) #reset the screen
    consistentFont = pygame.font.SysFont('Calibri', 25, True, False)  # import font
    while running == True:

        '''
        WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE //
        WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE //
        WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE // WELCOME PAGE //
        '''
        #loading every image needed for the welcome page
        welcome_screen = pygame.image.load(WELCOME).convert_alpha()
        overlay_start = pygame.image.load(WELCOME_OVERLAY[0]).convert_alpha()
        overlay_controls = pygame.image.load(WELCOME_OVERLAY[1]).convert_alpha()
        overlay_instructions = pygame.image.load(WELCOME_OVERLAY[2]).convert_alpha()
        overlay_credits = pygame.image.load(WELCOME_OVERLAY[3]).convert_alpha()
        overlay_exit = pygame.image.load(WELCOME_OVERLAY[4]).convert_alpha()

        welcome_running = True
        game_running = False
        controls_running = False  # Control page running or not
        instructions_running = False
        credits_running = False
        end_page_running = False
        quit_requested = False

        while welcome_running == True:

            screen.fill(WHITE)
            screen.blit(welcome_screen, [0, 0])

            for event in pygame.event.get(): #check for exit request
                if event.type == pygame.QUIT:
                    welcome_running = False
                    running = False
                    game_running = False
                    end_page_running = False
                    quit_requested = True

            mouse_pos = pygame.mouse.get_pos()

            #start
            if 276 <= mouse_pos[1] <= 304:
                if 580 <= mouse_pos[0] <= 698:
                    screen.blit(overlay_start, [580, 276])

                    eh = pygame.mouse.get_pressed()
                    if eh[0] == 1:
                        welcome_running = False
                        game_running = True

            #controls
            elif 316 <= mouse_pos[1] <= 344:
                if 552 <= mouse_pos[0] <= 728:
                    screen.blit(overlay_controls, [552, 316])

                    clicked = pygame.mouse.get_pressed()
                    if clicked[0] == True:
                        welcome_running = False
                        controls_running = True

            #instructions
            elif 356 <= mouse_pos[1] <= 384:
                if 516 <= mouse_pos[0] <= 764:
                    screen.blit(overlay_instructions, [516, 356])
                    eh = pygame.mouse.get_pressed()
                    if eh[0] == 1:
                        welcome_running = False
                        instructions_running = True

            #credit page
            elif 396 <= mouse_pos[1] <= 424:
                if 564 <= mouse_pos[0] <= 716:
                    screen.blit(overlay_credits, [564, 396])
                    eh = pygame.mouse.get_pressed()
                    if eh[0] == 1:
                        welcome_running = False
                        credits_running = True

            #exit
            elif 436 <= mouse_pos[1] <= 464:
                if 596 <= mouse_pos[0] <= 683:
                    screen.blit(overlay_exit, [596, 436])
                    eh = pygame.mouse.get_pressed()
                    if eh[0] == 1:
                        welcome_running = False
                        game_running = False
                        running = False
                        end_page_running = False
                        quit_requested = True
                        print("WE DON'T LOVE YOU ANYMORE")


            clock.tick(60)
            pygame.display.flip()


        '''
        CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE
        CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE
        CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE // CONTROLS PAGE
        '''

        controls_page = pygame.image.load(CONTROLS).convert_alpha()
        how_to_return = consistentFont.render("Press space to return...", True, BLACK)

        while controls_running:

            screen.fill(WHITE) # fill the screen with white
            screen.blit(controls_page, [0, 0]) # blitting the control page
            screen.blit(how_to_return, [SCREEN_L/2 - how_to_return.get_width()/2, SCREEN_H + 10]) # blitting the return instruction

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    welcome_running = False
                    running = False
                    game_running = False
                    end_page_running = False
                    controls_running = False
                    quit_requested = True
                elif event.type == pygame.KEYDOWN: # if space key is pressed, return to the menu page
                    if event.key == pygame.K_SPACE:
                        welcome_running = True
                        controls_running = False

            clock.tick(60)
            pygame.display.flip()

        '''
        INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS
        INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS
        INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS // INSTRUCTIONS
        '''

        temp = pygame.image.load(INSTRUCTIONS) #load in the page
        instructions_page = pygame.transform.scale(temp, (SCREEN_L, screen_height)).convert_alpha() #scale up

        while instructions_running:

            screen.fill(WHITE)
            screen.blit(instructions_page, [0, 0]) #posting the page onto the screen

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    welcome_running = False
                    running = False
                    game_running = False
                    instructions_running = False
                    end_page_running = False
                    quit_requested = True
                elif event.type == pygame.KEYDOWN: # return to the menu page once the space key is pressed
                    if event.key == pygame.K_SPACE:
                        welcome_running = True
                        instructions_running = False

            clock.tick(60)
            pygame.display.flip()

        '''
        CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS
        CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS
        CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS // CREDITS
        '''

        credits_page = pygame.image.load(CREDITS).convert_alpha()

        while credits_running:

            screen.fill(WHITE)
            screen.blit(credits_page, [0, 0]) #posting the page onto the screen
            screen.blit(how_to_return, [SCREEN_L/2 - how_to_return.get_width()/2, SCREEN_H + 10]) #displaying the return method

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    welcome_running = False
                    running = False
                    game_running = False
                    end_page_running = False
                    credits_running = False
                    quit_requested = True
                elif event.type == pygame.KEYDOWN: # return to the menu page once the space bar is pressed
                    if event.key == pygame.K_SPACE:
                        welcome_running = True
                        credits_running = False

            clock.tick(60)
            pygame.display.flip()


        '''
        GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP
        GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP
        GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP // GAME LOOP
        '''
        master = Master()

        while (master.player_R_score < 5 and master.player_B_score < 5) and game_running == True:
            master.refresh() # emptying all the lists

            #map and background
            random_map_number = random.randint(0, 2) #generating a random number
            map = pygame.image.load(MAP[random_map_number]).convert_alpha()
            background = pygame.image.load(BACKGROUND[random.randint(0, 2)]).convert_alpha() # loading the background
            #background = pygame.image.load(BACKGROUND[2]).convert_alpha()
            #background = pygame.image.load("resources/images/shaq.jpg").convert_alpha()
            background = pygame.transform.scale(background, (1280, 720)).convert_alpha() # scale up
            map = pygame.transform.scale(map, (1280, 720)).convert_alpha() #scale up the map

            # Initializing players
            player_R = Player("RED", map, PLAYER_POS[random_map_number][0], PLAYER_POS[random_map_number][1])
            player_B = Player("BLUE", map, PLAYER_POS[random_map_number][2], PLAYER_POS[random_map_number][3])

            # Add players to a list
            master.player_list.append(player_R)
            master.player_list.append(player_B)

            # render the texts of each player's score
            score1 = consistentFont.render("Player 1 Score: " + str(master.player_R_score), True, BLACK)
            score2 = consistentFont.render("Player 2 Score: "+ str(master.player_B_score), True, BLACK)

            # creating spawners
            for i in range(SPAWNER_POS[random_map_number][0][0]):
                spawner = Spawner(SPAWNER_POS[random_map_number][i+1][0], SPAWNER_POS[random_map_number][i+1][1])
                master.spawner_list.append(spawner)


            # each iteration is a round
            while (not master.check_round_end()) and (not quit_requested):
                #render the texts of players' health
                health1 = consistentFont.render("Player 1 health: " + str(master.player_list[0].health) + "%", True, BLACK)
                health2 = consistentFont.render("Player 2 health: " + str(master.player_list[1].health) + "%", True, BLACK)
                screen.fill (WHITE)
                screen.blit(background, [0, 0])
                screen.blit(map, [0, 0])
                # Window controls
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit_requested = True
                        game_running = False
                        running = False
                        end_page_running = False
                    # Single-press keyboard controls
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_w:
                            player_R.jump()
                        if event.key == pygame.K_UP:
                            player_B.jump()

                keys = pygame.key.get_pressed()

                #player_R key-bindings
                #movement
                if keys[pygame.K_d]:
                    player_R.move("right")
                elif keys[pygame.K_a]:
                    player_R.move("left")
                #fire
                if keys[pygame.K_c]:
                    if player_R.weapon != 0:
                        new_bullet = player_R.fire(screen)
                        if isinstance(new_bullet, tuple):
                            master.hitscan(new_bullet, player_B)
                        elif new_bullet != None:
                            master.bullet_list.append(new_bullet)

                #pick up weapons
                if keys[pygame.K_v]:
                    for each in master.weapon_on_map_list:
                        if master.close_to(player_R, each): # check if the player is on the weapon
                            if ((player_R.weapon != 0 and player_R.weapon # check whether or not the player is allowed to pick up the weapon
                                != each) or player_R.weapon == 0) and (player_R.last_time_switching_weapon
                                                                       + 500 < pygame.time.get_ticks()):
                                #put down the old weapon
                                old_weapon = player_R.pick(each)
                                master.weapon_on_map_list.remove(each) # remove the weapon from the map list
                                master.weapon_picked_list.append(each) # add the weapon to the picked list
                                for each_spawner in master.spawner_list: # inform the spawner that the weapon's taken
                                    if each == each_spawner.weapon:
                                        each_spawner.weapon = 0
                                        each_spawner.time_the_weapon_left = pygame.time.get_ticks() # start timing for respawn
                                if old_weapon != 0 and old_weapon.ammo_count != 0: # if the old weapon still has ammo, put it back on the map
                                    master.weapon_on_map_list.append(old_weapon)

                if keys[pygame.K_s]: # if s is pressed, open the chest
                    for each in master.spawner_list:
                        if master.close_to(player_R, each): # check to see whether the player can reach the spawner
                            if each.state == "crate": # if the crate's not already open
                                each.spawn_weapon()
                                master.weapon_on_map_list.append(each.weapon)

                #player_B key-bindings. identical to the previous section
                if keys[pygame.K_LEFT]:
                    player_B.move("left")
                elif keys[pygame.K_RIGHT]:
                    player_B.move("right")
                if keys[pygame.K_COMMA]:
                    for each in master.weapon_on_map_list:
                        if master.close_to(player_B, each):
                            if ((player_B.weapon != 0 and player_B.weapon
                                != each) or player_B.weapon == 0) and (player_B.last_time_switching_weapon
                                                                       + 500 < pygame.time.get_ticks()):
                                old_weapon = player_B.pick(each)
                                master.weapon_on_map_list.remove(each)
                                master.weapon_picked_list.append(each)
                                for each_spawner in master.spawner_list:
                                    if each == each_spawner.weapon:
                                        each_spawner.weapon = 0
                                        each_spawner.time_the_weapon_left = pygame.time.get_ticks()
                                if old_weapon != 0 and old_weapon.ammo_count != 0:
                                    master.weapon_on_map_list.append(old_weapon)
                if keys[pygame.K_PERIOD]:
                    if player_B.weapon != 0:
                        new_bullet = player_B.fire(screen)
                        if isinstance(new_bullet, tuple):
                            master.hitscan(new_bullet, player_R)
                        elif new_bullet != None:
                            master.bullet_list.append(new_bullet)

                if keys[pygame.K_DOWN]:
                    for each in master.spawner_list:
                        if master.close_to(player_B, each):
                            if each.state =="crate":
                                each.spawn_weapon()
                                master.weapon_on_map_list.append(each.weapon)

                #respawn
                for each in master.spawner_list:
                    if each.state == "weapon" and each.weapon == 0: # check if the spawner satisfies the respawn conditions
                        each.respawn()


                while len(master.weapon_on_map_list) > 6: # remove the first weapon if there are more than 6 weapons on the map
                    for each_spawner in master.spawner_list:
                        if master.weapon_on_map_list[0] == each_spawner.weapon:
                            each_spawner.weapon = 0
                            each_spawner.time_the_weapon_left = pygame.time.get_ticks() # start timing for respawn
                    del master.weapon_on_map_list[0]

                # move each bullet. if it hits something, delete it.
                master.bullet_list = [bullet for bullet in master.bullet_list if bullet.move(map)]
                # check if the bullet hits any player
                master.bullet_list = [bullet for bullet in master.bullet_list if not master.check_bullet_hit(bullet)]



                '''
                screen settings.............................................................................................................
                '''
                # if the crate is not open yet, display it on the screen
                for each in master.spawner_list:
                    if each.state == "crate":
                        screen.blit(each.image, each.imagebox)

                # display the player and the player's weapon(if any)
                for each in master.player_list:
                    each.exist()
                    screen.blit(each.image, each.imagebox)
                    if each.weapon != 0:
                        each.adjust()
                        screen.blit(each.weapon.image, each.weapon.imagebox)

                # display the weapons left on the map
                for each in master.weapon_on_map_list:
                    screen.blit(each.image, each.imagebox)

                #display all the bullets
                for each in master.bullet_list:
                    #pygame.draw.line(screen, YELLOW, each.initial_pos, (each.posX, each.posY), 10)
                    screen.blit(each.image, each. imagebox)

                #display the scores/health
                screen.blit(score1, [100, 730])
                screen.blit(score2, [SCREEN_L - score2.get_width() - 100, 730])
                screen.blit(health1, (350, 730))
                screen.blit(health2, (SCREEN_L - health2.get_width() - 350, 730))

                clock.tick(60)
                pygame.display.flip()

            if not quit_requested: # if the user doesn't want to quit
                if master.player_list[0].health <= 0: # when either of the player dies, set the banners
                    temp = pygame.image.load(WIN_BANNER[1])
                else:
                    temp = pygame.image.load(WIN_BANNER[0])
                #scale the banner
                banner = pygame.transform.scale(temp, (SCREEN_L, SCREEN_H)).convert_alpha()
                #display the banner
                screen.blit(banner, (0,0))
            pygame.display.flip()
            pygame.time.delay(1000)
            # if any player gets 5 kills, end the game
            if master.player_B_score == 5 or master.player_R_score == 5:
                end_page_running = True
                game_running = False



        '''
        END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE //
        END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE //
        END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE // END PAGE //
        '''
        # end game page
        if not quit_requested: # if the user doesn't want to quit
            #set the banners
            if master.player_R_score == 5:
                temp = pygame.image.load(WIN_BANNER[0])
            else:
                temp = pygame.image.load(WIN_BANNER[1])
            #scale up the background
            end_page_background = pygame.transform.scale(temp, (SCREEN_L, SCREEN_H)).convert_alpha()
            #render the texts
            restart_instruction = consistentFont.render("press space to return to the menu page...", True, BLACK)
            score1 = consistentFont.render("Player 1 Score: " + str(master.player_R_score), True, BLACK)
            score2 = consistentFont.render("Player 2 Score: "+ str(master.player_B_score), True, BLACK)

        while end_page_running:
            screen.fill(WHITE)
            screen.blit(end_page_background, [0, 0]) # display the background
            screen.blit(restart_instruction, [SCREEN_L/2 - restart_instruction.get_width()/2, SCREEN_H + 10]) # display the restart text
            # display the scores
            screen.blit(score1, (300, 400))
            screen.blit(score2, (SCREEN_L - 300 - score2.get_width(), 400))

            for event in pygame.event.get(): # if the user wants to quit, then quit
                if event.type == pygame.QUIT:
                    end_page_running = False
                    running = False

                elif event.type == pygame.KEYDOWN: # if the user wants to play again, back to the menu page
                    if event.key == pygame.K_SPACE:
                        welcome_running = True
                        end_page_running = False

            clock.tick(60)
            pygame.display.flip()

if __name__ == '__main__':
    main()
