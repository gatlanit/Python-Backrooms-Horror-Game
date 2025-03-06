import pygame

class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = 'resources/sounds/'
        self.ambiance = pygame.mixer.Sound(self.path + 'ambiance.wav')
        self.roar = pygame.mixer.Sound(self.path + 'roar.wav')
        self.static = pygame.mixer.Sound(self.path + 'static.wav')
        self.stomps = pygame.mixer.Sound(self.path + 'stomps.wav')
        self.footsteps = pygame.mixer.Sound(self.path + 'footsteps.wav')
        self.travel_ui = pygame.mixer.Sound(self.path + 'travel_ui.wav')
        self.select_ui = pygame.mixer.Sound(self.path + 'select_ui.wav')
        pygame.mixer.music.set_volume(0.3)

        self.sounds = [self.ambiance, self.roar, self.static, self.stomps, self.footsteps, self.travel_ui, self.select_ui]

    def reset_sounds(self):
        for sound in self.sounds:
            try:
                sound.stop()
            except:
                pass