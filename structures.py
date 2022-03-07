import operator
import math
from collections.abc import Iterator, Iterable

class Vec2:
    def __init__(self, x: float | int, y: float | int = None):
        # could be iterator
        if isinstance(x, Iterator):
            self.x = next(x)
            self.y = next(x)
            return
        elif isinstance(x, Iterable):
            x_iter = iter(x)
            self.x = next(x_iter)
            self.y = next(x_iter)
            return
            
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(map(operator.add, self, other))

    def __sub__(self, other):
        return Vec2(map(operator.sub, self, other))

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return Vec2(map(operator.mul, self, other))
        else:
            return Vec2(self.x * other, self.y * other)
    
    def __truediv__(self, other):
        if isinstance(other, Vec2):
            return Vec2(map(operator.truediv, self, other))
        else:
            return Vec2(self.x / other, self.y / other)
    
    def __floordiv__(self, other):
        if isinstance(other, Vec2):
            return Vec2(map(operator.floordiv, self, other))
        else:
            return Vec2(self.x // other, self.y // other)
    
    def __mod__(self, other):
        return Vec2(map(operator.mod, self, other))

    def __iter__(self):
        return [self.x, self.y].__iter__()

    def __str__(self):
        return f"Vec2({self.x}, {self.y})"
    
    def __repr__(self):
        return self.__str__()
    
    def __neg__(self):
        return Vec2(map(operator.neg, self))
    
    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def unit(self):
        return self / self.magnitude()

    @property
    def yx(self):
        return Vec2(self.y, self.x)
    
    @yx.setter
    def yx(self, value):
        self.x = value.y
        self.y = value.x

class Rect:
    def __init__(self, pos_x, pos_y = None, width = None, height = None):
        if isinstance(pos_x, Iterable):
            if isinstance(pos_y, Iterable):
                self.position = Vec2(pos_x)
                self.size = Vec2(pos_y)
            else:
                pos_x_iter = iter(pos_x)
                self.position = Vec2(next(pos_x_iter), next(pos_x_iter))
                self.size = Vec2(next(pos_x_iter), next(pos_x_iter))
            return            

        self.position = Vec2(pos_x, pos_y)
        self.size = Vec2(width, height)
    
    def __iter__(self):
        return [self.position.x, self.position.y, self.size.x, self.size.y].__iter__()

    def __str__(self):
        return f"Rect(position={self.position}, size={self.size})"
    
    def partition(self):
        return self.position, self.size