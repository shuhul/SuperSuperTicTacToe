import TicTacToe.util as util
import TicTacToe.Scuffle as Scuffle
import TicTacToe.Game as Game
from TicTacToe.Game import Game as G
from pynput.mouse import Button
import numpy as np

sp = (0, 0)
square_width = 0
total_width = 0
x_to_play = True
hasUndoed = False
is_clicking = False
shouldUpdate = True
hasSaved = False
hasLoaded = False
curi1 = (-1, -1)
listi1 = []

class Board:
    def __init__(self):
        self.values = [[G(), G(), G()], [G(), G(), G()], [G(), G(), G()]]
        self.winner = 0
        self.win_num = 0

    def getGame(self, pos):
        return self.values[pos[1]][pos[0]]

    def getVal(self, i1):
        i1, i2, i3 = util.convertIndices(i1)
        return self.getGame(i3).getScuffle(i2).getVal(i1)

    def setVal(self, i1, v):
        i1, i2, i3 = util.convertIndices(i1)
        self.getGame(i3).getScuffle(i2).setVal(i1, v)

    def getInternalArrayForm(self):
        winners = np.zeros((9, 9))
        win_nums = np.zeros((9, 9))
        for i in range(3):
            for j in range(3):
                wins, nums = self.values[i][j].getArrayForm()
                for k in range(3):
                    for l in range(3):
                        p = (3 * i) + k
                        q = (3 * j) + l
                        winners[p][q] = wins[k][l]
                        win_nums[p][q] = nums[k][l]
        return winners, win_nums

    def getArrayForm(self):
        winners = np.zeros((3, 3))
        win_nums = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                winners[i][j] = self.values[i][j].winner
                win_nums[i][j] = self.values[i][j].win_num
        return winners, win_nums

    def getCopy(self):
        b = Board()
        for i in range(3):
            for j in range(3):
                b.values[i][j] = self.values[i][j].getCopy()
        b.winner = self.winner
        b.win_num = self.win_num
        return b

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


current_board = Board()
board_list = [Board()]


def whenClicked(pressed, button):
    global total_width, square_width, x_to_play, current_board, is_clicking, shouldUpdate, curi1
    if pressed and util.isMouseWithinScreen(sp, total_width) and isAllowedState():
        if not is_clicking:
            is_clicking = True
            add = button == Button.left
            i1 = curi1
            if add:
                scuffle_winners = current_board.getInternalArrayForm()[0]
                game_winners = current_board.getArrayForm()[0]
                sw = util.getAtDiv(scuffle_winners, i1[0], i1[1], 3)
                gw = util.getAtDiv(game_winners, i1[0], i1[1], 9)
                bw = current_board.winner
                if current_board.getVal(i1) == 0 and sw == 0 and gw == 0 and bw == 0:
                    if x_to_play:
                        current_board.setVal(i1, 1)
                    else:
                        current_board.setVal(i1, 2)
                    x_to_play = not x_to_play
                    current_board.checkStrike()
                    board_list.append(current_board.getCopy())
                    listi1.append(curi1)
            else:
                current_board.setVal(i1, 0)
            shouldUpdate = True
    else:
        is_clicking = False


def onMove(x, y):
    global total_width, square_width, shouldUpdate, curi1, sp
    if square_width != 0 and util.isMouseWithinScreen(sp, total_width):
        shouldUpdate = True
        curi1 = util.getIndicesOfPos(sp, square_width)


util.setWhenClicked(whenClicked)
util.setOnMove(onMove)


def drawBoard(start_pos, box_width):
    for i in range(3):
        for j in range(3):
            util.setParams(start_pos, 9 * box_width)
            pos = (util.px(i), util.py(j))
            Game.drawGame(pos, box_width)

    Scuffle.drawScuffle(start_pos, 9 * box_width, 4)


def checkUndo():
    global current_board, board_list, hasUndoed, shouldUpdate, curi1, square_width, sp, listi1, curi1, x_to_play
    if util.isKeyPressed('z'):
        if not hasUndoed:
            if len(board_list) > 1:
                curi1 = listi1.pop()
                board_list.pop()
                current_board = board_list[-1].getCopy()
                shouldUpdate = True
                x_to_play = not x_to_play
            hasUndoed = True
    else:
        hasUndoed = False


