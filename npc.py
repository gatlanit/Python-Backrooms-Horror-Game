from sprite_object import *
import pygame
import random as rand
from sounds import *

class NPC(SpriteObject):
    def __init__(self, game, path="resources/sprites/npc/monster/monster.png", pos=(ENEMEY_POS),
                 scale = 1.75, shift = 0):
        super().__init__(game, path, pos, scale, shift)

        self.attack_dist = 0.8
        self.speed = ENEMY_SPEED
        self.size = 15
        self.attack_damage = 50
        self.ray_cast_value = False
        self.alive = True
        self.serach_player = False
        self.keep_searching_frame = 500
        self.roaring = False # for the roar mechanic
        self.moving = False
        self.current_target = None # Checks if the NPC has a goal to go towards
        self.distance_between = 0
        
    def update(self):
        if ENEMY_SPAWN:
            self.get_sprite()
            self.run_logic()
            self.dist_vol_check()
            if TOPDOWN:
                self.draw_ray_cast()

    def check_wall(self, x, y): # if a coordinate is not in a wall
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collisions(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def move(self):
        if not self.moving: # Makes sure the audio is playing only once and not overlaping
            self.moving = True
            if AUDIO:
                self.game.sound.stomps.play(-1)
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        if TOPDOWN:
            pygame.draw.rect(self.game.screen, "blue", (100 * next_x, 100 * next_y, 100, 100))
        
        angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_wall_collisions(dx, dy)

    def roam(self):
        if not self.moving: # Makes sure the audio is playing only once and not overlaping
            self.moving = True
            if AUDIO:
                self.game.sound.stomps.play(-1)
        
        if self.current_target is None or self.map_pos == self.current_target:
            # If there's no current target or the NPC has reached the current target, choose a new random spot
            rand_spot = rand.choice(list(self.game.map.open_map.keys()))
            self.current_target = rand_spot
        else:
            rand_spot = self.current_target

        next_pos = self.game.pathfinding.get_path(self.map_pos, rand_spot)
        next_x, next_y = next_pos

        if TOPDOWN:
            pygame.draw.rect(self.game.screen, "blue", (100 * next_x, 100 * next_y, 100, 100))
        
        angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
        dx = math.cos(angle) * self.speed
        dy = math.sin(angle) * self.speed
        self.check_wall_collisions(dx, dy)

    def attack(self):
        if self.game.player.alive:
            self.game.player.alive = False

    def run_logic(self):
        if self.alive and not self.game.win:
            self.ray_cast_value = self.ray_cast_player_npc()
            
            if self.ray_cast_value: # If looking at player
                self.serach_player = True

                if not self.roaring and AUDIO: # Makes sure the audio is playing only once and not overlaping
                    self.roaring = True
                    self.game.sound.roar.play(-1)
                
                self.keep_searching_frame = 500
                
                if self.dist < self.attack_dist:
                    self.attack()
                else:
                    self.move()
            
            elif self.serach_player and self.keep_searching_frame >= 0: # Else, continues following for a short time.
                self.move()
                self.keep_searching_frame -= 1

            else:
                self.serach_player = False
                self.roaring = False
                self.game.sound.roar.stop()
                self.roam()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    @property
    def pos(self):
        return self.x, self.y

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True
        
        wall_distance_v, wall_distance_h = 0,0
        player_distance_v, player_distance_h = 0,0

        px, py = self.game.player.pos
        mx, my = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # Horizontal intersections
        y_hor, dy = (my + 1, 1) if sin_a > 0 else (my - 1e-6, -1) # Solve for first intersection, Substracting a small number in order to make it check the left tile and not the right

        depth_hor = (y_hor - py) / sin_a
        x_hor = px + depth_hor * cos_a

        delta_depth = dy / sin_a # Solve for the second intersection (Hypotenuse)
        dx = delta_depth * cos_a # Solve for leg (dx)

        # Move the ray horizontal intersections at (dx) increments and (dy) oincrements until i = MAX_DEPTH
        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_distance_h = depth_hor
                break
            if tile_hor in self.game.map.world_map:
                wall_distance_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # Vertical intersections
        x_vert, dx = (mx + 1, 1) if cos_a > 0 else (mx - 1e-6, -1) # Solve for first intersection

        depth_vert = (x_vert - px) / cos_a
        y_vert = py + depth_vert * sin_a

        delta_depth = dx / cos_a # Solve for the second intersection (Hypotenuse)
        dy = delta_depth * sin_a # Solve for leg (dx)

        # Move the ray vertical intersections at (dx) increments and (dy) increments until i = MAX_DEPTH
        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_distance_v = depth_vert
                break
            if tile_vert in self.game.map.world_map:
                wall_distance_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth 

        player_dist = max(player_distance_h, player_distance_v)
        wall_dist = max(wall_distance_h, wall_distance_v)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        return False
    
    def draw_ray_cast(self):
        pygame.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_player_npc():
            pygame.draw.line(self.game.screen, "orange", (100 * self.game.player.x, 100 * self.game.player.y),
                            (100 * self.x, 100 * self.y), 2)
            
    def dist_vol_check(self):
        # Checks distance of the enemy from player and adjusts audio accordingly
        x1, y1 = self.pos # Enemy
        x2, y2 = self.game.player.pos # Player
        self.distance_between = math.sqrt((x2-x1) ** 2 + (y2-y1) ** 2)
        
        if self.distance_between < 10:
            self.game.sound.roar.set_volume(1)
            self.game.sound.stomps.set_volume(1)
        elif self.distance_between < 15:
            self.game.sound.roar.set_volume(0.75)
            self.game.sound.stomps.set_volume(0.75)
        elif self.distance_between < 20:
            self.game.sound.roar.set_volume(0.50)
            self.game.sound.stomps.set_volume(0.50)
        elif self.distance_between < 25:
            self.game.sound.roar.set_volume(0.25)
            self.game.sound.stomps.set_volume(0.25)
        else:
            self.game.sound.roar.set_volume(0.1)
            self.game.sound.stomps.set_volume(0)