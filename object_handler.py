import pygame
from settings import *
from sprite_object import *
from npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = "resources/sprites/npc/"
        self.static_sprite_path = ["resources/sprites/static_sprites"]
        self.distance_stat_transfer = 0
        add_sprite = self.add_sprite
        add_npc = self.add_npc

        # Add Sprites
        add_sprite(SpriteObject(game, key = True))
        add_sprite(SpriteObject(game, "resources/textures/cabinet.png", (5.7, 16.3)))
        add_sprite(SpriteObject(game, "resources/textures/table.png", (5.3, 26.7), scale = 0.8, shift=0.38))
        add_sprite(SpriteObject(game, "resources/textures/table.png", (1.5, 30.3), scale = 0.8, shift=0.38))
        add_sprite(SpriteObject(game, "resources/textures/cabinet.png", (15.5, 31.7)))
        add_sprite(SpriteObject(game, "resources/textures/table.png", (15.7, 9.3), scale = 0.8, shift=0.38))
        add_sprite(SpriteObject(game, "resources/textures/table.png", (32.3, 14.3), scale = 0.8, shift=0.38))
        add_sprite(SpriteObject(game, "resources/textures/cabinet.png", (40.7, 4.3)))
        add_sprite(SpriteObject(game, "resources/textures/table.png", (67.7, 5.5), scale = 0.8, shift=0.38))
        add_sprite(SpriteObject(game, "resources/textures/cabinet.png", (67.7, 4.5)))
        add_sprite(SpriteObject(game, "resources/textures/table.png", (27.3, 1.3), scale = 0.8, shift=0.38))
        add_sprite(SpriteObject(game, "resources/textures/cabinet.png", (67.7, 17.3)))

        # Add NPCs
        add_npc(NPC(game))

    def update(self):
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()
            self.distance_stat_transfer = npc.distance_between    

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)