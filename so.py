# import pygame.freetype
import sys
import pygame.constants

import classes_def as cd
import os
import locale_input as linp

ENTER = 13
FPS = 30
W = 1366
H = 710
CAPTION = 'TRPG Helper'
MAPS = list()

for root, dirs, files in os.walk('./maps'):
    for file in files:
        if file.find('.txt') == -1:
            MAPS.append('maps/' + file)

'''
DOCUMENTATION FOR ACTION ID
    100                 200
1   any-menu            move
2   any-map_arc         zoom_plus
3   any-map_editor      zoom_minus
4   any-new_adventure   grid
5                       text_field
6                       new_zone
7                       map_done
'''


def run_id(id, name=None):
    if type(id) != int:
        name = id[1]
        id = id[0]
    if id == 101:
        open_menu()
    if id == 102:
        open_map_arc()
    if id == 103:
        open_maps_editor(name)
    if id == 104:
        open_new_adventure()


def map_redact(map_opt):
    c_file = open('maps/opt/' + map_opt.name[:-4] + '.txt', 'w')

    c_file.write(str(map_opt.grid_factor) + '\n')
    c_file.write(str(map_opt.done) + '\n')

    for line in map_opt.zones:
        c_file.write(str(line[0]) + ' ' + str(line[1]) + '\n')
    c_file.write('end')

    c_file.close()


def open_menu():
    pygame.init()

    sc = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    pygame.display.set_caption(CAPTION)

    back_t = pygame.image.load('textures/menu.jpg')
    back_t = pygame.transform.scale(back_t, (600, 600))
    back_rect = back_t.get_rect()
    sc.blit(back_t, back_rect)

    buttons = list()
    buttons.append(
        cd.Button('Добро пожаловать в TRPG helper!',
                  (540, 540), (5, 10, 3, 200), (20, 20),
                  35, (255, 255, 255), 'uptitle'))
    buttons.append(
        cd.Button('Архив карт',
                  (300, 50), (11, 15, 10, 158), (130, 100),
                  30, (255, 255, 255), 'center', 'open_map_arc'))
    buttons.append(
        cd.Button('Новое приключение',
                  (300, 50), (11, 15, 10, 158), (130, 200),
                  30, (255, 255, 255), 'center', 'open_new_adventure')
    )

    for button in buttons:
        sc.blit(*button.draw_rect())
        sc.blit(*button.draw_text())

    mark = -1
    while mark == -1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if mark != -1:
                break
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in buttons:
                    id = i.acting(event)
                    if 99 < id < 200:
                        mark = id
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                mark = 102
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                mark = 104

        pygame.display.update()

    pygame.quit()
    run_id(mark)


def open_map_arc():
    pygame.init()
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption(CAPTION)

    back_t = pygame.image.load('textures/map_back.jpg')
    back_t = pygame.transform.scale(back_t, (W, H))
    back_rect = back_t.get_rect()
    sc.blit(back_t, back_rect)

    buttons = list()
    list_of_files = list()
    page = 0
    buttons.append(cd.Button('<',
                             (40, 40), (0, 15, 0, 200), (10, 10),
                             40, (255, 255, 255), 'center', 'open_menu'))
    buttons.append(cd.Button('Архив карт',
                             (500, 70), (5, 10, 3, 150), (400, 10),
                             60, (8, 235, 170), 'center'))
    buttons.append(cd.Button(str(page+1),
                             (50, 50), (0, 0, 0, 0), (1270, 650),
                             60, (255, 255, 255), 'center'))

    pos_x = 50
    pos_y = 150
    for filename in MAPS:
        if cd.maps[filename[5:]].done == 0:
            color = (211, 103, 108)
        else:
            color = (0, 255, 102)
        list_of_files.append(cd.Button((filename[5:]),
                                       (200, 200), (50, 50, 0, 150), (pos_x, pos_y),
                                       30, color, 'over', 'open_map_editor', filename, 19))
        pos_x += 240
        pos_x = pos_x % (240*5)
        if pos_x == 50:
            pos_y += 300
        pos_y = pos_y % 600

    mark = -1
    while mark == -1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if mark != -1:
                break

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mark = 101

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in buttons + list_of_files[page * 10:(page + 1) * 10]:
                    id = i.acting(event)
                    if 99 < id < 200:
                        mark = id
                    if id == 103:
                        mark = (mark, i.text)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if (page+2)*10 - len(list_of_files) < 10:
                    page += 1
                    buttons.pop()
                    buttons.append(cd.Button(str(page+1),
                                             (50, 50), (0, 0, 0, 0), (1270, 650),
                                             60, (255, 255, 255), 'center'))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if page > 0:
                    page -= 1
                    buttons.pop()
                    buttons.append(cd.Button(str(page+1),
                                             (50, 50), (0, 0, 0, 0), (1270, 650),
                                             60, (255, 255, 255), 'center'))

        sc.blit(back_t, back_rect)
        for c_file in list_of_files[page * 10:(page + 1) * 10]:
            sc.blit(*c_file.draw_rect())
            sc.blit(*c_file.draw_text())
        for button in buttons:
            sc.blit(*button.draw_rect())
            sc.blit(*button.draw_text())
        pygame.display.update()

    pygame.quit()
    run_id(mark)


