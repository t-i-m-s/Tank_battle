import sys
import math
import random
from math import pi
import pygame as pg


class Tank:
    gun_w, gun_h = 2, 14
    turret_w, turret_h = 8, 12
    turret_surf_w = turret_w
    turret_surf_h = 2*(turret_h/2 + gun_h)
    gun_color = 255, 255, 255, 255
    turret_color = 255, 255, 255, 255

    body_w, body_h = 14, 24
    body_surf_size = turret_surf_h if turret_surf_h > turret_surf_w else turret_surf_w
    front_w, front_h = 6, 2
    body_color = 255, 0, 0, 255

    _turret_surf: pg.Surface
    _body_surf: pg.Surface
    speed = 5
    turret_rot_angle = 360/12
    turret_current_angle = 0
    body_rot_angle = 360/12
    body_current_angle = 0

    def __init__(self, main_surf: pg.Surface, x, y):
        self.x = x
        self.y = y
        self.main_surf = main_surf
        self.turret_surf = pg.Surface((self.turret_surf_w, self.turret_surf_h), pg.SRCALPHA)
        self.body_surf = pg.Surface((self.body_surf_size, self.body_surf_size), pg.SRCALPHA)
        gun = pg.Rect(self.turret_surf.get_width()/2 - self.gun_w/2, 0, self.gun_w, self.gun_h)
        turret = pg.Rect(0, self.turret_surf.get_height()/2 - self.turret_h/2, self.turret_w, self.turret_h)
        body = pg.Rect(self.body_surf.get_width()/2 - self.body_w/2, self.body_surf.get_height()/2 - self.body_h/2, self.body_w, self.body_h)
        front = pg.Rect(self.body_surf.get_width() / 2 - self.front_w / 2, body.y, self.front_w, self.front_h)

        pg.draw.rect(self.turret_surf, self.gun_color, gun)
        pg.draw.rect(self.turret_surf, self.turret_color, turret)
        pg.draw.rect(self.body_surf, self.body_color, body)
        pg.draw.rect(self.body_surf, (0, 125, 255), front)

        self._turret_surf = self.turret_surf.copy()
        self._body_surf = self.body_surf.copy()

    def rotate_turret(self, clockwise=False):
        if clockwise:
            self.turret_current_angle -= self.turret_rot_angle
        else:
            self.turret_current_angle += self.turret_rot_angle
        self.turret_current_angle %= 360
        self._turret_surf = pg.transform.rotate(self.turret_surf,
                                                self.turret_current_angle)

    def rotate_body(self, clockwise=False):
        if clockwise:
            self.body_current_angle -= self.body_rot_angle
        else:
            self.body_current_angle += self.body_rot_angle
        self.body_current_angle %= 360
        self._body_surf = pg.transform.rotate(self.body_surf,
                                              self.body_current_angle)

    @staticmethod
    def _get_cathets(hypot, angle):
        return math.cos(angle)*hypot, math.sin(angle)*hypot

    def _get_xy_move(self):
        visible_angle = (self.body_current_angle + 90)*pi/180
        if 90 >= visible_angle > 0:
            _x, _y = self._get_cathets(self.speed, visible_angle)
            _y = -_y
        elif 180 >= visible_angle > 90:
            _y, _x = self._get_cathets(self.speed, visible_angle % 90)
            _x = -_x
            _y = -_y
        elif 270 >= visible_angle > 180:
            _x, _y = self._get_cathets(self.speed, visible_angle % 90)
            _x = -_x
        else:
            _y, _x = self._get_cathets(self.speed, visible_angle % 90)
        return round(_x), round(_y)

    def move_forward(self, zone_color):
        pxarray = pg.PixelArray(self.main_surf)
        zone = self.main_surf.map_rgb(zone_color)
        _x, _y = self._get_xy_move()
        sw = self.body_surf.get_width()
        sh = self.body_surf.get_height()
        print(zone, "-", pxarray[self.x + _x, self.y + _y])
        next_x = self.x + _x
        next_y = self.y + _y
        if width - self.body_surf.get_width() > next_x > 0:
            if pxarray[next_x, self.y] == zone and pxarray[next_x + sw, self.y] == zone and pxarray[next_x, self.y + sh] == zone and pxarray[next_x + sw, self.y + sh] == zone:
                self.x += _x
        else:
            if self.x + _x < curr_screen_xy[0]:
                print("left")
                add_map_from_on("left", self.main_surf)
                self.x -= self.body_surf
            else:
                print("right")
                add_map_from_on("right", self.main_surf)
                self.x += self.body_surf
        if height - self.body_surf.get_height() > next_y > 0:
            if pxarray[self.x, next_y] == zone and pxarray[self.x + sw, next_y] == zone and pxarray[self.x, next_y + sh] == zone and pxarray[self.x + sw, next_y + sh] == zone:
                self.y += _y
        else:
            if self.y + _y < curr_screen_xy[1]:
                print("top")
                add_map_from_on("top", self.main_surf)
                #  not finished
            else:
                print("bottom")
                add_map_from_on("bottom", self.main_surf)
                #  not finished

    def move_back(self, zone_color):
        pxarray = pg.PixelArray(self.main_surf)
        zone = self.main_surf.map_rgb(zone_color)
        print(zone)
        _x, _y = self._get_xy_move()
        sw = self.body_surf.get_width()
        sh = self.body_surf.get_height()
        next_x = self.x - _x
        next_y = self.y - _y
        if width - self.body_surf.get_width() > next_x > 0:
            if pxarray[next_x, self.y] == zone and pxarray[next_x + sw, self.y] == zone and pxarray[next_x, self.y + sh] == zone and pxarray[next_x + sw, self.y + sh] == zone:
                self.x -= _x
        else:
            print("next zone")
        if height - self.body_surf.get_height() > next_y > 0:
            if pxarray[self.x, next_y] == zone and pxarray[self.x + sw, next_y] == zone and pxarray[self.x, next_y + sh] == zone and pxarray[self.x + sw, next_y + sh] == zone:
                self.y -= _y
        else:
            print("next zone")

    def draw(self):
        _tank: pg.Surface = self._body_surf.copy()
        _tank.blit(self._turret_surf,
                   (_tank.get_width()/2 - self._turret_surf.get_width()/2, _tank.get_height()/2 - self._turret_surf.get_height()/2))
        self.main_surf.blit(_tank, (self.x - (_tank.get_width() - self.body_surf.get_width())/2, self.y - (_tank.get_height() - self.body_surf.get_height())/2))
        del _tank


