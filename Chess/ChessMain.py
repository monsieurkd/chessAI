'''user input and display the board'''

import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENTION = 8  # dimention of a chess board 8*8 (for multiplayer)
SQ_SIZE = HEIGHT // DIMENTION
MAX_FPS = 15
IMAGES = {}

'''load the images once, make change if wanted'''


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wK",
              'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.image.load("images/" + piece + ".png")

# main driver


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()  # once before the game begin
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    # highlight
    board = 0
    drawPieces(screen, board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENTION):
        for c in range(DIMENTION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    pass


if __name__ == "__main__":
    main()