def checkSave():
    global current_board, listi1, hasSaved, hasLoaded, board_list, shouldUpdate, x_to_play
    if util.isKeyPressed('s'):
        if not hasSaved:
            if len(listi1) > 0:
                print('\nSaving game...')
                util.saveState(current_board, listi1[-1], x_to_play)
                print('Game Saved')
    else:
        hasSaved = False

    if util.isKeyPressed('l'):
        if not hasLoaded:
            print('\nLoading game...')
            board_list.clear()
            listi1.clear()
            cb, l, x = util.loadState()
            current_board = cb.getCopy()
            board_list.append(current_board.getCopy())
            listi1.append(l)
            x_to_play = x
            print('Game Loaded')
            shouldUpdate = True
    else:
        hasLoaded = False


def drawXOs():
    global square_width, sp, current_board, curi1, listi1

    drawTurn(sp, square_width)

    scuffle_winners, scuffle_win_nums = current_board.getInternalArrayForm()
    game_winners, game_win_nums = current_board.getArrayForm()
    board_winner, board_win_num = current_board.winner, current_board.win_num

    for x in range(27):
        for y in range(27):
            v = current_board.getVal([x, y])
            sw = util.getAtDiv(scuffle_winners, x, y, 3)
            gw = util.getAtDiv(game_winners, x, y, 9)
            bw = board_winner

            p = (sp[0] + x * square_width, sp[1] + y * square_width)

            if bw != 0:
                c = 0.25
            elif gw != 0:
                c = 0.33
            elif sw != 0:
                c = 0.5
            else:
                c = 1.0

            if v == 1:
                Scuffle.drawX(c, p, square_width, 4)
            elif v == 2:
                Scuffle.drawO(c, p, square_width, 2)

    for x1 in range(9):
        for y1 in range(9):
            sw = util.getAt(scuffle_winners, x1, y1)
            swn = util.getAt(scuffle_win_nums, x1, y1)
            gw = util.getAtDiv(game_winners, x1, y1, 3)
            bw = board_winner

            p = (sp[0] + x1 * 3 * square_width, sp[1] + y1 * 3 * square_width)

            if bw != 0:
                c = 0.33
                c1 = 0.28
                c3 = 0.2
            elif gw != 0:
                c = 0.5
                c1 = 0.4
                c3 = 0.25
            else:
                c1 = 0.6
                c = 1.0
                c3 = 0.45

            if sw == 1:
                Scuffle.drawStrike(c1, p, square_width, 6, swn, 1)
                Game.drawX(c, p, square_width)
            elif sw == 2:
                Scuffle.drawStrike(c1, p, square_width, 6, swn, 2)
                Game.drawO(c, p, square_width)
            elif sw == 3:
                Scuffle.drawDraw(c3, p, square_width, 6, 1, 0.1, 2.9, 0.05)

    for x2 in range(3):
        for y2 in range(3):
            gw = util.getAt(game_winners, x2, y2)
            gwn = util.getAt(game_win_nums, x2, y2)
            bw = board_winner

            p = (sp[0] + x2 * 9 * square_width, sp[1] + y2 * 9 * square_width)

            if bw != 0:
                c = 0.5
                c1 = 0.4
                c3 = 0.3
            else:
                c1 = 0.6
                c = 1.0
                c3 = 0.4

            if gw == 1:
                Game.drawStrike(c1, p, square_width, gwn, 1)
                drawX(c, p, square_width)
            elif gw == 2:
                Game.drawStrike(c1, p, square_width, gwn, 2)
                drawO(c, p, square_width)
            elif gw == 3:
                Game.drawDraw(c3, p, square_width)

    if board_winner != 0 and board_winner != 3:
        drawStrike(0.6, sp, square_width, board_win_num, board_winner)
        drawWinner(1.0, sp, square_width, board_winner)
    elif board_winner == 3:
        drawDraw(0.4, sp, square_width)

    if len(listi1) > 0 and board_winner == 0:
        o1, o2, o3 = util.convertIndices(listi1[-1])
        if util.getAt(game_winners, o2[0], o2[1]) == 0:
            drawSendToBorder(util.dark_green(1.0), sp, square_width, o2 * 3, ffa=0)
        else:
            drawSendToBorder(util.dark_green(1.0), sp, square_width, o2 * 3, ffa=2)

    if isAllowedState():
        i1, i2, i3 = util.convertIndices(curi1)
        if util.getAt(game_winners, i2[0], i2[1]) == 0:
            drawSendToBorder(util.dark_purp(1.0), sp, square_width, i2 * 3, ffa=0)
        else:
            drawSendToBorder(util.dark_purp(1.0), sp, square_width, i2 * 3, ffa=2)


