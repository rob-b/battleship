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


@pytest.mark.parametrize(("position_string", "tile_count"), [
    (u'(10, 10, S) (0,0, W)', 2),
    (u'(10, 10, S) (0,0, W) (0,0, W) (0,0, W) (0,0, W)', 5),
    (u'', 0),
    (u'(10, 10, SW) (-10, 0, W)', 0),
])
def test_ship_placement(position_string, tile_count):
    from example import get_ship_placements
    output = get_ship_placements(position_string)
    assert len(output) == tile_count


@pytest.mark.parametrize(("action_string", "action_kind"), [
    (u'(0, 0) MRMLMM', u'movement'),
    (u'(9, 2)', u'shot'),
])
def test_ship_action(action_string, action_kind):
    from example import get_ship_action
    result = get_ship_action(action_string)
    assert action_kind == result['action']
