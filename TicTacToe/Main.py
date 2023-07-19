import TicTacToe.util as util
import TicTacToe.Scuffle as Scuffle
import TicTacToe.Game as Game
import TicTacToe.Board as Board


def update():
    start_pos = (35, 10)
    square_width = 25

    # Scuffle.drawScuffle((50,50), 20, 2, 1)
    # Game.drawGame(start_pos, square_width)

    Board.checkUndo()
    Board.checkSave()
    if Board.shouldUpdate:
        util.clearScreen()
        Board.drawSend(start_pos, square_width)
        Board.drawBoard(start_pos, square_width)
        Board.drawXOs()
        Board.shouldUpdate = False


util.setupScreen((750, 720), update, refresh_rate=10)
