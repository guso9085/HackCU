#Gustav Solis
#Ranganathan Chidambaranathan
#PROJECT 2

#USED PROGRAMARCADEGAMES.COM TO HELP UNDERSTAND PYGAME SYNTAX AND GET A GOOD START

import pygame                                              #IMPORT LIBRARY
from random import randint
#import sys
#from termcolor import colored, cprint

#img = pygame.image.load('plat.png')
#gameDisplay = pygame.display.set_mode((800,600))

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 600


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Player(pygame.sprite.Sprite):                         #FIRST CLASS: PLAYER CLASS
    def __init__(self):
        super().__init__()
        #self.jumpsleft = 1
        #self.inair = true
        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill((52, 73, 94))
        self.score = 0
        self.rect = self.image.get_rect()
        self.change_x = 0
        self.change_y = 0
        self.level = None

    def update(self):                                        #FIRST METHOD: PLAYER MOVEMENT
        self.grav()
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:                        #FOR LOOP
            if self.change_x >= 0:
                self.rect.right = block.rect.left
            elif self.change_x <= 0:
                self.rect.left = block.rect.right

        block_hit_list = pygame.sprite.spritecollide(self, self.level.light_list, False)
        for block in block_hit_list:
            if self.change_x >= 0:
                self.rect.right = block.rect.left
            elif self.change_x <= 0:

                self.rect.left = block.rect.rights
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            self.score = self.score + 1*(pygame.time.get_ticks()/5000.0)
            block.image.fill((randint(0,255), randint(0,255), randint(0,255)))
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:                         #ELSE IF STATEMENT
                self.rect.top = block.rect.bottom
            self.change_y = 0

    def grav(self):                                    #SECOND METHOD: GRAVITY
        if self.change_y == 0:
            self.change_y = 1
        else:                                               #IF + ELSE STATEMENT
            self.change_y += .8
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):                                         #THIRD METHOD: JUMP
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -17

    def left(self):                                      #FOURTH METHOD: LEFT
        self.change_x = -6 - (pygame.time.get_ticks()/3000.0)

    def right(self):                                     #FIFTH METHOD: RIGHT
        self.change_x = 6 + (pygame.time.get_ticks()/3000.0)

    def stop(self):                                         #SIXTH METHOD: STOP
        self.change_x = 0

