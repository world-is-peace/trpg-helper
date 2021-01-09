import pygame.freetype
import os

FONT = 'font.ttf'

MAPS = list()
for root, dirs, files in os.walk('./maps'):
    for file in files:
        if file.find('.txt') == -1:
            MAPS.append('maps/' + file)


class Button:
    def __init__(self, text, size, rgba, pos, t_size, t_rgb, t_pos, act='None', texture=None, cut=-1):
        if texture is None:
            self.surf = pygame.Surface(size)
            self.surf.fill((rgba[0], rgba[1], rgba[2]))
            self.surf.set_alpha(rgba[3])
            self.texture = None
        else:
            self.texture = pygame.image.load(texture)
            self.texture = pygame.transform.scale(self.texture, (size[0], size[1]))
            if text == 'up':
                self.texture = pygame.transform.rotate(self.texture, 180)
            if text == 'left':
                self.texture = pygame.transform.rotate(self.texture, -90)
            if text == 'right':
                self.texture = pygame.transform.rotate(self.texture, 90)
            self.rect = self.texture.get_rect()

            self.surf = pygame.Surface(size)
            self.surf.blit(self.texture, self.rect)

        self.pos = pos
        self.check_rect = pygame.Rect(*pos, *size)

        if len(text) > cut != -1 and act == 'open_map_editor':
            text_tmp = text[:cut - 3] + '...'
        elif len(text) > cut != -1:
            text_tmp = text[:cut]
        else:
            text_tmp = text

        self.title, self.t_rect = pygame.freetype.Font(FONT, t_size).render(text_tmp, t_rgb)
        if t_pos.find('center') > -1:
            self.t_rect = self.title.get_rect(center=(pos[0] + size[0] / 2, pos[1] + size[1] / 2))
        elif t_pos.find('left') > -1:
            self.t_rect.topleft = (pos[0] + 0.01 * size[0], pos[1] + 0.01 * size[1])
        elif t_pos.find('over') > -1:
            self.t_rect = self.title.get_rect(center=(pos[0] + size[0] / 2, pos[1] - t_size * 0.5))
            self.title, tmp = pygame.freetype.Font(FONT, t_size).render(text_tmp, t_rgb, rgba)
        else:
            self.t_rect = self.title.get_rect(center=(pos[0] + size[0] / 2, pos[1] + 0.01 * size[1] + 0.5 * t_size))

        self.act = act
        self.text = text
        self.active = False
        self.text_field = ''

    def draw_rect(self):
        if self.active is True:
            self.surf.fill((175, 255, 255))
        elif self.active is False and self.act == 'set_text_field':
            self.surf.fill((255, 255, 255))
        return [self.surf, self.pos]

    def set_input(self, symbol):
        if symbol == -1:
            self.text_field = self.text_field[:-1]
            self.title, self.t_rect = pygame.freetype.Font(FONT, self.check_rect.height).render(self.text_field,
                                                                                                (0, 0, 0))
            self.t_rect = self.title.get_rect(center=(self.pos[0] + self.check_rect.width / 2,
                                                      self.pos[1] + self.check_rect.height / 2))
            return
        self.text_field += symbol
        self.title, self.t_rect = pygame.freetype.Font(FONT, self.check_rect.height).render(self.text_field, (0, 0, 0))
        self.t_rect = self.title.get_rect(center=(self.pos[0] + self.check_rect.width / 2,
                                                  self.pos[1] + self.check_rect.height / 2))

    def draw_text(self):
        return [self.title, self.t_rect]

    def list_of_orders(self):
        order = 0
        if self.act.find('open') > -1:
            order += 100
            if self.act.find('map_arc') > -1:
                order += 2
            if self.act.find('menu') > -1:
                order += 1
            if self.act.find('map_editor') > -1:
                order += 3
            if self.act.find('new_adventure') > -1:
                order += 4
        elif self.act.find('set') > -1:
            order += 200
            if self.act.find('move') > -1:
                order += 1
            if self.act.find('grid') > -1:
                order += 4
            if self.act.find('text_field') > -1:
                self.active = True
                order += 5
            if self.act.find('new_zone') > -1:
                order += 6
            if self.act.find('map_done') > -1:
                order += 7

        return order

    def acting(self, event):
        if self.check_rect.collidepoint(*event.pos):
            return self.list_of_orders()
        else:
            return 0


class Map:
    def __init__(self, name, pos, size, back_t, back_rect):
        self.name = name
        self.grid_factor = 40
        self.w, self.h = size
        self.pos = pos
        self.zones = list()  # [rect(), hide:bool]
        self.surf = pygame.Surface((self.w, self.h))
        self.back_t = back_t
        self.back_rect = back_rect
        self.zoom_mod = 1
        self.area = [0, 0, size[0], size[1]]
        self.done = 0

    # ----------------------------------------------------------------------------------------------------------------------

    def set_grid(self, factor):
        self.grid_factor = factor

    def add_zone(self, rect, hide=False):
        self.zones.append([pygame.Rect(*rect), hide])

    def set_hide(self, index, val):
        self.zones[index][1] = val

    def move(self, modx, mody):
        self.back_rect[0] = self.back_rect[0] + modx
        self.back_rect[1] = self.back_rect[1] + mody
        self.pos = [self.pos[0] + modx, self.pos[1] + mody]

    def zoom(self, zoom):
        pass

    def load_file(self):
        file = open('maps/opt/' + self.name[:-4] + '.txt', 'r')
        lines = list()
        for line in file:
            lines.append(line[:-1])
        self.grid_factor = int(lines[0])
        if lines[1].isdigit():
            self.done = int(lines[1])
            tmp = 2
        else:
            tmp = 1
        for i in lines[tmp:-1]:
            n_line = i.split('> ')
            rect_str = n_line[0][6:-1].split(', ')
            # b = bool()
            if n_line[1].find('True') > -1:
                b = True
            else:
                b = False
            self.zones.append([
                pygame.Rect((int(rect_str[0]), int(rect_str[1]), int(rect_str[2]), int(rect_str[3]))), b])

    # ----------------------------------------------------------------------------------------------------------------------

    def draw_map(self):
        return [self.back_t, self.back_rect]

    def draw_map_set(self):
        self.surf.fill((0, 0, 0))
        for zone in self.zones:
            if zone[1] is False:
                pygame.draw.rect(self.surf, (0, 15, 23), zone[0])

        for i in range(int(self.grid_factor), self.w, int(self.grid_factor)):
            pygame.draw.aaline(self.surf, (108, 33, 44), [i, 0], [i, self.h])
        for i in range(int(self.grid_factor), self.h, int(self.grid_factor)):
            pygame.draw.aaline(self.surf, (108, 33, 44), [0, i], [self.w, i])

        self.surf.set_colorkey((0, 0, 0))

        return [self.surf, self.pos]


# --------------------------- СПИСОК КАРТ ------------------------------------------------------------------------------
maps = dict()
for m in MAPS:
    maps[m[5:]] = Map(m[5:], (0, 0), (0, 0), None, None)
    if os.path.exists('maps/opt/' + m[5:-4]+'.txt') and os.stat('maps/opt/' + m[5:-4]+'.txt').st_size != 0:
        maps[m[5:]].load_file()
# ----------------------------------------------------------------------------------------------------------------------


class Hero:
    def __init__(self, name):
        self.name = name
        self.file = open('char/' + name + '.txt', 'w')


class Adventure:
    def __init__(self, name):
        self.maps = list()  # list of Map() obj
        self.heroes = list()  # list of Hero() obj
        self.name = name
        self.file = open('adv/' + name + '.txt', 'w')
        self.rule = ''
