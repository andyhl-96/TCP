from piece import Piece
from colorama import Fore
from board import Board
from queen import Queen
class Pawn(Piece):
    # used for the first move allowing 2 tiles
    #moved: bool = False

    # set to true for one turn if the pawn moved 2 tiles
    # used to determine en passant
    #enp = False
    # set to true if the pawn has captured a piece
    # used to determine en passant
    #cap = False

    def __init__(self, position, team):
        if team == 0:
            super().__init__("pawn", "p", Fore.RED + "\u265F", position, team)
        else:
            super().__init__("pawn", "p", Fore.BLUE + "\u265F", position, team)
        self.moved = False
        self.enp = False
        self.cap = False

    def compute_move(self, positions: list[list[int]], board: Board, checking: bool):
        # first check possible moves
        # the team alignment is checked in the calling function

        # the initial position
        pos0 = positions[0]
        # the requested position to move
        pos1 = positions[1]
        self.pos_moves = []

        ud_var = 0
        if self.team == 0:
            ud_var = -1
        else:
            ud_var = 1
        # can make this code shorter later, ensure it works now

        limit = 2
        if not self.moved:
            limit = 3
        for i in range(1, limit):
            # check all possible moves
            # if a move is possible, add it to the list
            # of possible moves
            if board.board[pos0[0] + ud_var * i][pos0[1]] == None:
                # if the space is empty, allow move, 3rd element is cap
                self.pos_moves.append([pos0[0] + ud_var * i, pos0[1], None])
            else:
                # if a position is blocking other moves, do not
                # consider those moves
                break

        # next compute attacking positions
        
        # compute the positions
        atk_pos0 = [self.position[0] + ud_var, self.position[1] + 1]
        atk_pos1 = [self.position[0] + ud_var, self.position[1] - 1]

        # check the boundaries
        if atk_pos0[0] in range(0, 8) and atk_pos0[1] in range(0,8):
            # check validity of positions
            # ensure the attack positions are filled by enemy pieces
            piece0 = board.board[atk_pos0[0]][atk_pos0[1]]
            if piece0 != None and piece0.team != self.team:
                atk_pos0.append(piece0)
                self.pos_moves.append(atk_pos0)

            # en passant
            piece0 = board.board[atk_pos0[0] - ud_var][atk_pos0[1]]
            if piece0 != None and piece0.id == "p" and piece0.enp and not self.cap:
                atk_pos0.append(piece0)
                self.pos_moves.append(atk_pos0)

        if atk_pos1[0] in range(0, 8) and atk_pos1[1] in range(0, 8):
            piece0 = board.board[atk_pos1[0]][atk_pos1[1]]
            if piece0 != None and piece0.team != self.team:
                atk_pos1.append(piece0)
                self.pos_moves.append(atk_pos1)
            
            # en passant
            piece0 = board.board[atk_pos1[0] - ud_var][atk_pos1[1]]
            if piece0 != None and piece0.id == "p" and piece0.enp and not self.cap:
                atk_pos1.append(piece0)
                self.pos_moves.append(atk_pos1)


        # determine if the requested position is valid
        for move in self.pos_moves:
            # valid move by position
            if move[0] == pos1[0] and move[1] == pos1[1]:
                # determine if the move is valid by check (ie you do not put yourself in check)
                check_valid = False
                if checking:
                    check_valid = self.check_new_board_state(board, move)
                if check_valid:
                    return False, None, self.pos_moves

                if move[2] != None:
                    self.cap = True
                # determine if en passant is allowed
                if (pos0[0] + ud_var * 2) == pos1[0]:
                    # if moved 2 squares, allow enpassant
                    self.enp = True
                #self.moved = True

                return True, move[2], self.pos_moves
        # the requested position is not valid
        #print(self.pos_moves)
        #print(self.moved)
        return False, None, self.pos_moves

    def promote(self, board: Board):
        new_piece = Queen(position=self.position, team=self.team)
        if self.team == 0:
            board.red.pop(board.red.index(self))
            board.red.append(new_piece)
        elif self.team == 1:
            board.blue.pop(board.blue.index(self))
            board.blue.append(new_piece)
        board.board[new_piece.position[0]][new_piece.position[1]] = new_piece
    
    def update_state(self, turn: int, board: Board):
        # reset the enpassant
        if self.enp:
            if turn % 2 == 0 and self.team == 0:
                self.enp = False
            if turn % 2 == 1 and self.team == 1:
                self.enp = False
    
        # check promotion
        if self.team == 0 and self.position[0] == 0:
            self.promote(board)
        elif self.team == 1 and self.position[0] == 7:
            self.promote(board)
        

   