def open_maps_editor(cur_map):
    pygame.init()
    sc = pygame.display.set_mode((W, H), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    pygame.display.set_caption(CAPTION)

    back_t = pygame.image.load('maps/' + cur_map)
    map_size_x, map_size_y = back_t.get_size()
    if map_size_x > map_size_y and map_size_x/map_size_y > W/H:
        scale_value = W/map_size_x
    else:
        scale_value = (H-50)/map_size_y
    back_t = pygame.transform.scale(back_t, (int(map_size_x*scale_value), int(map_size_y*scale_value)))
    back_rect = back_t.get_rect(center=(W/2, H/2-15))
    map_size_x, map_size_y = back_t.get_size()
    cd.maps[cur_map].pos = (W/2-map_size_x/2, H/2-15-map_size_y/2)
    cd.maps[cur_map].w, cd.maps[cur_map].h = map_size_x, map_size_y
    cd.maps[cur_map].surf = pygame.Surface((cd.maps[cur_map].w, cd.maps[cur_map].h))
    cd.maps[cur_map].back_t = back_t
    cd.maps[cur_map].area = [0, 0, cd.maps[cur_map].w, cd.maps[cur_map].h]
    cd.maps[cur_map].back_rect = back_rect
    if os.path.exists('maps/opt/' + cur_map[:-4]+'.txt') and os.stat('maps/opt/' + cur_map[:-4]+'.txt').st_size != 0:
        cd.maps[cur_map].load_file()
    cd.maps[cur_map].add_zone((0, 0, 100, 100))

# --------------------------- СОЗДАНИЕ СПИСКА КНОПОК -------------------------------------------------------------------

    buttons = list()
    buttons.append(cd.Button('<',
                             (40, 40), (20, 20, 20, 200), (10, 10),
                             40, (255, 255, 255), 'center', 'open_map_arc'))
    buttons.append(cd.Button('', (250, H), (20, 20, 20, 230), (W-250, 0),
                             1, (0, 0, 0), 'center'))
    buttons.append(cd.Button('Карта готова',
                             (150, 30), (20, 20, 20, 200), (10, 60),
                             25, (255, 255, 255), 'center', 'set_map_done'))
    '''buttons.append((cd.Button('up',
                              (45, 45), (255, 255, 255, 255), (1230, 150),
                              1, (0, 0, 0), 'center', 'set_move', cut=0, texture='textures/triangle.jpg')))
    buttons.append((cd.Button('down',
                              (45, 45), (255, 255, 255, 255), (1230, 250),
                              1, (0, 0, 0), 'center', 'set_move', cut=0, texture='textures/triangle.jpg')))
    buttons.append((cd.Button('left',
                              (45, 45), (255, 255, 255, 255), (1180, 200),
                              1, (0, 0, 0), 'center', 'set_move', cut=0, texture='textures/triangle.jpg')))
    buttons.append((cd.Button('right',
                              (45, 45), (255, 255, 255, 255), (1280, 200),
                              1, (0, 0, 0), 'center', 'set_move', cut=0, texture='textures/triangle.jpg')))
    buttons.append((cd.Button('clear_move',
                              (45, 45), (255, 255, 255, 255), (1230, 200),
                              1, (0, 0, 0), 'center', cut=0, texture='textures/cross.jpg')))'''
# ----------------------------------------------------------------------------------------------------------------------
    buttons.append(cd.Button('<',
                             (40, 40), (255, 255, 255, 255), (1180, 600),
                             45, (0, 0, 0), 'center', 'set_grid'))
    buttons.append(cd.Button('>',
                             (40, 40), (255, 255, 255, 255), (1280, 600),
                             45, (0, 0, 0), 'center', 'set_grid'))
    buttons.append(cd.Button('Размер клетки (пиксели)',
                             (250, 10), (0, 0, 0, 0), (1366-250, 580),
                             22, (255, 255, 255), 'center'))
# ----------------------------------------------------------------------------------------------------------------------
    buttons.append(cd.Button('Добавить зону',
                             (250, 10), (0, 0, 0, 0), (1366-250, 50),
                             22, (255, 255, 255), 'center'))
    buttons.append(cd.Button('x',
                             (70, 30), (255, 255, 255, 255), (1366-200, 70),
                             15, (0, 0, 0), 'left', 'set_text_field', cut=0))
    buttons.append(cd.Button('y',
                             (70, 30), (255, 255, 255, 255), (1366 - 200, 110),
                             15, (0, 0, 0), 'left', 'set_text_field', cut=0))
    buttons.append(cd.Button('w',
                             (70, 30), (255, 255, 255, 255), (1366 - 200, 150),
                             15, (0, 0, 0), 'left', 'set_text_field', cut=0))
    buttons.append(cd.Button('h',
                             (70, 30), (255, 255, 255, 255), (1366 - 200, 190),
                             15, (0, 0, 0), 'left', 'set_text_field', cut=0))
    buttons.append(cd.Button('Создать',
                             (250, 10), (0, 0, 0, 0), (1366 - 250, 250),
                             22, (255, 255, 255), 'center', 'set_new_zone'))

# ----------------------------------------------------------------------------------------------------------------------

    mark = -1
    select_rect = [cd.maps[cur_map].pos[0], cd.maps[cur_map].pos[1], 0, 0]
    while mark == -1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if mark != -1:
                break

            if event.type == pygame.QUIT:
                map_redact(cd.maps[cur_map])
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mark = 102
                map_redact(cd.maps[cur_map])

            if event.type == pygame.KEYDOWN:
                symbol = event.unicode
                for i in buttons:
                    if i.active is True:
                        if event.key == ENTER:
                            i.active = False
                            if i.text_field == '':
                                break
                            if i.text == 'x':
                                select_rect[0] = int(i.text_field) + cd.maps[cur_map].pos[0]
                            if i.text == 'y':
                                select_rect[1] = int(i.text_field) + cd.maps[cur_map].pos[1]
                            if i.text == 'w':
                                select_rect[2] = int(i.text_field)
                            if i.text == 'h':
                                select_rect[3] = int(i.text_field)
                        elif event.key == pygame.K_BACKSPACE:
                            i.set_input(-1)
                        else:
                            i.set_input(symbol)

# --------------------------- НАЖАТИЯ НА КНОПКИ МЫШЬЮ ------------------------------------------------------------------

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in buttons:
                    if i.active is True:
                        i.active = False
                        if i.text_field == '':
                            break
                        if i.text == 'x':
                            select_rect[0] = int(i.text_field) + cd.maps[cur_map].pos[0]
                        if i.text == 'y':
                            select_rect[1] = int(i.text_field) + cd.maps[cur_map].pos[1]
                        if i.text == 'w':
                            select_rect[2] = int(i.text_field)
                        if i.text == 'h':
                            select_rect[3] = int(i.text_field)
                    id = i.acting(event)
                    if 99 < id < 200:
                        mark = id
                        map_redact(cd.maps[cur_map])
                    if id == 201:
                        mvx, mvy = 0, 0
                        if i.text == 'up':
                            mvx, mvy = 0, 1
                        if i.text == 'down':
                            mvx, mvy = 0, -1
                        if i.text == 'left':
                            mvx, mvy = -1, 0
                        if i.text == 'right':
                            mvx, mvy = 1, 0
                        cd.maps[cur_map].move(mvx, mvy)

                    if id == 204:
                        mod = 1
                        if i.text == '<':
                            mod = -1
                        cd.maps[cur_map].set_grid(cd.maps[cur_map].grid_factor+mod)
                    if id == 205:
                        i.active = True
                    if id == 206:
                        select_rect[0] -= cd.maps[cur_map].pos[0]
                        select_rect[1] -= cd.maps[cur_map].pos[1]
                        cd.maps[cur_map].add_zone(pygame.Rect(*select_rect))
                        select_rect = [cd.maps[cur_map].pos[0], cd.maps[cur_map].pos[1], 0, 0]
                        for b in buttons:
                            b.text_field = ''
                            if b.act == 'set_text_field':
                                b.title, b.t_rect = pygame.freetype.Font(
                                    cd.FONT, b.check_rect.height).render(b.text_field, (0, 0, 0))
                                b.t_rect = b.title.get_rect(center=(b.pos[0] + b.check_rect.width / 2,
                                                                    b.pos[1] + b.check_rect.height / 2))
                    if id == 207:
                        cd.maps[cur_map].done = 1

# --------------------------- ДВИЖЕНИЕ КАРТЫ ---------------------------------------------------------------------------

            if event.type == pygame.KEYDOWN:
                mvx, mvy = 0, 0
                if event.key == pygame.K_LEFT:
                    mvx, mvy = 10, 0
                if event.key == pygame.K_RIGHT:
                    mvx, mvy = -10, 0
                if event.key == pygame.K_UP:
                    mvx, mvy = 0, 10
                if event.key == pygame.K_DOWN:
                    mvx, mvy = 0, -10
                cd.maps[cur_map].move(mvx, mvy)

        buttons.append(cd.Button(str(cd.maps[cur_map].grid_factor),
                                 (40, 40), (255, 255, 255, 255), (1230, 600),
                                 45, (0, 0, 0), 'center'))

        sc.fill((0, 29, 24))
        sc.blit(*cd.maps[cur_map].draw_map())
        sc.blit(*cd.maps[cur_map].draw_map_set())
        for button in buttons:
            sc.blit(*button.draw_rect())
            sc.blit(*button.draw_text())
        pygame.draw.rect(sc, (255, 0, 0), select_rect, 2)
        pygame.display.update()

        buttons.pop()

    pygame.quit()
    run_id(mark)


def open_new_adventure():
    pygame.init()

    sc = pygame.display.set_mode((W, H))
    clock = pygame.time.Clock()
    pygame.display.set_caption(CAPTION)

    back_t = pygame.image.load('textures/menu.jpg')
    back_t = pygame.transform.scale(back_t, (W, H))
    back_rect = back_t.get_rect()
    sc.blit(back_t, back_rect)

    char = cd.Hero('Гунд')

# ----------------------------------------------------------------------------------------------------------------------
    name = ''
    maps = list()
    heroes = list()
    rule = ''
# ----------------------------------------------------------------------------------------------------------------------

    buttons = list()
    buttons.append(cd.Button('<',
                             (40, 40), (0, 15, 0, 200), (10, 10),
                             40, (255, 255, 255), 'center', 'open_menu'))
    buttons.append(cd.Button('Создать новое приключение',
                             (500, 60), (5, 10, 3, 150), (400, 10),
                             40, (8, 235, 170), 'center'))
# ----------------------------------------------------------------------------------------------------------------------
    '''buttons.append(cd.Button('name',
                             (700, 40), (255, 255, 255, 200), (50, 100),
                             21, (0, 0, 0), 'left', 'set_text_field', cut=0))
    buttons.append(cd.Button('Название',
                             (700, 40), (255, 255, 255, 0), (50, 150),
                             37, (0, 0, 0), 'center'))'''
    buttons.append(cd.Button(char.name + ' ' + char.age,
                             (400, 400), (255, 255, 255, 200), (50, 200),
                             21, (0, 0, 0), 'left'))
    mark = -1
    while mark == -1:
        clock.tick(FPS)

        for event in pygame.event.get():
            if mark != -1:
                break
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                mark = 101

            if event.type == pygame.KEYDOWN:
                symbol = linp.get_symbol(event.unicode)
                for i in buttons:
                    if i.active is True:
                        if event.key == ENTER:
                            i.active = False
                            if i.text == 'name':
                                name = i.text_field
                        elif event.key == pygame.K_BACKSPACE:
                            i.set_input(-1)
                        else:
                            i.set_input(symbol)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in buttons:
                    if i.active is True:
                        i.active = False
                        if i.text == 'name':
                            name = i.text_field
                    id = i.acting(event)
                    if 99 < id < 200:
                        mark = id

        sc.blit(back_t, back_rect)
        for button in buttons:
            sc.blit(*button.draw_rect())
            sc.blit(*button.draw_text())
        pygame.display.update()

    pygame.quit()
    run_id(mark)