def create_map(surf: pg.Surface, xy, exits, conn_side):
    if conn_side in ("left", "right"):
        col, row = xy
        _conn_side = tile_dict["top"]
        have_conn_side_row = tile_dict["bottom"]
        if conn_side == "left":
            have_conn_side_col = tile_dict["right"]
        else:
            col += width - tile_size
            have_conn_side_col = tile_dict["left"]
    else:
        row, col = xy
        _conn_side = tile_dict["left"]
        have_conn_side_row = tile_dict["right"]
        if conn_side == "top":
            have_conn_side_col = tile_dict["bottom"]
        else:
            col += height - tile_size
            have_conn_side_col = tile_dict["top"]
    prev_exit = None
    for i, _exit in enumerate(exits[:]):
        if _exit is True:
            tile_kit = tile_dict[conn_side]
        else:
            tile_kit = set()
            for kit in tile_dict.values():
                tile_kit.add(kit - tile_dict[conn_side])

        if prev_exit is True:
            tile_kit &= _conn_side
        else:
            tile_kit -= _conn_side

        _tile: pg.Surface = random.choice(tuple(tile_kit))
        surf.blit(_tile, (col, row))
        row += tile_size
        if _tile in have_conn_side_row:
            prev_exit = True
        else:
            prev_exit = False
        if _tile in have_conn_side_col:
            exits[i] = True
        else:
            exits[i] = False
    if (abs(col) % width) == 0:
        return None
    if conn_side == "left":
        row -= height
        col += tile_size
    elif conn_side == "right":
        row -= height
        col -= tile_size
    elif conn_side == "top":
        row -= width
        col += tile_size
    else:
        row -= width
        col -= tile_size
    create_map(surf, (col, row), exits, conn_side)


def add_map_from_on(side, surf: pg.Surface):
    connect_side: str
    if side == "left":
        curr_screen_xy[0] -= width
        connect_side = "right"
    elif side == "top":
        curr_screen_xy[1] -= height
        connect_side = "bottom"
    elif side == "right":
        curr_screen_xy[0] += width
        connect_side = "left"
    elif side == "bottom":
        curr_screen_xy[1] += height
        connect_side = "top"
    else:
        raise Exception("Invalid side - {}" % side)
    _map = map_tile_dict.get(tuple(curr_screen_xy))
    if _map is not None:
        surf.blit(_map, curr_screen_xy)
    else:
        new_map = pg.Surface((width, height), pg.SRCALPHA)
        exits = side_exits[side]
        create_map(new_map, curr_screen_xy, exits, connect_side)
        map_tile_dict[tuple(curr_screen_xy)] = new_map
        surf.blit(new_map, curr_screen_xy)


