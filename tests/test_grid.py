import pytest
from pprint import pprint


@pytest.fixture
def five_grid():
    from example import make_grid
    return make_grid(5, 5)


@pytest.mark.parametrize(("x", "y", "expected"), [
    (12, 23, (12, 23)),
    (4, 5, (4, 5)),
])
def test_create_grid(x, y, expected):
    from example import make_grid
    grid = make_grid(x, y)
    assert expected == (len(grid[0]), len(grid))


def test_position_tile(five_grid):
    from example import position_tile, Position, make_tile
    position = Position(2, 3)
    tile = make_tile('ship', position)
    grid = position_tile(five_grid, tile, position)
    assert grid[3][2] == tile


@pytest.mark.parametrize(("position", "x", "y"), [
    ((6, 10), 4, 4),
    ((-6, -10), 0, 0),
])
def test_cannot_position_tile_beyond_grid(position, x, y):
    from example import position_tile, Position, make_tile, make_grid
    grid = make_grid(5, 5)
    position = Position(*position)
    tile = make_tile('ship', position)
    grid = position_tile(grid, tile, position)
    assert grid[y][x] == tile


def test_ship_placement():
    from example import get_ship_placements
    input_ = u'(0, 0, N) (12, 4, W)'
    output = get_ship_placements(input_)
    assert len(output) == 3

