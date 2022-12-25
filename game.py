import pygame
import pytmx
import pyscroll
from players import Player
from operator import itemgetter


class Game:

    def __init__(self):
        # create game windows
        self.map = "world"
        self.screen = pygame.display.set_mode((900, 900))
        pygame.display.set_caption("Game PortFolio")

        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # draw map call
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # generate player
        player_position = tmx_data.get_object_by_name('player')
        self.player = Player(player_position.x, player_position.y)
        self.group.add(self.player)
        # list colision
        # definir les rect de maison
        enter_house = tmx_data.get_object_by_name('enter')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle(self):
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_UP]:
            self.player.move_up()
            self.player.change_animation('left')
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_animation('down')
        if pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_animation('up')
        if pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_animation('right')

    def switch_house(self):
        tmx_data = pytmx.util_pygame.load_pygame('house_int.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # draw map call
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group.add(self.player)
        # list colision
        # definir les rect de maison
        enter_house = tmx_data.get_object_by_name('exit_house')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)
        # spawn point

        spawn_house_point = tmx_data.get_object_by_name('spawn_house')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y - 20

    def switch_world(self):
        tmx_data = pytmx.util_pygame.load_pygame('carte.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2

        # draw map call
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)

        self.walls = []

        for obj in tmx_data.objects:
            if obj.name == 'collision':
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group.add(self.player)
        # list colision
        # definir les rect de maison
        enter_house = tmx_data.get_object_by_name('enter')
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        # spawn point

        spawn_house_point = tmx_data.get_object_by_name('enter_house_exit')
        self.player.position[0] = spawn_house_point.x
        self.player.position[1] = spawn_house_point.y + 20

    def update(self):
        self.group.update()

        # verifier entrer dans la maison
        if self.map == 'world' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house()
            self.map = 'house'

        # verifier entrer dans la maison
        if self.map == 'house' and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_world()
            self.map = 'world'

        # verifier colision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    def run(self):

        clock = pygame.time.Clock()

        runner = True
        while runner:
            self.player.save_location()
            self.handle()
            self.update()
            self.group.draw(self.screen)
            self.group.center(self.player.rect)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    runner = False

            clock.tick(60)
        pygame.quit()
