# coding=utf-8

import re
import sys
import operator
import functools
from pprint import pprint


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return u'{}x{}'.format(self.x, self.y)

    @property
    def as_tuple(self):
        return (self.x, self.y)

    def __eq__(self, other):
        return self.as_tuple == other.as_tuple


class Empty(object):
    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return u'___'


class Ship(object):
    def __init__(self, position, direction=u'N'):
        self.position = position
        self.direction = direction
        self.sunk = False

    def __repr__(self):
        delim = u'\{}/' if self.sunk else u'_{}_'
        return delim.format(self.direction)

    @property
    def position_tuple(self):
        return self.position.as_tuple

    def sink(self):
        self.sunk = True


def make_tile(kind, position, **extra):
    kind = kind.title()
    kinds = {'Empty': Empty, 'Ship': Ship}
    assert kind in kinds
    cls = kinds[kind]
    return cls(position=position, **extra)


def make_ship(s):
    args = str_to_pos_args(s)
    return make_tile('ship', Position(*args[:2]), direction=args[2])


def shoot_at_ship(ship, shot_position):
    if ship.position == shot_position:
        ship.sink()


def make_grid(x, y):
    return [[make_tile('empty', Position(x1, y1)) for x1 in range(x)] for y1 in range(y)][::-1]


def position_tile(grid, tile, position):
    # ensure that the x and y coords don't exceed the grid dimensions
    grid = grid[::-1]
    y = max(min(len(grid) - 1, position.y), 0)
    x = max(min(len(grid[y]) - 1, position.x), 0)
    grid[y][x] = tile
    tile.position.x = x
    tile.position.y = y
    return grid[::-1]


ws_regex = re.compile(r'\s{1,}')
bracket_regex = re.compile(r'\((\d+,\d+,(?:N|S|E|W))\)')
action_regex = re.compile(r'\((\d+,\d+)\)((?:M|L|R){1,})?')


def no_whitespace(fn):
    @functools.wraps(fn)
    def inner(st):
        return fn(ws_regex.sub('', st))
    return inner


def str_to_pos_args(x):
    tmp_ = x.split(',')
    return map(int, tmp_[:2]) + tmp_[2:]


@no_whitespace
def get_ship_placements(s):
    m = bracket_regex.findall(s)
    return [make_ship(x) for x in m]


@no_whitespace
def get_ship_action(s):
    m = action_regex.match(s)
    if not m:
        return {}
    target, movements = m.groups()
    pos = Position(*map(int, target.split(',')))
    return {'position': pos,
            'action': 'shot' if movements is None else 'movement',
            'movements': movements or ''}


def rotate(direction, rotate):
    directions = {'N': ['W', 'E'],
                  'W': ['S', 'N'],
                  'S': ['E', 'W'],
                  'E': ['N', 'S']}
    index = 0 if rotate == 'L' else 1
    return directions[direction][index]


def get_coords_from_movements(movements, direction='N'):
    changes = []
    for c in movements:
        if c in ['L', 'R']:
            direction = rotate(direction, c)
            continue
        if direction == 'N':
            change = (0, 1)
        elif direction == 'S':
            change = (0, -1)
        elif direction == 'W':
            change = (-1, 0)
        else:
            change = (1, 0)
        changes.append(change)
    return changes


def change_position(position, change):
    x, y = position.x, position.y
    return Position(*[operator.add(*pair) for pair in zip((x, y), change)])


def add_tuples(a, b):
    return tuple([operator.add(*pair) for pair in zip(a, b)])


def get_tile_from_grid(grid, target):
    return grid[::-1][target.y][target.x]


def final_standings(grid):
    retval = []
    for yindex, y in enumerate(grid[::-1]):
        for xindex, tile in enumerate(y):
            if not isinstance(tile, Ship):
                continue
            args = [xindex,
                    yindex,
                    tile.direction,
                    ' SUNK' if tile.sunk else '']
            retval.append('({}, {}, {}){}'.format(*args))
    return '\n'.join(retval[::-1])
