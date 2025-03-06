import pygame
from settings import *

class UI:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.font = pygame.font.Font(FONT, FONT_SIZE)
        self.font_big = pygame.font.Font(FONT, FONT_SIZE + 64)
        self.done = False
        self.selected_option = 1.5  # Index of the currently selected option
        self.arrow_pressed = False
        self.menu = True
        self.ctrls = False 
        #self.animation_out = True # For animation
        self.fade_alpha = 255  # Initial alpha value for fading
        self.fade_speed = 4  # How much to decrease
        self.theme_play = False

        self.vhs = self.get_texture("resources/textures/VHS.png", RES)
        self.main_menu_img = self.get_texture("resources/textures/main-menu.png", RES)
        self.ctrl_img = self.get_texture("resources/textures/controls.png", RES)

        # Text
        self.dead = self.font_big.render("FOOTAGE CORRUPTED", True, FONT_COLOR)
        self.dead_rect = self.dead.get_rect(center = (HALF_WIDTH, HALF_HEIGHT))

        self.end_txt = self.font_big.render("FOOTAGE RECOVERED", True, "white")
        self.end_rect = self.end_txt.get_rect(center = (HALF_WIDTH, HALF_HEIGHT))

        self.space_to_txt = self.font.render("Press the spacebar to retry", True, FONT_COLOR)
        self.txt_rect = self.space_to_txt.get_rect(center = (HALF_WIDTH, HALF_HEIGHT + 400))
        
        self.space_exit_txt = self.font.render("Press the spacebar to exit", True, "white")
        self.space_exit_rect = self.space_exit_txt.get_rect(center = (HALF_WIDTH, HALF_HEIGHT + 400))

        self.pickup_txt = self.font.render("Press E to pickup the key", True, "white")

        self.already_txt = self.font.render("You already have the key...", True, "white")

        self.need_key_txt = self.font.render("You need a key to unlock the elevator", True, FONT_COLOR)
        self.need_rect = self.need_key_txt.get_rect(center = (HALF_WIDTH, HALF_HEIGHT + 400))

        self.use_txt = self.font.render("Press E to use key", True, "white")
        self.use_rect = self.use_txt.get_rect(center = (HALF_WIDTH, HALF_HEIGHT + 400))

        self.distance_txt = self.font.render("Null", True, "white")
        self.distance_rect = self.distance_txt.get_rect(topleft = (20, 20))

        self.pos_txt = self.font.render("Pos: ", True, "white")
        self.pos_rect = self.pos_txt.get_rect(topright = (WIDTH - 220, 20))

        # Main Menu
        self.title_txt = self.font_big.render("BACKROOMS", True, "white")
        self.title_rect = self.title_txt.get_rect(topleft = (40, 40))

        self.caption = self.font.render("Python Edition", True, "silver")
        self.caption_rect = self.caption.get_rect(topleft = (45,160))

        self.start_txt = self.font.render("START", True, "white")
        self.start_rect = self.start_txt.get_rect(topleft = (40, HEIGHT - 225))

        self.how_txt = self.font.render("HOW TO",  True, "white")
        self.how_rect = self.how_txt.get_rect(topleft = (40, HEIGHT - 150))
        
        self.quit_txt = self.font.render("QUIT", True, "white")
        self.quit_rect = self.quit_txt.get_rect(topleft = (40, HEIGHT - 75))

        self.arrow_txt = self.font.render("<", True, "white")

    @staticmethod
    def get_texture(path, res =  (TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)
    
    def game_over(self):
        if not self.game.player.alive or self.game.win:
            # Sounds
            self.game.sound.roar.stop()
            self.game.sound.ambiance.stop()
            self.game.sound.stomps.stop()
            self.game.sound.footsteps.stop()

            if not self.done:
                self.done = True
                if AUDIO:
                    self.game.sound.static.play(-1)

            if not self.game.player.alive:
                self.screen.blit(self.dead, self.dead_rect)
                self.screen.blit(self.space_to_txt, self.txt_rect)
            
            elif self.game.win:
                self.screen.blit(self.end_txt, self.end_rect)
                self.screen.blit(self.space_exit_txt, self.space_exit_rect)

            pygame.display.flip()
            
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_SPACE]:
                self.fade_alpha = 255
                self.game.sound.static.stop()
                self.game.running = False

    def pickup_item(self):
        if self.game.player.alive and self.game.player.item_pickup() and "Key" not in self.game.player.inventory:
            self.screen.blit(self.pickup_txt, self.txt_rect)

    def use_item(self):
        if self.game.player.alive and self.game.player.use_item() and "Key" in self.game.player.inventory and not self.game.win:
            self.screen.blit(self.use_txt, self.use_rect)
        elif self.game.player.alive and self.game.player.use_item() and "Key" not in self.game.player.inventory and not self.game.win:
            self.screen.blit(self.need_key_txt, self.need_rect)

    def controls(self):
        self.screen.blit(self.main_menu_img, (0,0))
        self.screen.blit(self.ctrl_img, (0,0))
        
        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            if AUDIO:
                self.game.sound.select_ui.play()
            self.ctrls = False
            self.menu = True

    def game_ui(self):
        self.screen.blit(self.vhs, (0,0))
        self.pickup_item() # Check if item is near
        self.use_item() # Check if can use item

        if not DEBUG:
            if self.game.object_handler.distance_stat_transfer > 15:
                self.distance_txt = self.font.render("Entity distance: " + str(self.game.object_handler.distance_stat_transfer.__round__(3)) + " M", True, "white")
            else:
                self.distance_txt = self.font.render("Entity distance: " + str(self.game.object_handler.distance_stat_transfer.__round__(3)) + " M", True, FONT_COLOR)
        else:
            self.distance_txt = self.font.render("FPS: " + str(self.game.clock.get_fps().__round__(3)), True, "white")
            
        for npc in self.game.object_handler.npc_list:
            if npc.serach_player:
                self.screen.blit(self.distance_txt, self.distance_rect)

        self.pos_txt = self.font.render("Pos: " + str(self.game.player.map_pos), True, "white")
        self.screen.blit(self.pos_txt, self.pos_rect)
        self.game_over() # check if game is over

    def main_menu(self):
        self.screen.blit(self.main_menu_img, (0,0))
        self.screen.blit(self.title_txt, self.title_rect)
        self.screen.blit(self.caption, self.caption_rect)

        self.screen.blit(self.start_txt, self.start_rect) # start button
        self.screen.blit(self.how_txt, self.how_rect)
        self.screen.blit(self.quit_txt, self.quit_rect) # quit button
        self.arrow_rect = self.arrow_txt.get_rect(topleft = (240, HEIGHT - 150 * self.selected_option))
        self.screen.blit(self.arrow_txt, self.arrow_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_DOWN]:
            if not self.arrow_pressed:
                if AUDIO:
                    self.game.sound.travel_ui.play()
                self.selected_option -= 0.5
                self.arrow_pressed = True
            if self.selected_option < 0.5:
                if AUDIO:
                    self.game.sound.travel_ui.play()
                self.selected_option = 0.5
        
        if keys[pygame.K_UP]:
            if not self.arrow_pressed:
                if AUDIO:
                    self.game.sound.travel_ui.play()
                self.selected_option += 0.5
                self.arrow_pressed = True
            if self.selected_option > 1.5:
                if AUDIO:
                    self.game.sound.travel_ui.play()
                self.selected_option = 1.5

        if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.arrow_pressed = False

        if keys[pygame.K_RETURN]:
            if self.selected_option == 1.5:  # Start
                if AUDIO:
                    self.game.sound.select_ui.play()
                self.animation_out = False # Switch to fade in animation
                self.game.sound.ambiance.stop()
                self.game.running = True
                self.game.new_game()
                if AUDIO:
                    self.game.sound.ambiance.play(-1)
            
            elif self.selected_option == 1:  # Controls
                if AUDIO:
                    self.game.sound.select_ui.play()
                self.ctrls = True
                self.menu = False
            
            elif self.selected_option == 0.5:  # Quit
                if AUDIO:
                    self.game.sound.select_ui.play()
                pygame.quit()
                exit()

    def fade_out(self):
        self.fade_alpha -= self.fade_speed
        # Draw the fading effect
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.set_alpha(self.fade_alpha)
        self.screen.blit(fade_surface, (0, 0))
        if self.fade_alpha < 0:
            self.fade_alpha = 0
            return True

    def draw(self):
        if self.game.running:
            self.game_ui()
            self.fade_out()
        elif self.menu:
            if not self.theme_play:
                self.theme_play = True
                if AUDIO:
                    self.game.sound.ambiance.play(-1)
            self.main_menu()
            self.fade_out()
        elif self.ctrls:
            self.controls()
            self.fade_out()