from copy import copy
import pygame

pygame.init()

from structures import Vec2

def get_perpendicular_vector(vec):
    return Vec2(vec.y, -vec.x)

def get_line_corners(start_pos, end_pos, start_radius, end_radius):
    perpendicular = get_perpendicular_vector(end_pos - start_pos).unit()
    points = [
        start_pos + perpendicular * start_radius,
        start_pos - perpendicular * start_radius,
        end_pos - perpendicular * end_radius,
        end_pos + perpendicular * end_radius,
    ]
    return points

def draw_positions(screen, positions_radii, color):
    previous = positions_radii[0]
    pygame.draw.circle(screen, color, tuple(previous[0]), previous[1])
    
    for (pos, radius) in positions_radii[1:]:
        prev_pos, prev_radius = previous
        
        points = get_line_corners(prev_pos, pos, prev_radius, radius)
        pygame.draw.polygon(screen, color, tuple(map(tuple, points)))
        pygame.draw.circle(screen, color, tuple(pos), radius)

        previous = (pos, radius)
