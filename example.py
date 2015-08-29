import re


class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return u'{}x{}'.format(self.x, self.y)


class Empty(object):
    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return u'<{} {}>'.format('Empty', self.position)


class Ship(object):
    def __init__(self, position, direction=u'N'):
        self.position = position
        self.direction = direction

    def __repr__(self):
        return u'<{} {}{}>'.format('Ship', self.position, self.direction)


def make_tile(kind, position, **extra):
    kind = kind.title()
    kinds = {'Empty': Empty, 'Ship': Ship}
    assert kind in kinds
    cls = kinds[kind]
    return cls(position=position, **extra)


def make_ship(s):
    args = str_to_pos_args(s)
    return make_tile('ship', Position(*args[:2]), direction=args[2])


def make_grid(x, y):
    return [[make_tile('empty', Position(x1, y1)) for x1 in range(x)] for y1 in range(y)]


def position_tile(grid, tile, position):
    # ensure that the x and y coords don't exceed the grid dimensions
    y = max(min(len(grid) - 1, position.y), 0)
    x = max(min(len(grid[y]) - 1, position.x), 0)
    grid[y][x] = tile
    return grid


ws_regex = re.compile(r'\s{1,}')
bracket_regex = re.compile(r'\((\d+,\d+,(?:N|S|E|W))\)')


def str_to_pos_args(x):
    tmp_ = x.split(',')
    return map(int, tmp_[:2]) + tmp_[2:]


def get_ship_placements(s):
    s = ws_regex.sub('', s)
    m = bracket_regex.findall(s)
    return [make_ship(x) for x in m]
