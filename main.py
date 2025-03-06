import pygame
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from object_handler import *
from pathfinding import *
from ui import *
from sounds import *

"""

TODO:

    - Comment code for future reference

"""

class Game:
    def __init__(self):
        # init
        pygame.init()
        pygame.mouse.set_visible(False) # turn off cursor
        
        # Screen
        pygame.display.set_caption("Backrooms | Python Edition") # title
        self.screen = pygame.display.set_mode(RES, pygame.FULLSCREEN | pygame.SCALED | pygame.RESIZABLE) # res
        self.icon = pygame.image.load("resources/textures/icon.png").convert_alpha() # load img
        pygame.display.set_icon(self.icon) # icon
        
        # Game
        self.clock = pygame.time.Clock()
        self.delta_time = 1 # for syncing fps
        self.running = False
        self.win = False
        self.new_game()

    def new_game(self): # sets condition of new game to default
        self.win = False
        # Only resets if soudnds was already created
        try:
            self.sound.reset_sounds()
        except:
            pass
        self.map  = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.pathfinding = PathFinding(self)
        self.ui = UI(self)
        self.sound = Sound(self)

    def update(self):
        if self.running:
            self.player.update()
            self.raycasting.update()
            self.object_handler.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(FPS)

    def draw(self):
        if TOPDOWN and self.running:
            self.screen.fill("Black")
            self.map.draw()
            self.player.draw()
        else:
            if self.running:
                self.object_renderer.draw() 
            self.ui.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.QUIT
                exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

game = Game()
game.run()