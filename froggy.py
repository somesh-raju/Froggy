import pygame
import os
import math
import random

x = 100
y = 30
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

pygame.init()
pygame.font.init()

display_height = pygame.display.Info().current_h - 70
display_width = 600

screen = pygame.display.set_mode((display_width, display_height))  # game window size
pygame.display.set_caption('Froggy')  # name of the game
clock = pygame.time.Clock()

main_menu_image = pygame.image.load('assets/main_menu/froggy_main_t.png').convert_alpha()
main_menu_image = pygame.transform.smoothscale(main_menu_image, (display_width, display_height))

game_over_image = pygame.image.load('assets/game_over/game_over_1.png').convert_alpha()
game_over_image = pygame.transform.smoothscale(game_over_image, (display_width, display_height))

tutorial_image = pygame.image.load('assets/tutorial.png').convert_alpha()
tutorial_image = pygame.transform.smoothscale(tutorial_image, (display_width, display_height))

bg_main = [pygame.image.load('assets/1.png'), pygame.image.load('assets/2.png'), pygame.image.load('assets/3.png'),
           pygame.image.load('assets/4.png'),
           pygame.image.load('assets/5.png'), pygame.image.load('assets/6.png'), pygame.image.load('assets/7.png'),
           pygame.image.load('assets/8.png'),
           pygame.image.load('assets/9.png'), pygame.image.load('assets/10.png')]
bg_main = [i.convert_alpha() for i in bg_main]

bg_wave = [pygame.image.load('assets/bg/water_wave_1.png'), pygame.image.load('assets/bg/water_wave_2.png'),
           pygame.image.load('assets/bg/water_wave_3.png'),
           pygame.image.load('assets/bg/water_wave_4.png'),
           pygame.image.load('assets/bg/water_wave_5.png'), pygame.image.load('assets/bg/water_wave_6.png'),
           pygame.image.load('assets/bg/water_wave_7.png'),
           pygame.image.load('assets/bg/water_wave_8.png'),
           pygame.image.load('assets/bg/water_wave_9.png'), pygame.image.load('assets/bg/water_wave_10.png')]
bg_wave = [pygame.transform.scale(i, (display_width, display_height + 400)) for i in bg_wave]
bg_wave = [i.convert_alpha() for i in bg_wave]

bg_lava = [pygame.image.load('assets/bg/lava/bg_lava_1.png'), pygame.image.load('assets/bg/lava/bg_lava_2.png'),
           pygame.image.load('assets/bg/lava/bg_lava_3.png'),
           pygame.image.load('assets/bg/lava/bg_lava_4.png'), pygame.image.load('assets/bg/lava/bg_lava_5.png'),
           pygame.image.load('assets/bg/lava/bg_lava_6.png'),
           pygame.image.load('assets/bg/lava/bg_lava_7.png'), pygame.image.load('assets/bg/lava/bg_lava_8.png'),
           pygame.image.load('assets/bg/lava/bg_lava_9.png'), pygame.image.load('assets/bg/lava/bg_lava_10.png')]
bg_lava = [pygame.transform.scale(i, (display_width, display_height + 400)) for i in bg_lava]
bg_lava = [i.convert_alpha() for i in bg_lava]

bg = random.choice([bg_main, bg_wave, bg_lava])

frog = [pygame.image.load('assets/frog/frog1.png'),
        pygame.image.load('assets/frog/frog2.png'),
        pygame.image.load('assets/frog/frog3.png'),
        pygame.image.load('assets/frog/frog4.png'),
        pygame.image.load('assets/frog/frog5.png'),
        pygame.image.load('assets/frog/frog6.png'),
        pygame.image.load('assets/frog/frog7.png')]
dead_frog = pygame.image.load('assets/frog/frog_dead.png')

arrow = pygame.image.load('assets/arrow1_2.png')
arrow = pygame.image.load('assets/tongue.png')
lilypad_green = pygame.image.load('assets/FrogLilypad_images/Objects/lilypad_green.png')
lilypad_teal = pygame.image.load('assets/FrogLilypad_images/Objects/lilypad_teal.png')
lilypad_yellow = pygame.image.load('assets/FrogLilypad_images/Objects/lilypad_yellow.png')

# Sound
if not (bg == bg_lava):
    music_main = pygame.mixer.music.load('assets/Sound/main_music.mp3')
    pygame.mixer.music.play(-1)
