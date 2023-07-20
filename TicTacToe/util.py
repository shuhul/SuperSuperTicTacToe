import pygame as pg
import os
import numpy as np
import pynput
import keyboard
from pynput.mouse import Listener
import pickle

mouse = pynput.mouse.Controller()
wc = lambda pressed, button: pressed
om = lambda x,y: 0

ranWC = False


def on_click(x, y, button, pressed):
    wc(pressed, button)

def on_move(x,y):
    om(x,y)

def red(shade):
    return c_avg(c_red, c_white, shade)


def blue(shade):
    return c_avg(c_blue, c_white, shade)


def red_purp(shade):
    return c_avg(red(shade), purp(shade), 0.8)


def blue_purp(shade):
    return c_avg(blue(shade), purp(shade), 0.9)


def purp(shade):
    return c_avg(c_purp, c_white, shade)


def c_avg(c1, c2, x):
    if x > 1:
        x = 1
    return np.array(c1) * x + np.array(c2) * (1 - x)


def orange(shade):
    return c_avg(c_orange, c_white, shade)


def orange2(shade):
    return c_avg(c_orange2, c_white, shade)


def blue2(shade):
    return c_avg(c_blue2, c_white, shade)


def green(shade):
    return c_avg(c_green, c_white, shade)


def dark_green(shade):
    return c_avg(c_dark_green, c_white, shade)


def dark_purp(shade):
    return c_avg(c_dark_purp, c_white, shade)


def gray(shade):
    return c_avg(c_black, c_white, shade)


listener = Listener(on_click=on_click, on_move=on_move)
listener.start()
window = None
c_purp = (255, 0, 255)
c_white = (255, 255, 255)
c_black = (0, 0, 0)
c_red = (255, 0, 0)
c_blue = (60, 60, 255)
c_green = (0, 255, 0)
c_dark_green = c_avg(c_green, c_black, 0.5)
c_dark_purp = c_avg(c_purp, c_black, 0.5)

c_orange = c_avg((240, 128, 0), c_black, 0.9)

c_orange2 = (242, 160, 40)
c_blue2 = c_avg((0, 150, 255), c_black, 0.9)
# light_red = (255, 100, 100)
# light_blue = (160, 160, 255)
# light_light_red = (255, 170, 170)
# light_light_blue = (210, 210, 255)
# light_light_light_red = (255, 220, 220)
# light_light_light_blue = (230, 230, 255)
black = (0, 0, 0)
white = (255, 255, 255)

sp = (0, 0)
bw = 0


def setParams(start_pos, box_width):
    global sp, bw
    sp = start_pos
    bw = box_width


def px(i):
    global sp, bw
    return sp[0] + i * bw


def py(i):
    global sp, bw
    return sp[1] + i * bw


def getIndicesOfPos(start_pos, box_width):
    p = np.array(getMousePos()) - np.array(start_pos)
    indices = p // box_width
    return indices


def convertIndices(i):
    i = np.array(i)
    return i % 3, (i // 3) % 3, ((i // 9) % 3)


def isMouseWithinScreen(start_pos, width):
    p = getMousePos()
    return start_pos[0] <= p[0] <= start_pos[0] + width and start_pos[1] <= p[1] <= start_pos[1] + width


def isKeyPressed(key):
    return keyboard.is_pressed(key)


def setWhenClicked(whenClickedFunc):
    global wc
    wc = whenClickedFunc

def setOnMove(onMovedFunc):
    global om
    om = onMovedFunc

def getMousePos():
    winpos = str(os.environ['SDL_VIDEO_WINDOW_POS'])
    x, y = winpos.split(',')
    return np.array(mouse.position) - np.array([int(x), int(y)])


def drawRect(color, rb, size, width):
    pg.draw.rect(window, color, (rb[0], rb[1], size[0], size[1]), width)


def drawSquare(color, rb, size, width):
    pg.draw.rect(window, color, (rb[0], rb[1], size, size), width)


def drawFilledSquare(color, rb, size):
    pg.draw.rect(window, color, (rb[0], rb[1], size, size))


def drawFilledRect(color, rb, size):
    pg.draw.rect(window, color, (rb[0], rb[1], size[0], size[1]))



def drawLine(color, lb, lt, width):
    pg.draw.line(window, color, lb, lt, width)


def drawCircle(color, lb, radius, width):
    pg.draw.circle(window, color, (int(lb[0]), int(lb[1])), int(radius), width)


def setupScreen(size, update, exit_key='q', refresh_rate=30, pos=(50, 70)):
    global window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % pos
    pg.init()

    window = pg.display.set_mode(size)

    pg.display.set_caption("Super Squared Tic-Tac-Toe")

    run = True

    while run:
        pg.time.delay(int(1000 / refresh_rate))



        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

        pg.event.get()

        if isKeyPressed(exit_key):
            break

        update()

        pg.display.update()

    pg.quit()


def clearScreen():
    window.fill((255, 255, 255))


def checkStrike(grid):
    for i in range(3):
        if grid[0][i] == grid[1][i] == grid[2][i] and grid[0][i] != 0 and grid[0][i] != 3:
            return True, i, grid[0][i]
    for j in range(3):
        if grid[j][0] == grid[j][1] == grid[j][2] and grid[j][0] != 0 and grid[j][0] != 3:
            return True, j + 3, grid[j][0]
    if grid[0][0] == grid[1][1] == grid[2][2] and grid[1][1] != 0 and grid[1][1] != 3:
        return True, 6, grid[1][1]
    if grid[2][0] == grid[1][1] == grid[0][2] and grid[1][1] != 0 and grid[1][1] != 3:
        return True, 7, grid[1][1]
    return False, None, None


def checkDraw(grid):
    grid1 = np.copy(np.array(grid))
    grid2 = np.copy(np.array(grid))
    s = 0
    for i in range(3):
        for j in range(3):
            s += (0 if grid[i][j] == 0 else 1)
    if s > 5:
        for i1 in range(3):
            for j1 in range(3):
                if grid1[i1][j1] == 0:
                    grid1[i1][j1] = 1
        strike1 = checkStrike(grid1)[0]
        for i2 in range(3):
            for j2 in range(3):
                if grid2[i2][j2] == 0:
                    grid2[i2][j2] = 2
        strike2 = checkStrike(grid2)[0]
        return not strike1 and not strike2
    return False


def getAtDiv(arr, x, y, n):
    if x // n > len(arr)-1 or y // n > len(arr)-1:
        return arr[-1][-1]
    else:
        return arr[y // n][x // n]


def getAt(arr, x, y):
    return arr[y][x]

def saveState(current_board, last_i1, x2p):
    pickle.dump(current_board, open('save/current_board2.obj', 'wb'))
    # pickle.dump(last_i1, open('save/current_board.obj', 'w'))
    # np.save('save/current_board', current_board)
    np.save('save/last_i12', last_i1)
    np.save('save/x2p2', x2p)

def loadState():
    return pickle.load(open('save/current_board2.obj', 'rb')), np.load('save/last_i12.npy'), np.load('save/x2p2.npy')

# arr = np.zeros((3,3))
# arr[1][1] = 1
# arr[0][1] = 2
# arr[1][0] = 2
# arr[0][0] = 1
# arr[2][2] = 2
# arr[2][1] = 1
# arr[0][2] = 2
# arr[1][2] = 1
# print(arr)
# print(checkDraw(arr))
