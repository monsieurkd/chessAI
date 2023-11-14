"""
storing current info of the board
determine the vaild move
move log (undo move)
"""


class GameState():
    def __init__(self):
        # 8*8 2 dimentional list, each have 2 characters (black space is '--')
        # the first character is for color ('b': black; 'w': white)
        # the second is for the piece(Queen, Knight, Rook,..)
        # numpy array is more efficient
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove


class Move():
    
    ranksToRows = {"1": 7, "2": 6 , "3": 5, "4": 4 , "5": 3, "6": 2, "7": 1, "8":0}
    rowsToRanks = {v:k for k,v in ranksToRows.items()} 
    
    filesToCols = {"a": 0, "b": 1 , "c": 2, "d": 3 , "e": 4, "f": 5, "g": 6, "h":7}
    colsToFiles = {v:k for k,v in filesToCols.items()}



    def __init__(self, startSq, endSq, board):
        self.startSq = startSq
        self.endSq = endSq
        self.startCol = startSq[1]
        self.startRow = startSq[0]
        self.endCol = endSq[1]
        self.endRow = endSq[0]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCapture = board[self.endRow][self.endCol]


    def getRankFile(self, col, row):
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    def getNotation(self):
        return self.getRankFile(self.startCol, self.startRow) + self.getRankFile(self.endCol, self.endRow)