def isAllowedState():
    global current_board, curi1, listi1
    if len(listi1) > 0:
        oldi1 = listi1[-1]
        scuffle_winners = current_board.getInternalArrayForm()[0]
        game_winners = current_board.getArrayForm()[0]
        o1, o2, o3 = util.convertIndices(oldi1)
        onew = o2 * 3 + o1
        inew = np.array(curi1) // 3
        if noWinnerAtCuri1():
            if util.getAt(game_winners, o2[0], o2[1]) == 0:
                if util.getAt(scuffle_winners, onew[0], onew[1]) == 0:
                    if onew[0] == inew[0] and onew[1] == inew[1]:
                        return True
                else:
                    inew2 = 3 * (inew // 3)
                    onew2 = o2 * 3
                    if inew2[0] == onew2[0] and inew2[1] == onew2[1] and util.getAt(scuffle_winners, inew[0],
                                                                                    inew[1]) == 0:
                        return True
            else:
                onew3 = o1
                inew3 = inew % 3
                inew4 = np.array(curi1) // 9
                if inew3[0] == onew3[0] and inew3[1] == onew3[1] and util.getAt(scuffle_winners, inew[0],
                                                                                inew[1]) == 0 and util.getAt(
                        game_winners, inew4[0], inew4[1]) == 0:
                    return True
        else:
            return False

        if curi1[0] != -1 and noWinnerAtCuri1():
            i1, i2, i3 = util.convertIndices(curi1)
            inew = i2 * 3 + i1

    else:
        return True

    # drawSendToBorder(util.dark_green(1.0), sp, square_width, [1, 1])
    # drawSendToBorder(util.dark_purp(1.0), sp, square_width, [8, 8], ffa=0)


def noWinnerAtCuri1():
    global curi1
    scuffw, gamew, boardw = getCurrentWinners()
    curv = current_board.getVal(curi1)
    return boardw == 0 and gamew == 0 and scuffw == 0 and curv == 0


def getCurrentWinners():
    global curi1, current_board

    scuffle_winners, scuffle_win_nums = current_board.getInternalArrayForm()
    game_winners, game_win_nums = current_board.getArrayForm()

    sw = util.getAtDiv(scuffle_winners, curi1[0], curi1[1], 3)
    gw = util.getAtDiv(game_winners, curi1[0], curi1[1], 9)
    bw = current_board.winner
    return sw, gw, bw


def drawSend(start_pos, box_width):
    global sp, total_width, square_width, current_board, curi1, listi1
    sp = start_pos
    square_width = box_width
    total_width = int(27 * square_width)

    board_winner = current_board.winner

    scuffle_winners = current_board.getInternalArrayForm()[0]
    game_winners = current_board.getArrayForm()[0]

    # if len(listi1) > 0:
    #     lasti1 = listi1[-1]
    #     p = (start_pos[0] + (lasti1[0] * box_width), start_pos[1] + (lasti1[1] * box_width))
    #     util.drawFilledSquare(util.dark_green(0.2),p, box_width)

    if len(listi1) > 0 and board_winner == 0:
        o1, o2, o3 = util.convertIndices(listi1[-1])
        onew = o2 * 3 + o1
        if util.getAt(game_winners, o2[0], o2[1]) == 0:
            if util.getAt(scuffle_winners, onew[0], onew[1]) == 0:
                drawSendTo(util.dark_green(0.2), start_pos, box_width, onew, ffa=0)
            else:
                drawSendTo(util.dark_green(0.2), start_pos, box_width, onew, ffa=1)
        else:
            drawSendTo(util.dark_green(0.2), start_pos, box_width, onew, ffa=2)

    if isAllowedState():
        i1, i2, i3 = util.convertIndices(curi1)
        inew = i2 * 3 + i1
        if util.getAt(game_winners, i2[0], i2[1]) == 0:
            if util.getAt(scuffle_winners, inew[0], inew[1]) == 0:
                drawSendTo(util.dark_purp(0.2), start_pos, box_width, inew, ffa=0)
            else:
                drawSendTo(util.dark_purp(0.2), start_pos, box_width, inew, ffa=1)
        else:
            drawSendTo(util.dark_purp(0.2), start_pos, box_width, inew, ffa=2)

    # for x1 in range(9):
    #     for y1 in range(9):
    #         sw = util.getAt(scuffle_winners, x1, y1)
    #         p = (start_pos[0] + x1 * 3 * box_width, start_pos[1] + y1 * 3 * box_width)
    #         if sw == 3 or x1 == 0 and y1 == 0:
    #             Scuffle.drawDraw(0.3, p, box_width)

    # drawSendTo(util.dark_green(0.2), start_pos, box_width, [3, 3])
    # drawSendTo(util.dark_purp(0.2), start_pos, box_width, [6, 6])
    # drawSendTo(util.dark_purp(0.2), start_pos, box_width, [8, 8], ffa=2)
    # drawSendTo(util.dark_purp(0.2), start_pos, box_width, [8, 8], ffa=0)


def drawSendTo(c, start_pos, box_width, p, ffa=0):
    if ffa == 0:
        q = 3
        p = (start_pos[0] + p[0] * q * box_width, start_pos[1] + p[1] * q * box_width)
        util.drawFilledSquare(c, p, q * box_width)
    elif ffa == 1:
        pos = 3 * ((np.array(p) // 3) % 3)
        q = 3
        scuffle_winners = current_board.getInternalArrayForm()[0]
        for i in range(3):
            for j in range(3):
                pos2 = pos + np.array((i, j))
                sw = util.getAt(scuffle_winners, pos2[0], pos2[1])
                p = (start_pos[0] + pos2[0] * q * box_width, start_pos[1] + pos2[1] * q * box_width)
                if sw == 0:
                    util.drawFilledSquare(c, p, q * box_width)
    else:
        pos = (np.array(p) % 3)
        scuffle_winners = current_board.getInternalArrayForm()[0]
        game_winners = current_board.getArrayForm()[0]
        for x in range(3):
            for y in range(3):
                pos2 = pos + 3 * np.array((x, y))
                gw = util.getAt(game_winners, x, y)
                sw = util.getAt(scuffle_winners, pos2[0], pos2[1])
                p = (start_pos[0] + (pos2[0] * 3 * box_width), start_pos[1] + (pos2[1] * 3 * box_width))
                if gw == 0 and sw == 0:
                    util.drawFilledSquare(c, p, 3 * box_width)


def drawSendToBorder(c, start_pos, box_width, p, ffa=0):
    if ffa != 2:
        p = (np.array(p) // 3) % 3
        p = (start_pos[0] + p[0] * 9 * square_width, start_pos[1] + p[1] * 9 * square_width)
        util.drawSquare(c, p, box_width * 9, 7)
    else:
        p = (start_pos[0], start_pos[1])
        util.drawSquare(c, p, box_width * 27, 7)


def drawX(shade, start_pos, box_width):
    Scuffle.drawXi(shade, start_pos, 9 * box_width, 38, 0.13, -1)


def drawO(shade, start_pos, box_width):
    Scuffle.drawOi(shade, start_pos, 9 * box_width, 30, 0.82)


def drawStrike(shade, start_pos, box_width, i, w):
    Scuffle.drawStrike(shade, start_pos, 9 * box_width, 44, i, w)


def drawWinner(shade, start_pos, box_width, w):
    if w == 1:
        Scuffle.drawXi(shade, start_pos, 27 * box_width, 120, 0.13, -1)
    elif w == 2:
        Scuffle.drawOi(shade, start_pos, 27 * box_width, 90, 0.82)


def drawDraw(shade, start_pos, box_width):
    Scuffle.drawDraw(shade, start_pos, 9 * box_width, 6, 9, 0.0, 3, 0.0)

def drawTurn(start_pos, box_width):
    global x_to_play
    if x_to_play:
        c = util.red(0.6)
    else:
        c = util.blue(0.6)
    b = 0.0
    util.drawFilledRect(c, (start_pos[0] + b*box_width, start_pos[1] + 27.6 * box_width), ((27-2*b) * box_width, 0.2*box_width))

# def setDraw(x1, y1, x2, y2):
#     global current_board
#     x = x1*3 + x2*9
#     y = y1*3 + y2*9
#     current_board.setVal([x + 1, y+ 1], 1)
#     current_board.setVal([x + 0, y+0], 1)
#     current_board.setVal([x + 1, y+0], 2)
#     current_board.setVal([x + 0, y+1], 2)
#     current_board.setVal([x + 2, y+2], 2)
#     current_board.setVal([x + 1, y+2], 1)
#     current_board.setVal([x + 2, y+1], 1)
#     current_board.setVal([x + 2, y+0], 2)
#
# def setDraw2(x2, y2):
#     setDraw(0, 0, x2, y2)
#     setDraw(1, 0, x2, y2)
#     setDraw(1, 1, x2, y2)
#     setDraw(2, 1, x2, y2)
#     setDraw(2, 2, x2, y2)
#     setDraw(2, 0, x2, y2)
