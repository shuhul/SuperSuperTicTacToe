import TicTacToe.util as util
import TicTacToe.Scuffle as Scuffle
from TicTacToe.Scuffle import Scuffle as S
import numpy as np


class Game:
    def __init__(self):
        self.values = [[S(), S(), S()], [S(), S(), S()], [S(), S(), S()]]
        self.winner = 0
        self.win_num = 0

    def getScuffle(self, pos):
        return self.values[pos[1]][pos[0]]

    def getCopy(self):
        g = Game()
        for i in range(3):
            for j in range(3):
                g.values[i][j] = self.values[i][j].getCopy()
        g.winner = self.winner
        g.win_num = self.win_num
        return g

    def getArrayForm(self):
        winners = np.zeros((3, 3))
        win_nums = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                winners[i][j] = self.values[i][j].winner
                win_nums[i][j] = self.values[i][j].win_num
        return winners, win_nums

    def checkInternalStrikes(self):
        for i in range(3):
            for j in range(3):
                self.values[i][j].checkStrike()

    def checkStrike(self):
        self.checkInternalStrikes()
        winners, win_nums = self.getArrayForm()
        strike, win_num, winner = util.checkStrike(winners)
        if strike:
            self.winner = winner
            self.win_num = win_num
        elif util.checkDraw(winners):
            self.winner = 3


def drawGame(start_pos, box_width):
    for i in range(3):
        for j in range(3):
            util.setParams(start_pos, 3 * box_width)
            pos = (util.px(i), util.py(j))
            Scuffle.drawScuffle(pos, box_width, 1)

    Scuffle.drawScuffle(start_pos, 3 * box_width, 1)


def drawX(shade, start_pos, box_width):
    Scuffle.drawXi(shade, start_pos, 3 * box_width, 12, 0.15, -1)


def drawO(shade, start_pos, box_width):
    Scuffle.drawOi(shade, start_pos, 3 * box_width, 8, 0.8)


def drawStrike(shade, start_pos, box_width, i, w):
    Scuffle.drawStrike(shade, start_pos, 3 * box_width, 15, i, w)


def drawDraw(shade, start_pos, box_width):
    Scuffle.drawDraw(shade, start_pos, 3 * box_width, 6, 3,0.05, 2.98, 0.05)
