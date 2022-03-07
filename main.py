import pygame
import sys

from grid import Grid
from snake import Direction, Snake, SnakeLine
from structures import Vec2, Rect
from gui import Gui
from tilemap import Tilemap

from draw import draw_positions

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake")
    
    tiles_x = 60
    tiles_y = 30

    gui = Gui(tiles_x=[1, True, 15], tiles_y=[1, True, 15])
    snake = Snake(Vec2(5, 5), (73, 185, 230), SnakeLine(Direction.UP, 4, SnakeLine(Direction.RIGHT, 4, SnakeLine(Direction.DOWN, 5, None))))
    tilemap = Tilemap("images/tilemap.png", Vec2(16, 16))
    floor_tiles = (tilemap[0][0], tilemap[0][1])
    time_since_move = 0

    while True:
        delta_time = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gui.on_mouse_down(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                gui.on_mouse_up()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.next_step_dir = Direction.RIGHT
                elif event.key == pygame.K_LEFT:
                    snake.next_step_dir = Direction.LEFT
                elif event.key == pygame.K_UP:
                    snake.next_step_dir = Direction.UP
                elif event.key == pygame.K_DOWN:
                    snake.next_step_dir = Direction.DOWN
        
        time_since_move += delta_time
        move_interval = 500
        if time_since_move > move_interval:
            snake.step_forward()

            time_since_move %= move_interval
        mouse_pos = pygame.mouse.get_pos()

        gui.update(mouse_pos)
        
        grid = Grid(Vec2(gui.tiles_x, gui.tiles_y), floor_tiles)

        screen.fill((83, 173, 71))
        grid_rect = grid.draw(screen)
        grid.draw_snake(screen, grid_rect, snake)
        gui.draw(screen)

        pygame.display.update()
