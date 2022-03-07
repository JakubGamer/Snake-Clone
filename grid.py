from turtle import color
import pygame
from structures import Vec2, Rect
from snake import Direction, get_chunk_radius
from draw import draw_positions

MARGIN = Vec2(40, 40)

def calculate_position(grid_position, tile_size, tile_x, tile_y):
    return tile_size * Vec2(tile_x, tile_y) + grid_position

# calculate integer size of tile
def calculate_size(grid_position, tile_size, tile_x, tile_y, tile_position):
    next_tile_position = calculate_position(grid_position, tile_size, tile_x + 1, tile_y + 1)
    return Vec2(map(int, next_tile_position)) - Vec2(map(int, tile_position))

def calculate_rect(grid_position, tile_size, tile_x, tile_y):
    position = calculate_position(grid_position, tile_size, tile_x, tile_y)
    size = calculate_size(grid_position, tile_size, tile_x, tile_y, position)

    return Rect(position, size)

class Grid:
    def __init__(self, tile_dimensions, tile_images):
        self.tile_dimensions = tile_dimensions
        self.tile_images = tile_images
        
    def draw_at(self, screen, grid_rect):
        grid_position, grid_size = grid_rect.partition()

        tile_size = grid_size / self.tile_dimensions

        for tile_x in range(self.tile_dimensions.x):
            for tile_y in range(self.tile_dimensions.y):
                calced_pos, calced_size = calculate_rect(grid_position, tile_size, tile_x, tile_y).partition()

                if (tile_x + tile_y) % 2 == 0:
                    screen.blit(pygame.transform.scale(self.tile_images[0], tuple(calced_size)), tuple(calced_pos))
                    # pygame.draw.rect(screen, (255, 255, 255), tuple(calculated_rect))
                else:
                    screen.blit(pygame.transform.scale(self.tile_images[1], tuple(calced_size)), tuple(calced_pos))
                    # pygame.draw.rect(screen, (220, 220, 220), tuple(calculated_rect))

    def draw(self, screen):
        available_width, available_height = Vec2(screen.get_size()) - MARGIN * 2
        available_aspect_ratio = available_height / available_width
        grid_aspect_ratio = self.tile_dimensions.y / self.tile_dimensions.x
        
        draw_height = None
        draw_width = None


        if grid_aspect_ratio > available_aspect_ratio:
            draw_height = available_height
            draw_width = available_height / grid_aspect_ratio
        else:
            draw_width = available_width
            draw_height = available_width * grid_aspect_ratio
        
        offset_x = (available_width - draw_width) / 2 + MARGIN.x
        offset_y = (available_height - draw_height) / 2 + MARGIN.y

        result_rect = Rect(offset_x, offset_y, draw_width, draw_height)
        self.draw_at(screen, result_rect)

        return result_rect
    
    def draw_snake(self, screen, grid_rect, snake):
        positions_to_draw = []
        grid_pos, grid_size = grid_rect.partition()
        tile_size = grid_size / self.tile_dimensions
        counter = 0
        base_coordinate = snake.head_position

        for snake_line in snake:
            for _ in range(snake_line.length):
                base_coordinate -= snake_line.direction.to_vec2()
                position, size = calculate_rect(grid_pos, tile_size, base_coordinate.x, base_coordinate.y).partition()
                radius_factor = get_chunk_radius(counter)
                position += size / 2

                positions_to_draw.append((position, radius_factor / 2 * tile_size.x))
                counter += 1
        
        draw_positions(screen, positions_to_draw, snake.color)

        # for chunk_coord in snake:
        #     position, size = calculate_rect(grid_pos, tile_size, chunk_coord.x, chunk_coord.y).partition()
        #     radius_factor = get_chunk_radius(counter)
        #     position += size / 2

        #     positions_to_draw.append((position, radius_factor / 2 * tile_size.x))
        #     counter += 1

        # draw_positions(screen, positions_to_draw, snake.color)