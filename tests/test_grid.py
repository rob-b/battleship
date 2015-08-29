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
    assert grid[1][2] == tile


@pytest.mark.parametrize(("position", "x", "y"), [
    ((6, 10), 4, 0),
    ((-6, -10), 0, 4),
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


@pytest.mark.parametrize(("movement", "expected"), [
    (u'MRMLMM', [(0, 1), (1, 0), (0, 1), (0, 1)]),
])
def test_convert_movement_to_coords(movement, expected):
    from example import get_coords_from_movements
    assert get_coords_from_movements(movement) == expected


@pytest.mark.parametrize(("current", "angle", "new"), [
    (u'N', u'R', u'E'),
    (u'N', u'L', u'W'),
    (u'S', u'L', u'E'),
    (u'S', u'R', u'W'),
    (u'E', u'L', u'N'),
    (u'E', u'R', u'S'),
    (u'W', u'L', u'S'),
    (u'W', u'R', u'N'),
])
def test_rotate(current, angle, new):
    from example import rotate
    assert rotate(current, angle) == new


@pytest.mark.parametrize(("old", "new", "expected"), [
    ((10, 12), (7, 4), (17, 16)),
    ((10, 8), (-7, 0), (3, 8)),
])
def test_change_position(old, new, expected):
    from example import Position, change_position
    pos = Position(*old)
    new_pos = change_position(pos, new)
    assert (new_pos.x, new_pos.y) == expected


def test_final_standings(five_grid):
    from example import Position, make_tile, position_tile, final_standings
    position = Position(2, 3)
    tile = make_tile('ship', position, direction=u'E')
    grid = position_tile(five_grid, tile, position)

    result = final_standings(grid)
    assert result == u'(2, 3, E)'
