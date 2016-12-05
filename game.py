import pygame
from random import randint

#img = pygame.image.load('plat.png')
#gameDisplay = pygame.display.set_mode((800,600))

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
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

    def update(self):

        self.calc_grav()

        self.rect.x += self.change_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

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
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .8

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -17

    def go_left(self):
        self.change_x = -6 - (pygame.time.get_ticks()/3000.0)

    def go_right(self):
        self.change_x = 6 + (pygame.time.get_ticks()/3000.0)

    def stop(self):
        self.change_x = 0

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill((231, 76, 60))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Light(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Scorebox(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        #super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([width, height])
        self.image.fill((236, 240, 241)) #(236, 240, 241)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Platform(pygame.sprite.Sprite):
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

class Level():
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

    def update(self):
        self.wall_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.light_list.update()
        self.scorebox_list.update()

    def draw(self, screen):
        #BackGround = Background('background.jpg', [0,0])
        screen.fill((236, 240, 241))
        #screen.blit(BackGround.image, BackGround.rect)

        self.platform_list.draw(screen)
        self.wall_list.draw(screen)
        self.enemy_list.draw(screen)
        self.light_list.draw(screen)
        self.scorebox_list.draw(screen)

    def shift_world(self, shift_x):
        # Keep track of the shift amount
        self.world_shift += shift_x

        # Go through all the sprite lists and shift

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for enemy in self.enemy_list:
            enemy.rect.x += shift_x


class Level_01(Level):

    def __init__(self, player):

        Level.__init__(self, player)

        self.level_limit = -1000


        level = []
        offset = 3210
        for i in range(10):
            level.append([210, 40, 500 + (i * offset), randint(150,560)])
            level.append([210, 40, 750 + (i * offset), randint(150,560)])
            level.append([210, 40, 1000 + (i * offset), randint(150,560)])
            level.append([210, 40, 1250 + (i * offset), randint(150,560)])
            level.append([210, 40, 1500 + (i * offset), randint(150,560)])
            level.append([210, 40, 1750 + (i * offset), randint(150,560)])
            level.append([210, 40, 2000 + (i * offset), randint(150,560)])
            level.append([210, 40, 2250 + (i * offset), randint(150,560)])
            level.append([210, 40, 2500 + (i * offset), randint(150,560)])
            level.append([210, 40, 2750 + (i * offset), randint(150,560)])
            level.append([210, 40, 3000 + (i * offset), randint(150,560)])
            level.append([210, 40, 3250 + (i * offset), randint(150,560)])

        wall = Wall(0, 0, 40, 600)
        self.wall_list.add(wall)
        #all_sprite_list.add(wall)

        light = Light(1000, 0, 15, 2000)
        self.light_list.add(light)

        scorebox = Scorebox(680, 20, 100, 100)
        self.scorebox_list.add(scorebox)

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def main():
    pygame.init()

    #Size
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Cube Runner")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))

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

    while not done:

        #screen.fill([255, 255, 255])
        #screen.blit(BackGround.image, BackGround.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
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
        current_level.shift_world(-diff)



        if player.rect.left <= 40:
            done = True;
        if player.rect.y >= 560:
            done = True;

        current_level.draw(screen)
        active_sprite_list.draw(screen)


        clock.tick(60)

        pygame.display.flip()

    print("Your score is " + str(int(player.score)))
    pygame.quit()

if __name__ == "__main__":
    main()
