import TicTacToe.util as util
from TicTacToe.util import px, py
import numpy as np


class Scuffle:
    def __init__(self):
        self.values = np.zeros((3, 3))
        self.winner = 0
        self.win_num = 0

    def setVal(self, pos, v):
        self.values[pos[1]][pos[0]] = v

    def getVal(self, pos):
        return self.values[pos[1], pos[0]]

    def getCopy(self):
        s = Scuffle()
        s.values = np.copy(self.values)
        s.winner = self.winner
        s.win_num = self.win_num
        return s

    def isWon(self):
        return self.winner != 0

    def checkStrike(self):
        strike, win_num, winner = util.checkStrike(self.values)
        if strike:
            self.winner = winner
            self.win_num = win_num
        elif util.checkDraw(self.values):
            self.winner = 3


def drawScuffle(start_pos, box_width, thickness):
    util.setParams(start_pos, box_width)
    util.drawRect(util.black, util.sp, (3 * util.bw, 3 * util.bw), thickness)
    util.drawLine(util.black, (px(1), py(0)), (px(1), py(3)), thickness)
    util.drawLine(util.black, (px(2), py(0)), (px(2), py(3)), thickness)
    util.drawLine(util.black, (px(0), py(1)), (px(3), py(1)), thickness)
    util.drawLine(util.black, (px(0), py(2)), (px(3), py(2)), thickness)


def drawX(shade, start_pos, box_width, thickness):
    drawXi(shade, start_pos, box_width, thickness, 0.2, -1)


def drawO(shade, start_pos, box_width, thickness):
    drawOi(shade, start_pos, box_width, thickness, 0.8)


def drawXi(shade, start_pos, box_width, thickness, o, b):
    util.setParams(start_pos, box_width)
    util.drawLine(util.red(shade), (px(o) + b, py(o)), (px(1 - o) + b, py(1 - o)), thickness)
    util.drawLine(util.red(shade), (px(1 - o) + b, py(o)), (px(o) + b, py(1 - o)), thickness)


def drawOi(shade, start_pos, box_width, thickness, s):
    util.setParams(start_pos, box_width)
    util.drawCircle(util.blue(shade), (px(0.5) + 1, py(0.5) + 1), int(box_width * s * 0.5), thickness)


def drawStrike(shade, start_pos, box_width, thickness, i, w):
    util.setParams(start_pos, box_width)
    if w == 1:
        c = util.red_purp(shade)
    else:
        c = util.blue_purp(shade)

    if i < 3:
        util.drawLine(c, (px(0.5 + i), py(0.3)), (px(0.5 + i), py(2.7)), thickness)
    elif i < 6:
        i -= 3
        util.drawLine(c, (px(0.3), py(0.5 + i)), (px(2.7), py(0.5 + i)), thickness)
    elif i == 6:
        util.drawLine(c, (px(0.4), py(0.4)), (px(2.6), py(2.6)), int(thickness * 1.4))
    elif i == 7:
        util.drawLine(c, (px(2.6), py(0.4)), (px(0.4), py(2.6)), int(thickness * 1.4))


def drawDraw(shade, start_pos, box_width, thickness, div, con, b, q):
    util.setParams(start_pos, box_width)
    c = util.gray(shade)
    for i in range(1, 10*div):
        y = (i * 0.6/div)-con
        deltay = np.clip(y - b, 0, 10)
        util.drawLine(c, (px(q + deltay), py(y - deltay)), (px(y - deltay), py(q + deltay)), thickness)
    # for i in range(1, 6):
    #     util.drawLine(c, (px(3-(i*0.5)-0.1), py(2.9)), (px(2.9), py(3-(i*0.5)-0.1)), thickness)
    # util.drawFilledSquare(util.gray(shade), start_pos, 3*box_width)
