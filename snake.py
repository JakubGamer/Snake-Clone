from distutils.command.build_scripts import first_line_re
from enum import Enum, auto
from dataclasses import dataclass
from typing import Tuple
from collections.abc import Generator
import pygame
from structures import Vec2

class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def to_vec2(self):
        if self == Direction.UP:
            return Vec2(0, -1)
        if self == Direction.DOWN:
            return Vec2(0, 1)
        if self == Direction.LEFT:
            return Vec2(-1, 0)
        if self == Direction.RIGHT:
            return Vec2(1, 0)

def get_chunk_radius(chunk_num):
    return 1 / (chunk_num / 10 + 1)

class SnakeLine: ...

@dataclass
class SnakeLine:
    direction: Direction
    length: int
    next_line: SnakeLine | None

class Snake:
    head_position: Vec2
    color: pygame.Color | Tuple[int, int, int]
    first_line: SnakeLine
    next_step_dir: Direction

    def __init__(self, head_position: Vec2, color: pygame.Color | Tuple[int, int, int], first_line: SnakeLine):
        self.head_position = head_position
        self.color = color
        self.first_line = first_line
        self.next_step_dir = None
    
    def __iter__(self) -> Generator[SnakeLine]:
        line = self.first_line
        while line is not None:
            yield line
            line = line.next_line

    def step_forward(self):
        last_line = None
        second_last_line = None
        for snake_line in self:
            second_last_line = last_line
            last_line = snake_line
        
        self.cut_tail(last_line, second_last_line)
        
        if self.next_step_dir is not None:
            self.first_line = SnakeLine(self.next_step_dir, 1, self.first_line)
            self.head_position += self.next_step_dir.to_vec2()
            self.next_step_dir = None
        else:
            self.head_position += self.first_line.direction.to_vec2()

            self.first_line.length += 1

    def cut_tail(self, last_line, second_last_line):
        last_line.length -= 1
        if last_line.length == 0:
            second_last_line.next_line = None

# @dataclass
# class Snake:
#     head_position: Vec2
#     color: pygame.Color | Tuple[int, int, int]
#     first_line: SnakeLine
#     next_step_dir: Direction = None

#     def __iter__(self) -> Generator[SnakeLine]:
#         line = self.first_line
#         while line is not None:
#             yield line
#             line = line.next_line

#     def step_forward(self):
#         last_line = None
#         second_last_line = None
#         for snake_line in self:
#             second_last_line = last_line
#             last_line = snake_line
        
#         self.cut_tail(last_line, second_last_line)

#         if self.next_step_dir is not None:
#             self.first_line = SnakeLine(Direction.next_step_dir, 1, self.first_line)
#             self.next_step_dir = None
#         else:
#             self.head_position += self.first_line.direction.to_vec2()

#             self.first_line.length += 1

#     def cut_tail(self, last_line, second_last_line):
#         last_line.length -= 1
#         if last_line.length == 0:
#             second_last_line.next_line = None

