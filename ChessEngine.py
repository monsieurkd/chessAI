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
        self.moveFunctions = {'p': self.pawnMove, 'R': self.rookMove, 'N': self.knightMove, 'B': self.bishopMove, 'Q': self.queenMove, 'K': self.kingMove}
        self.whiteKingPosition = (7,4)
        self.blackKingPosition = (0,4)
        self.checkMate = False
        self.staleMate = False
     
    '''make a move but not for enpassant, castling and promotion '''
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #update king position
        if move.pieceMoved == "wK": 
            self.whiteKingPosition = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingPosition = (move.endRow, move.endCol)
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

    '''undo'''
    def UndoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCapture
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK": 
                self.whiteKingPosition = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingPosition = (move.startRow, move.startCol)
    '''to check valid, generate move, make the move, generate move for opponent, if opponent possible move have check -> invalid move (the piece move make the opponent piece able to check)'''
    def getValidMoves(self):
        moves = self.getPossibleMoves()

        for i in range(len(moves)-1,-1,-1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.UndoMove()
        
        if len(moves) == 0:
            if self.inCheck:
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        
        return moves
    
    def blankFuc(self):
        pass

    

    def squareUnderAttack(self,r,c):
        self.whiteToMove = not self.whiteToMove
        oppMove = self.getPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMove:
            if move.endRow == r and move.endCol == c:
                return True
                
        return False
    #check if king in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingPosition[0], self.whiteKingPosition[1])
        else:
            return self.squareUnderAttack(self.blackKingPosition[0], self.blackKingPosition[1])
        





    '''generate all possible move'''
    def getPossibleMoves(self):
        moves= []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                color = self.board[r][c][0]
                piece = self.board[r][c][1] 

                if((color == 'w' and self.whiteToMove ) or ( color == 'b' and not self.whiteToMove )):
                    self.moveFunctions[piece](r,c,moves)

        return moves
    

    def pawnMove(self,r,c,moves):
        #check for color
        #check for collision
        #eat piece
        if self.whiteToMove:
            #add first move
                
            if self.board[r-1][c] == "--":
                   
                   
                moves.append(Move((r,c),(r-1,c),self.board))
                if self.board[r-2][c] == "--" and r == 6:
                    moves.append(Move((r,c),(r-2,c),self.board))
            
            if c -1 >= 0 and self.board[r-1][c-1][0] == 'b' : #add capture left
                
                moves.append(Move((r,c),(r-1,c-1),self.board))
            if  c +1 <= 7 and self.board[r-1][c+1][0] == 'b' : #add capture right
              
                moves.append(Move((r,c),(r-1,c+1),self.board)) 
        
        else:
            
            #add first move
                
            if self.board[r+1][c] == "--":
                
                   
                moves.append(Move((r,c),(r+1,c),self.board))
                if self.board[r+2][c] == "--" and r == 1:
                    moves.append(Move((r,c),(r+2,c),self.board))
        

            
           
            if c +1 <= 7 and self.board[r+1][c+1][0] == 'w' : #add capture left
                
                moves.append(Move((r,c),(r+1,c+1),self.board))
            if c -1 >=0  and self.board[r+1][c-1][0] == 'w' : #add capture right
              
                moves.append(Move((r,c),(r+1,c-1),self.board))


                    

    def rookMove(self,r,c,moves):
        #empty square, same color square and different color square
        direction = ((-1,0),(1,0),(0,-1),(0,1))
        enemyColor = "b" if self.whiteToMove else "w" 

        for d in direction:
            for i in range (1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endCol <8 and 0 <= endRow <8: #onboard
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                        break
                    else:
                        break
                else: #out of bounce
                    break    
            
        
    def bishopMove(self,r,c,moves):
        direction = ((-1,1),(1,1),(1,-1),(-1,-1))
        enemyColor = "b" if self.whiteToMove else "w" 

        for d in direction:
            for i in range (1,8):
                endRow = r + d[0]*i
                endCol = c + d[1]*i
                if 0<= endCol <8 and 0 <= endRow <8: #onboard
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                        break
                    else:
                        break
                else: #out of bounce
                    break   

    def knightMove(self,r,c,moves):
        
        directions = ((-2,1),(2,1),(2,-1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]
                endCol = c + d[1]
                if 0 <= endCol <8 and  0<= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    else: #same color piece
                
                        break

                else: #out of bounce
                    break

    
    
    def queenMove(self,r,c,moves):
        self.bishopMove(r,c,moves)
        self.rookMove(r,c,moves)

    def kingMove(self,r,c,moves):
        directions = ((-1,1),(-1,0),(-1,-1),(0,-1),(0,1),(1,1),(1,-1),(1,0))
        allyColor = "w" if self.whiteToMove else "b"
        for d in directions:
            for i in range(1,8):
                endRow = r + d[0]
                endCol = c + d[1]
                if 0 <= endCol <8 and  0<= endRow < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow, endCol), self.board))
                    else: #same color piece
                
                        break

                else: #out of bounce
                    break 




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
        self.isPawnPromotion = False
        if (self.pieceMoved == "wp" and self.endRow == 0) or (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True
        self.moveID = self.startCol * 1000 + self.startRow * 100 + self.endCol * 10 + self.endRow

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getRankFile(self, col, row):
        return self.colsToFiles[col] + self.rowsToRanks[row]
    
    def getNotation(self):
        return self.getRankFile(self.startCol, self.startRow) + self.getRankFile(self.endCol, self.endRow)