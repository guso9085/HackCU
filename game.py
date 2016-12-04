import pygame

#img = pygame.image.load('plat.png')
gameDisplay = pygame.display.set_mode((800,600))

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        self.image.fill((52, 73, 94))

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

            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y = 0

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35

        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -6

    def go_right(self):
        self.change_x = 6

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

class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        #pygame.Surface.blit(img, (0,0))
        #gameDisplay.blit(img, (105,-100))
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
        self.player = player

    def update(self):
        self.wall_list.update()
        self.platform_list.update()
        self.enemy_list.update()
        self.light_list.update()

    def draw(self, screen):
        #BackGround = Background('background.jpg', [0,0])
        screen.fill((236, 240, 241))
        #screen.blit(BackGround.image, BackGround.rect)

        self.platform_list.draw(screen)
        self.wall_list.draw(screen)
        self.enemy_list.draw(screen)
        self.light_list.draw(screen)

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
        offset = 2030
        for i in range(10):
            level.append([210, 70, 500 + (i * offset), 550])
            level.append([210, 70, 800 + (i * offset), 400])
            level.append([210, 70, 1000 + (i * offset), 500])
            level.append([210, 70, 1120 + (i * offset), 280])
            level.append([210, 70, 1250 + (i * offset), 550])
            level.append([210, 70, 1400 + (i * offset), 600])
            level.append([210, 70, 1510 + (i * offset), 200])
            level.append([210, 70, 1690 + (i * offset), 380])
            level.append([210, 70, 1830 + (i * offset), 150])
            level.append([210, 70, 1980 + (i * offset), 600])
            level.append([210, 70, 2190 + (i * offset), 200])
            level.append([210, 70, 2320 + (i * offset), 380])

        wall = Wall(0, 0, 40, 600)
        self.wall_list.add(wall)
        #all_sprite_list.add(wall)

        light = Light(800, 0, 15, 600)
        self.light_list.add(light)

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

    pygame.display.set_caption("Side-scrolling Platformer")

    player = Player()

    level_list = []
    level_list.append(Level_01(player))

    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
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
        diff = 7
        current_level.shift_world(-diff)

        if player.rect.left <= 40:
            done = True;

        current_level.draw(screen)
        active_sprite_list.draw(screen)

        clock.tick(60)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