class Wall(pygame.sprite.Sprite):                           #SECOND CLASS: LEFT WALL
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((231, 76, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Light(pygame.sprite.Sprite):                          #THIRD CLASS: RIGHT WALL
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Scorebox(pygame.sprite.Sprite):                       #FOURTH CLASS: SCOREBOX
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((236, 240, 241)) #(236, 240, 241)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):                       #FIFTH CLASS: PLATFORM
    def __init__(self, width, height):
        super().__init__()
        #Custom Platform Image
        #ss = pygame.image.load("plat.png").convert()
        self.image = pygame.Surface([width, height]).convert()
        #self.image.blit(ss, (0,0), (0,0,210,70))
        #self.image.set_colorkey((0,0,0))
        self.image.fill((71, 71, 107))
        self.rect = self.image.get_rect()

'''class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
'''

class Level():                                              #SIXTH CLASS: LEVEL
    wall_list = None
    platform_list = None
    enemy_list = None
    light_list = None
    world_shift = 0

    def __init__(self, player):
        self.light_list = pygame.sprite.Group()
        self.wall_list = pygame.sprite.Group()
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.scorebox_list = pygame.sprite.Group()
        self.player = player

    def update(self):                                       #FIRST METHOD
        self.wall_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.light_list.update()
        self.scorebox_list.update()

    def draw(self, screen):                                 #SECOND METHOD
        #BackGround = Background('background.jpg', [0,0])
        screen.fill((236, 240, 241))
        #screen.blit(BackGround.image, BackGround.rect)
        self.platform_list.draw(screen)
        self.wall_list.draw(screen)
        self.enemy_list.draw(screen)
        self.light_list.draw(screen)
        self.scorebox_list.draw(screen)

    def shifty(self, shift_x):                         #THIRD METHOD: SHIFTING WORLD AND OBJECTS
        self.world_shift += shift_x
        for platform in self.platform_list:                 #FOR LOOP
            platform.rect.x += shift_x
        for enemy in self.enemy_list:                       #FOR LOOP
            enemy.rect.x += shift_x


class MLevel(Level):                                      #THIRD CLASS: MAIN LEVEL
    def __init__(self, player):
        Level.__init__(self, player)
        self.level_limit = -1000
        level = []                                          #LIST
        offset = 3210
        for i in range(20):                                 #FOR LOOP WITH RANGE
            level.append([210, 40, 500 + (i * offset), randint(150,560)])
            level.append([210, 40, 770 + (i * offset), randint(150,560)])
            level.append([210, 40, 1040 + (i * offset), randint(150,560)])
            level.append([210, 40, 1310 + (i * offset), randint(150,560)])
            level.append([210, 40, 1580 + (i * offset), randint(150,560)])
            level.append([210, 40, 1850 + (i * offset), randint(150,560)])
            level.append([210, 40, 2120 + (i * offset), randint(150,560)])
            level.append([210, 40, 2390 + (i * offset), randint(150,560)])
            level.append([210, 40, 2660 + (i * offset), randint(150,560)])
            level.append([210, 40, 2930 + (i * offset), randint(150,560)])
            level.append([210, 40, 3200 + (i * offset), randint(150,560)])
            level.append([210, 40, 3470 + (i * offset), randint(150,560)])

        wall = Wall(0, 0, 40, 600)
        self.wall_list.add(wall)

        light = Light(1000, 0, 15, 2000)
        self.light_list.add(light)

        scorebox = Scorebox(680, 20, 100, 100)
        self.scorebox_list.add(scorebox)

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def main():
    File = "scores.txt"
    boom = False
    while boom == False:
        answer = input("Would you like to enter a name for your score? (Y/N) : ")
        if answer == 'Y':
            answer = input("Name: ")
            boom = True
        elif answer == 'N':
            print("Bye Bye")
            answer = "Unknown"
            boom = True
        elif answer != 'X' or answer != 'Y':
            print("Invalid input")

    pygame.init()
    highscore = 0
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Cube Runner")
    player = Player()
    level_list = []                                         #LIST
    level_list.append(MLevel(player))
    current_level_no = 0
    current_level = level_list[current_level_no]
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    player.rect.x = 340
    #player.rect.y = SCREEN_HEIGHT - player.rect.height
    player.rect.y = 0
    active_sprite_list.add(player)
    done = False
    clock = pygame.time.Clock()

    try:                                                        #TRY AND EXCEPT
        myFile = open(File, "r")                                #FILE IO, READING
        for line in myFile:
            split = line.split("|")
            if int(split[1]) > highscore:
                highscore = int(split[1])
    except:
        print("Error")

    frame_count = 0
    frame_rate = 60
    #start_time = 90

    font = pygame.font.Font(None, 60)


    while not done:                                         #WHILE LOOP
        #screen.fill([255, 255, 255])
        #screen.blit(BackGround.image, BackGround.rect)
        for event in pygame.event.get():                    #NESTED FOR LOOP
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left()
                if event.key == pygame.K_RIGHT:
                    player.right()
                if event.key == pygame.K_UP:
                    player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        active_sprite_list.update()
        current_level.update()

        #Constant Scrolling
        diff = 7 + (pygame.time.get_ticks()/3000.0)
        current_level.shifty(-diff)

        if player.rect.left <= 40:
            done = True;
        if player.rect.y >= 560:
            done = True;
        current_level.draw(screen)
        active_sprite_list.draw(screen)
        clock.tick(60)

        if player.score <= 100 and player.score < highscore:
            Soutput_string = "{}".format(int(player.score))
            stext = font.render(Soutput_string, True, ((26,188,156)))
            screen.blit(stext, [880, 20])
        elif player.score > 100 and player.score <= 500 and player.score < highscore:
            Soutput_string = "{}".format(int(player.score))
            stext = font.render(Soutput_string, True, ((46,204,113)))
            screen.blit(stext, [880, 20])
        elif player.score > 500 and player.score <= 1000 and player.score < highscore:
            Soutput_string = "{}".format(int(player.score))
            stext = font.render(Soutput_string, True, ((52,152,219)))
            screen.blit(stext, [880, 20])
        elif player.score > 1000 and player.score <= 2000 and player.score < highscore:
            Soutput_string = "{}".format(int(player.score))
            stext = font.render(Soutput_string, True, ((155,89,182)))
            screen.blit(stext, [880, 20])
        elif player.score > 2000 and player.score < highscore:
            Soutput_string = "{}".format(int(player.score))
            stext = font.render(Soutput_string, True, ((192,57,43)))
            screen.blit(stext, [880, 20])
        elif player.score > highscore:
            Soutput_string = "{}".format(int(player.score))
            stext = font.render(Soutput_string, True, ((randint(0,255), randint(0,255), randint(0,255))))
            screen.blit(stext, [880, 20])


        pygame.display.flip()
    myFile = open(File, "a")                                #FILE IO, WRITING
    myFile.write(answer + "|")
    myFile.write(str(int(player.score))+ "\n")

    Library = {}
    highscores = []

    myFile = open(File, "r")                                #FILE IO, READING
    for line in myFile:
        split = line.split("|")
        if int(split[1]) in Library:                        #LIBRARY W/ COMPLEX OBJECT
            Library[int(split[1])].append(str(split[0]))
        else:
            Library[int(split[1])] = [str(split[0])]
        #print(str(Library[int(split[1])]))
        highscores.append(int(split[1]))

    highscores.sort(reverse=True)

    #colored('hello', 'red'), colored('world', 'green')

    #print(bcolors.WARNING + "Warning: No active frommets remain. Continue?" + bcolors.ENDC)

    #print(bcolors.WARNING + "SCORE: " + str(int(player.score)) + bcolors.ENDC)
    print(bcolors.BOLD + "TOP 5 SCORES" + bcolors.ENDC)
    print(bcolors.HEADER + "1] " + str(Library[highscores[0]]) + " scored " + bcolors.BOLD + str(highscores[0]) + bcolors.ENDC)
    print(bcolors.OKBLUE + "2] " + str(Library[highscores[1]]) + " scored " + bcolors.BOLD + str(highscores[1]) + bcolors.ENDC)
    print(bcolors.OKGREEN + "3] " + str(Library[highscores[2]]) + " scored " + bcolors.BOLD + str(highscores[2]) + bcolors.ENDC)
    print(bcolors.WARNING + "4] " + str(Library[highscores[3]]) + " scored " + bcolors.BOLD + str(highscores[3]) + bcolors.ENDC)
    print(bcolors.FAIL + "5] " + str(Library[highscores[4]]) + " scored " + bcolors.BOLD + str(highscores[4]) + bcolors.ENDC)
    print(bcolors.UNDERLINE + "You scored: " + str(int(player.score)) + "\n"+ bcolors.ENDC)

    pygame.quit()
if __name__ == "__main__":
    main()