else:
    music_remix = pygame.mixer.music.load('assets/Sound/main_music_remix.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.6)

jump_sound = pygame.mixer.Sound('assets/Sound/jump3.wav')
water_splash_sound = pygame.mixer.Sound('assets/Sound/water_splash2.wav')

# Font
score_font = pygame.font.Font('assets/fonts/crackman/tt/crackman.ttf', 30)
game_over_font = pygame.font.Font('assets/fonts/crackman/tt/crackman front.ttf', 40)

# all variables
running = True
'''bg animation variables'''
i = 0
ii = 10  # bg speed; every ii iteration next bg will be blited/displayed
elapsed_bg = 0  # store iteration count, when surpasses ii, reset
'''variables to increase game speed as it progresses'''
speed_counter = 0
jump_speed_counter = 0
''' lily's variables'''
# b = False
lily_pos = {'x': [], 'y': []}
lily_rows = 6
lily_rect = lilypad_green.get_rect()
gap_bw_lilies = 50
gap = lily_rect.height + gap_bw_lilies
# center point of 1 row; if there are 4 rows, cal center of 1 row, which is same for all rows
row_center = (display_width / lily_rows) / 2
# calculate x coordinate for each row based on the no. of lily rows
# ex - 4 lily rows, each row center will be , row_center*odd multiples - lily_width/2
# 0,0|   1   |   3    |   5   |   7    |
lily_pos_list = [(row_center * (l + (l + 1)) - lily_rect.width / 2) for l in range(0, lily_rows)]
lily_speed = 1
'''score variable'''
score = 0
'''drawfrog variables'''
j = 0
frog_x = frog_y = 0
'''jumpfrog variables'''
jump_frame = elapsed_frog = 0
jump = False
jump_speed = 5
frog_size = 1  # initial frog size
frog_size_counter = 0.07  # frog size to inc/dec after every iteration of jump
jump_s = False  # jump sound
'''drawarrow variables'''
angle = 0
inc = arrow_speed = 2.5
'''collision variables'''
z = 0
collided = False
replay = False
'''game over'''
game_over_music = 0
tutorial_showed = False


class Frog(pygame.sprite.Sprite):
    def __init__(self, frogX, frogY):
        frog_width, frog_height = frog[0].get_rect().width, frog[0].get_rect().height
        super(Frog, self).__init__()
        self.surf = frog[0].convert_alpha()
        self.image = frog[0].convert_alpha()
        self.rect = pygame.Rect(frogX, frogY, frog_width, frog_height)
        self.mask = pygame.mask.from_surface(frog[0])


class Lilypad(pygame.sprite.Sprite):
    def __init__(self, lilyX, lilyY):
        lily_width, lily_height = lilypad_green.get_rect().width, lilypad_green.get_rect().height
        super(Lilypad, self).__init__()
        self.surf = lilypad_green.convert_alpha()
        self.image = lilypad_green.convert_alpha()
        self.rect = pygame.Rect(lilyX, lilyY, lily_width, lily_height)
        self.mask = pygame.mask.from_surface(lilypad_green)


def drawFrog(frog_x=frog_x, frog_y=frog_y):
    global j, elapsed_frog, collided

    if collided:
        screen.blit(dead_frog.convert_alpha(), (frog_x, frog_y))
        return
    screen.blit(frog[0].convert_alpha(), (frog_x, frog_y))


def jumpFrog():
    global jump_frame, elapsed_frog, jump, frog_x, frog_y, gap_bw_lilies, frog_size, angle
    global jump_s, jump_speed, score
    global game_over_music

    if not jump_s:  # do not play in every iteration; only at start
        pygame.mixer.Sound.play(jump_sound)
        jump_s = True
    if jump_frame >= len(frog):
        jump_frame = 0
        jump = False
        jump_s = False
        frog_size = 1
        col = collision(frogX=frog_x, frogY=frog_y)
        if col:
            game_over_music = 1
        else:
            score += 1
        return
    elapsed_frog += 1
    if elapsed_frog >= jump_speed:
        if jump_frame >= (len(frog) / 2):
            frog_size = frog_size - frog_size_counter
        else:
            frog_size = frog_size + frog_size_counter

        rotated_image = pygame.transform.rotozoom(frog[jump_frame], angle, frog_size)
        screen.blit(rotated_image.convert_alpha(), (frog_x, frog_y))
        jump_frame += 1
        elapsed_frog = 0
        '''Gap to be covered is (gap b/w lilies + lily height)
        and in every iteration we are moving with lily_speed
        after every jump_speed iteration'''
        frog_y -= ((gap_bw_lilies + lilypad_green.get_rect().height) / len(frog)) - lily_speed * jump_speed
        # tan(angle) * adjacent = opposite
        # /len(frog) as jump will blit len(frog) frames
        if angle > 0:
            # frog_x -= (abs((display_width / lily_rows)) / len(frog))
            frog_x -= (math.tan(math.radians(abs(angle))) * (gap_bw_lilies + lilypad_green.get_rect().height)) / len(
                frog)
        elif angle < 0:
            # frog_x += (abs((display_width / lily_rows)) / len(frog))
            frog_x += (math.tan(math.radians(abs(angle))) * (gap_bw_lilies + lilypad_green.get_rect().height)) / len(
                frog)
        # check edge case
        if frog_x > display_width:
            frog_x = display_width - frog[0].get_rect().width
        elif frog_x < 0:
            frog_x = 0
    else:
        rotated_image = pygame.transform.rotozoom(frog[jump_frame], angle, frog_size)
        screen.blit(rotated_image.convert_alpha(), (frog_x, frog_y))


def tdrawArrow(arrow=arrow):
    global angle, inc, collided
    if collided:
        return

    image = arrow
    angle += inc

    if angle > 90:
        inc = -arrow_speed
    if angle < -90:
        inc = arrow_speed

    # keep arrow's center same after rotation
    # calculate center based on original image topleft
    topleft = arrow.get_rect().topleft
    rotated_image = pygame.transform.rotate(image, angle)
    print(arrow.get_rect().center, image.get_rect().center)
    new_rect = rotated_image.get_rect(center=(image.get_rect(topleft=topleft).center[0] - 5,
                                              image.get_rect(topleft=topleft).center[1] - 15))

    screen.blit(rotated_image, (new_rect.topleft[0] + (frog[0].get_rect().topleft[0] + frog_x),
                                new_rect.topleft[1] + (frog[0].get_rect().topleft[1] + frog_y)))


def drawArrow(arrow=arrow):
    global angle, inc, collided
    if collided:
        return
    angle += inc
    if angle > 90:
        inc = -arrow_speed
    if angle < -90:
        inc = arrow_speed
    # keep arrow's center same after rotation
    # calculate rotated image center based on original image center and use it for blitting
    rotated_image = pygame.transform.rotate(arrow, angle)
    new_rect = rotated_image.get_rect(center=(arrow.get_rect().center[0] - 5,
                                              arrow.get_rect().center[1] - 15))

    screen.blit(rotated_image, (new_rect.topleft[0] + frog_x,
                                new_rect.topleft[1] + frog_y))


def drawLilypad(lilypad_x=False, lilypad_y=False):
    if lilypad_x and lilypad_y:
        screen.blit(lilypad_green.convert_alpha(), (lilypad_x, lilypad_y))


def generate_xy(choice=None):
    global lily_pos_list
    x = y = 0
    if choice:
        # next lily should be in right side of last blitted lily
        if choice == '+':
            x = lily_pos['x'][-1] + (display_width / lily_rows)
            y = lily_pos['y'][-1] - gap
        # next lily should be in left side of last blitted lily
        if choice == '-':
            x = lily_pos['x'][-1] - (display_width / lily_rows)
            y = lily_pos['y'][-1] - gap
        return x, y
    x = random.choice(lily_pos_list)
    y = -(lily_rect.height / 2)
    return x, y


# add lily x and y pos to the lily dictionary
def addToLilyList(x, y):
    global lily_pos
    lily_pos['x'].append(x)
    lily_pos['y'].append(y)


def collision(frogX=None, frogY=None):
    global z, collided, jump, frog_x, frog_y
    collide_rect = False
    diff = 20
    lily_width, lily_height = lilypad_green.get_rect().width, lilypad_green.get_rect().height
    frog_width, frog_height = frog[0].get_rect().width, frog[0].get_rect().height
    # distance_bw_coord = math.sqrt(math.pow((lilyX - frogX), 2) + math.pow((lilyY - frogY), 2))
    # print(frog[0].get_rect().colliderect(lilypad_green.get_rect()))

    for i in range(0, len(lily_pos['x'])):
        lilyX, lilyY = lily_pos['x'][i], lily_pos['y'][i]
        if pygame.Rect(frogX, frogY, frog_width, frog_height) \
                .colliderect(pygame.Rect(lilyX, lilyY, lily_width, lily_height)):
            collide_rect = True
            if (frogX >= lilyX - diff and frogY >= lilyY - diff) and \
                    ((frogX + frog_width) <= (lilyX + lily_width) + diff and (frogY + frog_height) <= (
                            lilyY + lily_height) + diff):
                pass
            else:
                collided = True
                return True
            z += 1

    if not jump and not collide_rect:
        collided = True
        return True


def out_of_screen():
    global collided, frog_y, game_over_music
    if frog_y > display_height - (frog[0].get_rect().height - 25):
        collided = True
        game_over_music = 1


def draw_score(x, y):
    global score
    rendered_font = score_font.render(f'SCORE : {score}', True, (255, 255, 255))
    screen.blit(rendered_font, (x, y))


def draw_bg():
    global i, elapsed_bg
    if i >= 10:  # 10; no of backgrounds
        i = 0  # once the background iteration reaches 10(no. of bg), restart
    elapsed_bg += 1
    if elapsed_bg > ii:  # every ii iteration blit bg
        screen.blit(bg[i], (0, 0))
        i += 1
        elapsed_bg = 0
    else:
        try:
            screen.blit(bg[i], (0, 0))
        except pygame.error:
            pass


def menu():
    pygame.init()
    while 1:
        draw_bg()
        screen.blit(pygame.transform.smoothscale(main_menu_image, (display_width + 100, display_height)), (-60, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                    menu_animation()
                    return
        try:
            pygame.display.update()
        except:
            pass
        clock.tick(60)  # fps


def menu_animation():
    m = 0
    elapsed_menu = 0
    width = 100
    height = 60
    transparency_counter = 200
    main_menu_image = pygame.image.load('assets/main_menu/froggy_main_t.png').convert()
    pygame.init()
    while 1:
        transparency_counter -= 3
        main_menu_image.set_alpha(transparency_counter)
        draw_bg()
        if m >= 22:  # 10; no of backgrounds
            return
        elapsed_menu += 1
        if elapsed_menu > 3:  # every ii iteration blit bg
            screen.blit(
                pygame.transform.scale(main_menu_image, (display_width + width, display_height + width)),
                (-height, -height))
            width += 95
            height += 45
            m += 1
            elapsed_menu = 0
        else:
            screen.blit(
                pygame.transform.scale(main_menu_image, (display_width + width, display_height + width)),
                (-height, -height))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()
        pygame.display.update()
        clock.tick(60)  # fps


def game_over():
    global score, game_over_music
    if game_over_music == 1:
        pygame.mixer.Sound.play(water_splash_sound)
        pygame.mixer.music.set_volume(0.1)
        game_over_music += 1

    file_path = r'assets/score.dat'
    with open(file_path, 'r') as f:
        hscore = int(f.readline())

    if hscore < int(score):
        with open(file_path, 'w') as f:
            f.write(str(score))

    game_over_score_text = game_over_font.render(f'YOUR SCORE : {score}', True, (255, 255, 255))
    game_over_highscore_text = game_over_font.render(f'HIGH SCORE : {hscore}', True, (255, 255, 255))
    screen.blit(game_over_image, (0, 0))
    screen.blit(game_over_score_text, ((display_width / 2) - 150, (display_height / 2) - 10))
    screen.blit(game_over_highscore_text, ((display_width / 2) - 150, (display_height / 2) + 50))


def tutorial():
    global tutorial_showed
    if not tutorial_showed:
        while 1:
            screen.blit(tutorial_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        tutorial_showed = True
                        run()
                        return
            pygame.display.update()
            clock.tick(60)  # fps


menu()


def run():
    global running, bg
    global j, frog_x, frog_y, lily_pos, lily_rows
    global lily_speed, arrow_speed, jump_speed
    global speed_counter, jump_speed_counter, jump
    global score
    global jump_frame, elapsed_frog, jump, jump_speed, frog_size, frog_size_counter, jump_s
    global angle, inc, arrow_speed, z, collided
    global replay
    global game_over_music, music_remix, music_main
    # below variables need to be reset for replay
    if replay:
        bg = random.choice([bg_main, bg_wave, bg_lava])
        j = 0
        frog_x = frog_y = 0
        lily_speed = 1
        arrow_speed = 2.5
        jump_speed = 5
        speed_counter = 0
        jump_speed_counter = 0
        # lily_rows = random.choice([4, 6, 8])
        jump = False
        lily_pos = {'x': [], 'y': []}
        score = 0
        # jumpfrog variables
        jump_frame = elapsed_frog = 0
        jump = False
        jump_speed = 5
        frog_size = 1  # initial frog size
        frog_size_counter = 0.07  # frog size to inc/dec after every iteration of jump
        jump_s = False  # jump sound
        # drawarrow variables
        angle = 0
        inc = arrow_speed = 2.5
        # collision variables
        z = 0
        collided = False
        replay = False
        game_over_music = 0
        if bg == bg_lava:
            music_remix = pygame.mixer.music.load('assets/Sound/main_music_remix.mp3')
            # pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.6)
        else:
            music_main = pygame.mixer.music.load('assets/Sound/main_music.mp3')
            # pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play(-1)
    try:
        while running:
            draw_bg()
            tutorial()
            if lily_speed < 3:
                speed_counter += 1
                if speed_counter > 250:
                    lily_speed += 0.1
                    arrow_speed += 0.1
                    speed_counter = 0
            if jump_speed > 2:
                jump_speed_counter += 1
                if jump_speed_counter > 2400 or \
                        (lily_speed > 2.2 and jump_speed == 4) or \
                        (lily_speed > 2.6 and jump_speed == 3):
                    jump_speed -= 1
                    jump_speed_counter = 0

            if len(lily_pos['x']) == 0:
                x, y = generate_xy()
                frog_x, frog_y = x + 20, y  # lily x pos + 20(to make frog blit in lily center), lily y pos
                addToLilyList(x, y)  # add lily x and y pos to the lily dictionary
                drawLilypad(x, y)  # for loop x, y ; blit in the end
            else:
                if lily_pos['y'][-1] > -lily_rect.height:  # generate new lily coordinates when last lily enters the screen
                    # +, -, both -> blit on right, left & both side respectively
                    next_step = random.choice(['+', '-', 'both'])
                    # if last blitted lily x pos is in the 1st row then blit next lily on right side
                    # as left side will go out of the screen and vice-versa
                    if lily_pos['x'][-1] == lily_pos_list[0]:
                        next_step = '+'
                    elif lily_pos['x'][-1] == lily_pos_list[-1]:
                        next_step = '-'

                    if next_step == '+':
                        x, y = generate_xy('+')
                        addToLilyList(x, y)
                    elif next_step == '-':
                        x, y = generate_xy('-')
                        addToLilyList(x, y)
                    elif next_step == 'both':
                        lr = random.choice(['left', 'right'])
                        if lr == 'left':  # left lily's x,y will goto list in last pos
                            x, y = generate_xy("+")
                            addToLilyList(x, y)
                            x = x - (display_width / lily_rows) * 2
                            addToLilyList(x, y)
                        elif lr == 'right':  # right lily's x,y will goto list in last pos
                            x, y = generate_xy("-")
                            addToLilyList(x, y)
                            x = x + (display_width / lily_rows) * 2
                            addToLilyList(x, y)

            if not collided:
                for ntemp in range(0, len(lily_pos['x'])):
                    if lily_pos['y'][ntemp] > display_height:
                        lily_pos['x'][ntemp] = 'remove'
                        lily_pos['y'][ntemp] = 'remove'
                    else:
                        drawLilypad(lily_pos['x'][ntemp], lily_pos['y'][ntemp])
                        lily_pos['y'][ntemp] += lily_speed
                if lily_pos['x'].count('remove') >= 1:
                    lily_pos['x'] = list(filter(lambda a: a != 'remove', lily_pos['x']))
                    lily_pos['y'] = list(filter(lambda a: a != 'remove', lily_pos['y']))
            # without below loop, lily blitting was jittery
            for ntemp in range(0, len(lily_pos['x'])):
                drawLilypad(lily_pos['x'][ntemp], lily_pos['y'][ntemp])

            if not jump:
                drawArrow()
                drawFrog(frog_x, frog_y)
                if not collided:
                    frog_y += lily_speed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # jump when space is pressed
                        if not collided:
                            jump = True
                    if event.key == pygame.K_r:
                        if collided:
                            replay = True
                            run()

            if jump:
                jumpFrog()

            if not game_over_music:
                out_of_screen()

            if not collided:
                draw_score(5, 0)
                pass
            else:
                game_over()

            pygame.display.update()
            clock.tick(60)  # fps
    except SystemExit:
        pygame.display.quit()
        pygame.quit()
        exit()


run()

pygame.quit()
quit()
