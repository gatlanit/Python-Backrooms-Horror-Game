import pygame
import math 
from settings import *

"""
Raycasting in a nutshell

We get the player coordinates (where the player is inside of a tile) and the map coordinates (what tile the player is in)
When we find the player's sin and cos of the angle of the ray (first ray is always half of the fov on the left side so that we can increment with delta_angle)

HORIZONTALS:
    For horizontal intersections, if the sin > 0 (player facing down),
    we add one to the y_vert with my + 1 since we know that the first horizontal y_coordinate is going to be one greater than than the map y since we know that the intersection is going to be down one (pygame treats down as postive) and we make dy = 1 since we know thats going to be constant,
    otherwise if sin > 0 (facing up) we substract a small number from y_vert since we want the top tile, then we make dy = -1 since its going up (again pygame treats downwards as postitive)

    We find the distance between the player and the first intersection using depth_hor using trig functions to find the distance between the player and the first intersection in the horizontal lines (depth_hor)
    Then we find out how much it travels in the x axis each time we get another horizontal intersection (dx)

    Finally we loop for however long the render_distance is (MAX_DEPTH):
        In this loop we...
            Find the tile of the horizontal intersection (tile_hor = int(x_vert, y_vert))
            Check if this is inside of the wall inside of self.game.map.world_map, 
                which we then break if this is true
            Otherwise we keep going increenting by the dx and dy value, then incrementing the length of the entire hypotenuse (depth_hor) by how long we know each icrement will be (delta_depths)

VERTICALS:
    For vertical intersections, if the cos > 0 (player facing right), 
    we add one to the x_vert with mx since we know that the first vertical x_coordinate intersection is going to be mx + 1 and dx is going to be 1 because we know that in each intersection is going to be 1 away, 
    otherwise if cos < 0 (facing left) we subtract a small amount to check the tile on the left and make dx = -1 since the next intersection in the x_coordinate is going to be -1 each time.

    We find the distance between the player and the first intersection using depth_vert and trig functions which solve for the hypotenuse (depth_vert).
    Then we find how much it travels in the y axis each time we get another vertical intersection (dy)

    Finally we loop for however long the render_distance is (MAX_DEPTH):
        In this loop we...
            Find the tile of the vertical intersection
            Check if its inside of a wall 
                (If it is we break and thats how long the ray will be)

            Otherwise we keep going by incrementing by the dx and dy value, then incrementing the length of the entire hyptonuse (depth_vert) by how long we know each increment will be (delta_depth)

    After all this we check if the horizontal or the vertical intersection is closer to the player and render the closeest one by setting the depth = to closest intersection
"""


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE)
                wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        px, py = self.game.player.pos
        mx, my = self.game.player.map_pos

        texture_vert, texture_hor = 1,1

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001 # First ray (left most)
        for ray in range(NUM_RAYS):
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
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
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
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth 

            # Pick the intersection that is closest to the player (between the vertical and horizontal intersections
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fish bowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # # Draw rays
            # pygame.draw.line(self.game.screen, "yellow", (100 * px, 100 * py), 
            #                 (100 * px + 100 * depth * cos_a, 100 * py + 100 * depth * sin_a), 2)
                
            # Project as psuedo 3D

            proj_height = SCREEN_DIST / (depth + 0.0001)

            # Ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            # color =[255 / (1 + depth ** 5 * 0.00002)] * 3 # Add "fog"
            # pygame.draw.rect(self.game.screen, color,
            #                 (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))


            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()