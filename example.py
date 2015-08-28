class Position(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return u'{}x{}'.format(self.x, self.y)


class Tile(object):
    def __init__(self, kind, position):
        self.kind = kind
        self.position = position

    def __repr__(self):
        return u'<{} {}>'.format(self.kind, self.position)


def make_tile(kind, position):
    kind = kind.title()
    assert kind in ('Empty', 'Ship')
    return Tile(kind, position=position)


def make_grid(x, y):
    return [[make_tile('empty', Position(x1, y1)) for x1 in range(x)] for y1 in range(y)]


def position_tile(grid, tile, position):
    # ensure that the x and y coords don't exceed the grid dimensions
    y = max(min(len(grid) - 1, position.y), 0)
    x = max(min(len(grid[y]) - 1, position.x), 0)
    grid[y][x] = tile
    return grid


def get_ship_placements(s):
    pass
