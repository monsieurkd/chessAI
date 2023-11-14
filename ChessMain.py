'''user input and display the board'''

import pygame as p
import ChessEngine as ce

WIDTH = HEIGHT = 512
DIMENSION = 8  # dimention of a chess board 8*8 (for multiplayer)
SQ_SIZE = HEIGHT // DIMENSION
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
    gs = ce.GameState()
    loadImages()  # once before the game begin
    running = True

    sqSelected = ()
    tempClick = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col) :#check if click the same square twice
                    sqSelected = ()
                    tempClick = []
                else: #add the move
                    sqSelected = (row, col)
                    tempClick.append(sqSelected)
                
                if len(tempClick) == 2: #make a move, have start and end position
                    row, col = tempClick[0]
                    print("Start position:", row, col)

                    row, col = tempClick[1]
                    print("End position:", row, col)
                    # make move
                    move = ce.Move(tempClick[0], tempClick[1], gs.board)
                    print(tempClick)
                    print(move.getNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    tempClick = []
                    
                

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gs):
    drawBoard(screen)
    # highlight
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '--':  # draw pieces
                screen.blit(IMAGES[piece], p.Rect(
                    c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
