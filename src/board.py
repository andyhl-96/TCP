# class to define a board object
#from piece import Piece
from colorama import Fore

class Board:
    # standard dimensions of a chessboard
    #dim = (8, 8)
    # 2d array to hold the board state
    #board: list[list[None]]
    # list containing the two tile colors
    tiles = ["\u25A6", "\u25A1"]
    # red team
    #red = []
    # blue team
    #blue = []

    # ensure all positions on the board are unique locations in memory
    def __init__(self) -> None:
        self.board = []
        self.red = []
        self.blue = []
        for row in range(8):
            self.board.append([])
            for col in range(8):
                self.board[row].append(None)
        pass

    # prints the board to stdout
    def draw_board(self, turn: int):
        # update all piece states
        for piece in self.red:
            piece.update_state(turn, self)
        for piece in self.blue:
            piece.update_state(turn, self)

        # change this later to reduce repeated code
        if len(self.red) == 1 and len(self.blue) == 1:
            for row in range(8):
                print(Fore.WHITE + str(row) + " ", end="")
                for col in range(8):
                    if self.board[row][col] != None:
                        piece = self.board[row][col]
                        print(piece.icon + " ", end="")
                    else:
                        print(Fore.GREEN + self.tiles[(row + col) % 2] + " ", end="")
                print()
            print("STALEMATE")
            exit(0)
        if self.checkmate(0):
            print("RED REMAINING: " + str(len(self.red)))
            print("BLUE REMAINING: " + str(len(self.blue)))

            print(Fore.WHITE + "  0 1 2 3 4 5 6 7")
            # iterate over all rows
            for row in range(8):
                print(Fore.WHITE + str(row) + " ", end="")
                for col in range(8):
                    if self.board[row][col] != None:
                        piece = self.board[row][col]
                        print(piece.icon + " ", end="")
                    else:
                        print(Fore.GREEN + self.tiles[(row + col) % 2] + " ", end="")
                print()
            print("BLUE WINS BY CHECKMATE")
            exit(0)
        if self.checkmate(1):
            print("RED REMAINING: " + str(len(self.red)))
            print("BLUE REMAINING: " + str(len(self.blue)))

            print(Fore.WHITE + "  0 1 2 3 4 5 6 7")
            # iterate over all rows
            for row in range(8):
                print(Fore.WHITE + str(row) + " ", end="")
                for col in range(8):
                    if self.board[row][col] != None:
                        piece = self.board[row][col]
                        print(piece.icon + " ", end="")
                    else:
                        print(Fore.GREEN + self.tiles[(row + col) % 2] + " ", end="")
                print()
            print("RED WINS BY CHECKMATE")
            exit(0)
        if self.stalemate(0):
            print("RED REMAINING: " + str(len(self.red)))
            print("BLUE REMAINING: " + str(len(self.blue)))

            print(Fore.WHITE + "  0 1 2 3 4 5 6 7")
            # iterate over all rows
            for row in range(8):
                print(Fore.WHITE + str(row) + " ", end="")
                for col in range(8):
                    if self.board[row][col] != None:
                        piece = self.board[row][col]
                        print(piece.icon + " ", end="")
                    else:
                        print(Fore.GREEN + self.tiles[(row + col) % 2] + " ", end="")
                print()
            print("STALEMATE")
            exit(0)
        if self.stalemate(1):
            print("RED REMAINING: " + str(len(self.red)))
            print("BLUE REMAINING: " + str(len(self.blue)))

            print(Fore.WHITE + "  0 1 2 3 4 5 6 7")
            # iterate over all rows
            for row in range(8):
                print(Fore.WHITE + str(row) + " ", end="")
                for col in range(8):
                    if self.board[row][col] != None:
                        piece = self.board[row][col]
                        print(piece.icon + " ", end="")
                    else:
                        print(Fore.GREEN + self.tiles[(row + col) % 2] + " ", end="")
                print()
            print("STALEMATE")
            exit(0)

        if self.check(0):
            print("RED IN CHECK")
        if self.check(1):
            print("BLUE IN CHECK")

        print("RED REMAINING: " + str(len(self.red)))
        print("BLUE REMAINING: " + str(len(self.blue)))

        print(Fore.WHITE + "  0 1 2 3 4 5 6 7")
        # iterate over all rows
        for row in range(0, 8):
            print(Fore.WHITE + str(row) + " ", end="")
            for col in range(0, 8):
                if self.board[row][col] != None:
                    piece = self.board[row][col]
                    print(piece.icon + " ", end="")
                else:
                    print(Fore.GREEN + self.tiles[(row + col) % 2] + " ", end="")
            print()

    def add_piece(self, new_piece):
        r = new_piece.position[0]
        c = new_piece.position[1]
        self.board[r][c] = new_piece

    # takes a piece as a parameter and moves it to the specified position
    def move_piece(self, piece, target, position: list[int], enemy_team: int):
        # remove the piece at the current location on the board
        if piece.id == "p":
            piece.moved = True
        self.board[piece.position[0]][piece.position[1]] = None
        # get the target position
        # if none, no attack was made
        # if the target has a piece, an attack was made
        # remove the attacked piece
        if target != None:
            if enemy_team == 0:
                if target in self.red:
                    self.red.pop(self.red.index(target))
            else:
                if target in self.blue:
                    self.blue.pop(self.blue.index(target))
            self.board[target.position[0]][target.position[1]] = None

        self.board[position[0]][position[1]] = piece
        piece.position[0] = position[0]
        piece.position[1] = position[1]
    
    # functions to determine if given team in check/checkmate

    # ***this function will return false if a king is NOT in check
    def check(self, team: int) -> bool:
        pieces = []
        king = None
        # get the enemy pieces and the team king
        if team == 0:
            for piece in self.red:
                if piece.id == "k":
                    king = piece
            pieces = self.blue
        else:
            for piece in self.blue:
                if piece.id == "k":
                    king = piece
            pieces = self.red
        
        # obtain all possible moves of enemy pieces
        all_moves = []
        for piece in pieces:
            # throwaway positional argument, do not check for further checks, will result in infinite recursion
            temp = piece.compute_move([piece.position, [-1, -1]], self, False)
            # get only the moves
            pos_moves = temp[2]
            #print(pos_moves)
            all_moves.extend(pos_moves)
        
        #print(all_moves)
        
        # check if the king is a target in any possible moves
        # move is of form [pos0, pos1, target]
        for move in all_moves:
            if move[2] != None and move[2].id == "k":
                king.check = True
                #print("check")
                return True
        king.check = False
        #print("not check")
        return False
    

    # call every time the board is drawn or turn starts
    # a player is checkmated when they are in check and if they have no available moves
    # if a player is checkmated, end the game
    def checkmate(self, team: int):
        if not self.check(team):
            #print("NO CHECKMATE")
            return False
        # player is checked, look for possible moves
        all_moves = []
        if team == 0:
            for piece in self.red:
                # calculate possible moves accounting for the check
                temp = piece.compute_move([piece.position, [-1, -1]], self, True)
                pos_moves = temp[2]
                all_moves.extend(pos_moves)
                # check move validity
                for move in pos_moves:
                    if piece.compute_move([piece.position, [move[0], move[1]]], self, True)[0]:
                        return False
                
        else:
            for piece in self.blue:
                # calculate possible moves accounting for the check
                temp = piece.compute_move([piece.position, [-1, -1]], self, True)
                pos_moves = temp[2]
                all_moves.extend(pos_moves)
                for move in pos_moves:
                    if piece.compute_move([piece.position, [move[0], move[1]]], self, True)[0]:
                        return False
        
        #print("CHECKMATE")
        return True
        
    
    # if no player is in check and no more moves are possible
    # call at the start of each player's turn
    def stalemate(self, team):
        if self.check(team):
            #print("NOT STALEMATE")
            return False
            # check red moves
        all_moves = []
        if team == 0:
            for piece in self.red:
                # calculate possible moves accounting for the check
                temp = piece.compute_move([piece.position, [-1, -1]], self, True)
                pos_moves = temp[2]
                all_moves.extend(pos_moves)
                for move in pos_moves:
                    if piece.compute_move([piece.position, [move[0], move[1]]], self, True)[0]:
                        return False
        else:
            for piece in self.blue:
                # calculate possible moves accounting for the check
                temp = piece.compute_move([piece.position, [-1, -1]], self, True)
                pos_moves = temp[2]
                all_moves.extend(pos_moves)
                for move in pos_moves:
                    if piece.compute_move([piece.position, [move[0], move[1]]], self, True)[0]:
                        return False
        
        return True

    def print_array(self):
        print(self.board)


