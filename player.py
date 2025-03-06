import pygame
import math
from settings import *

class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.alive = True
        self.inventory = []
        self.moving = False
        self.playing = False

    def move(self):
        if self.alive and not self.game.win:
            sin_a = math.sin(self.angle)
            cos_a = math.cos(self.angle)

            # Incrament
            dx, dy = 0, 0

            # Speed
            speed = PLAYER_SPEED * self.game.delta_time

            speed_sin = speed * sin_a # Solve the equation
            speed_cos = speed * cos_a

            # Check key inputs
            key = pygame.key.get_pressed()

            if key[pygame.K_w]:
                dx += speed_cos
                dy += speed_sin
                self.moving = True
            if key[pygame.K_s]:
                dx += -speed_cos
                dy += -speed_sin
                self.moving = True
            if key[pygame.K_a]:
                dx += speed_sin
                dy += -speed_cos
                self.moving = True
            if key[pygame.K_d]:
                dx += -speed_sin
                dy += speed_cos
                self.moving = True
            if not key[pygame.K_w] and not key[pygame.K_s] and not key[pygame.K_a] and not key[pygame.K_d]: # If nothing pressed
                self.moving = False
                self.playing = False
                self.game.sound.footsteps.stop()

            if key[pygame.K_LEFT]:
                self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
            if key[pygame.K_RIGHT]:
                self.angle += PLAYER_ROT_SPEED * self.game.delta_time

            self.check_wall_collisions(dx, dy)

            self.angle %= math.tau # If angle greater than 2*pi, loop it back around

    def draw(self):
        pygame.draw.line(self.game.screen, "yellow", (self.x * 100, self.y * 100),
                        (self.x * 100 + WIDTH * math.cos(self.angle),
                         self.y  * 100 + WIDTH * math.sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        if self.alive and not self.game.win:
            mousex, mousey = pygame.mouse.get_pos()
            if mousex < MOUSE_BORDER_LEFT or mousex > MOUSE_BORDER_RIGHT:
                pygame.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            self.rel = pygame.mouse.get_rel()[0]
            self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def item_pickup(self):
        keys = pygame.key.get_pressed()
                            # Center  C-Left   C-Right   Top     Bottom   T- Left   T-RIGHT   B-LEFT  B-RIGHT
        all_use_locations = [(33,15), (32,15), (34,15), (33,16), (33,14), (32,16), (34, 16), (32,14), (34,14) ]
        for sprite in self.game.object_handler.sprite_list:
            if self.map_pos in all_use_locations:
                if keys[pygame.K_e]:
                    self.inventory.append("Key")
                    for sprite in self.game.object_handler.sprite_list:
                        if sprite.key: # If key
                            self.game.object_handler.sprite_list.remove(sprite)
                return True
            
    def use_item(self):
        keys = pygame.key.get_pressed()

        all_use_locations = [(1,16), (1,17), (1,15), (2,15), (2,16), (2,17), (67,16), (67,17), (67,15), (68,15), (68,16), (68,17)]
        if self.map_pos in all_use_locations:
            if keys[pygame.K_e] and "Key" in self.inventory: # Change this
                self.game.win = True
            return True

    def update(self):
        self.move()
        self.mouse_control()
        self.item_pickup()
        self.use_item()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collisions(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time # Gives player its size
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy
        if not self.playing and self.moving == True and AUDIO:
            self.playing = True
            self.game.sound.footsteps.play(-1)

    @property
    def pos(self):
        return self.x, self.y
    
    @property
    def map_pos(self):
        return int(self.x), int(self.y)