pg.init()

BLACK = 0, 0, 0
GREEN = 0, 255, 0
ROAD = 74, 74, 74
FRAMERATE = 30
clock = pg.time.Clock()

tile_size = 128
size = width, height = 5*tile_size, 5*tile_size
screen = pg.display.set_mode(size)
tile1 = pg.transform.scale2x(pg.image.load("./map_1/1.png"))
tile2 = pg.transform.scale2x(pg.image.load("./map_1/2.png"))
tile3 = pg.transform.scale2x(pg.image.load("./map_1/3.png"))
tile4 = pg.transform.scale2x(pg.image.load("./map_1/4.png"))
tile5 = pg.transform.scale2x(pg.image.load("./map_1/5.png"))
tile6 = pg.transform.scale2x(pg.image.load("./map_1/6.png"))
tile7 = pg.transform.scale2x(pg.image.load("./map_1/7.png"))
tile8 = pg.transform.scale2x(pg.image.load("./map_1/8.png"))
tile9 = pg.transform.scale2x(pg.image.load("./map_1/9.png"))
tile10 = pg.transform.scale2x(pg.image.load("./map_1/10.png"))
tile11 = pg.transform.scale2x(pg.image.load("./map_1/11.png"))
tile_dict = {
    "top": {tile5, tile6, tile7, tile8, tile9, tile10, tile11},
    "left": {tile2, tile3, tile4, tile6, tile7, tile9, tile10},
    "right": {tile5, tile1, tile2, tile3, tile6, tile8, tile9},
    "bottom": {tile5, tile1, tile3, tile4, tile6, tile7, tile11}
}
map_tile_dict = {}
side_exits = {
    "top": [False, False, True, False, False],
    "left": [False, False, True, False, False],
    "right": [False, False, True, False, False],
    "bottom": [False, False, True, False, False]
}

main_tile = screen.copy()

main_tile.blit(tile1, (0, 0))
main_tile.blit(tile2, (128, 0))
main_tile.blit(tile6, (128 * 2, 0))
main_tile.blit(tile2, (128 * 3, 0))
main_tile.blit(tile4, (128 * 4, 0))

main_tile.blit(tile11, (0, 128))
main_tile.blit(tile11, (128 * 2, 128))
main_tile.blit(tile11, (128 * 4, 128))

main_tile.blit(tile6, (0, 128 * 2))
main_tile.blit(tile2, (128, 128 * 2))
main_tile.blit(tile6, (128 * 2, 128 * 2))
main_tile.blit(tile2, (128 * 3, 128 * 2))
main_tile.blit(tile6, (128 * 4, 128 * 2))

main_tile.blit(tile11, (0, 128 * 3))
main_tile.blit(tile11, (128 * 2, 128 * 3))
main_tile.blit(tile11, (128 * 4, 128 * 3))

main_tile.blit(tile8, (0, 128 * 4))
main_tile.blit(tile2, (128, 128 * 4))
main_tile.blit(tile6, (128 * 2, 128 * 4))
main_tile.blit(tile2, (128 * 3, 128 * 4))
main_tile.blit(tile10, (128 * 4, 128 * 4))

curr_screen_xy = [0, 0]
screen.blit(main_tile, curr_screen_xy)
map_tile_dict[tuple(curr_screen_xy)] = main_tile
curr_screen_map = main_tile

tank = Tank(screen, 50, 50)

while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    is_pushed = pg.key.get_pressed()
    if is_pushed[pg.K_w]:
        tank.move_forward((74, 74, 74, 255))  # (74, 74, 74, 255)
    elif is_pushed[pg.K_s]:
        tank.move_back((74, 74, 74, 255))  # (74, 74, 74, 255)
    if is_pushed[pg.K_a]:
        tank.rotate_body()
    elif is_pushed[pg.K_d]:
        tank.rotate_body(clockwise=True)
    if is_pushed[pg.K_UP]:
        tank.rotate_turret()
    elif is_pushed[pg.K_DOWN]:
        tank.rotate_turret(clockwise=True)

    screen.blit(curr_screen_map, curr_screen_xy)
    tank.draw()

    pg.display.flip()
    clock.tick(FRAMERATE)
