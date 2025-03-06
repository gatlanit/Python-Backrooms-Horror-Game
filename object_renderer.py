import pygame
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()

    def draw(self):
        self.draw_background()
        self.render_game_objects()

    def draw_background(self):
        pygame.draw.rect(self.screen, FLOOR_COLOR, (0, 0, WIDTH, HEIGHT)) # Floor
        pygame.draw.rect(self.screen, CEILING_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT)) # Ceiling

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res =  (TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture("resources/textures/0.png"), # regular wall
            2: self.get_texture("resources/textures/1.png"), # Drawing
            3: self.get_texture("resources/textures/2.png"), # Exit
            4: self.get_texture("resources/textures/3.png"), # Black simple
            5: self.get_texture("resources/textures/4.png"), # Red complex
            6: self.get_texture("resources/textures/5.png"), # Black complex
            7: self.get_texture("resources/textures/6.png"), # Red simple
        }
