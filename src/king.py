from piece import Piece
from colorama import Fore
from board import Board
class King(Piece):
    # used for castle validity
    #moved = False
    # determine if king is in check
    #check = False
    def __init__(self, position, team):
        if team == 0:
            super().__init__("king", "k", Fore.RED + "\u265A", position, team)
        else:
            super().__init__("king", "k", Fore.BLUE + "\u265A", position, team)
        self.moved = False
        self.check = False

    def compute_move(self, positions: list[list[int]], board: Board, checking: bool):
        # the initial position
        pos0 = positions[0]
        # the requested position to move
        pos1 = positions[1]
        # empty the possible moves list
        self.pos_moves = []

        # 8 possible move directions
        moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        for move in moves:
            if (pos0[0] + move[0]) in range(0, 8) and (pos0[1] + move[1]):
                piece = board.board[pos0[0] + move[0]][pos0[1] + move[1]]
                if piece == None or piece.team != self.team:
                    self.pos_moves.append([pos0[0] + move[0], pos0[1] + move[1], piece])
        
        for move in self.pos_moves:
            if move[0] == pos1[0] and move[1] == pos1[1]:
                # determine if the move is valid by check (ie you do not put yourself in check)
                check_valid = False
                if checking:
                    check_valid = self.check_new_board_state(board, move)
                if check_valid:
                    return False, None, self.pos_moves
                self.moved = True
                return True, move[2], self.pos_moves
        return False, None, self.pos_moves
    
    # called when castle command is inputted
    def castle(self, dir: str, board: Board):
        if not self.check and not self.moved:
            if dir == "k":
                # see if no bishop or knight
                for i in range(5, 7):
                    if board.board[self.position[0]][i] != None:
                        return False
                # check the kingside rook position
                rook = board.board[self.position[0]][7]
                if rook == None or rook.id != "r":
                    return False
                if rook.moved:
                    return False
                # perform the castle
                board.board[self.position[0]][self.position[1] + 1] = rook
                board.board[rook.position[0]][rook.position[1]] = None
                rook.position = [self.position[0], self.position[1] + 1]
                board.board[rook.position[0]][rook.position[1] + 1] = self
                board.board[self.position[0]][self.position[1]] = None
                self.position = [rook.position[0], rook.position[1] + 1]
                return True
            elif dir == "q":
                # check empty spaces
                for i in range(1, 4):
                    if board.board[self.position[0]][i] != None:
                        return False
                # check the queenside rook position
                rook = board.board[self.position[0]][0]
                if rook == None or rook.id != "r":
                    return False
                if rook.moved:
                    return False
                board.board[self.position[0]][self.position[1] - 1] = rook
                board.board[rook.position[0]][rook.position[1]] = None
                rook.position = [self.position[0], self.position[1] - 1]
                board.board[rook.position[0]][rook.position[1] - 1] = self
                board.board[self.position[0]][self.position[1]] = None
                self.position = [rook.position[0], rook.position[1] - 1]
                return True
        # error
        return False