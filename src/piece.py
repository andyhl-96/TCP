from board import Board
import copy
class Piece:
    # name: str
    # id: str
    # icon: str
    # position: list
    # team: int = 0
    # pos_moves= []
    def __init__(self, name, id, icon, position, team):
        self.name = name
        self.id = id
        self.icon = icon
        self.position = position
        self.team = team
        self.pos_moves = []
    
    def update_state(self, turn: int, board: Board):
        pass

    def check_new_board_state(self, old_board: Board, move) -> bool:
        # initialize the new board
        new_board = Board()
        # add copies of pieces to the new board
        for row in old_board.board:
            for piece in row:
                if piece == None:
                    continue
                piece_copy = copy.deepcopy(piece)
                #print(piece_copy)
                new_board.add_piece(piece_copy)
                if piece_copy.team == 0:
                    new_board.red.append(piece_copy)
                else:
                    new_board.blue.append(piece_copy)
        
        # perform the move
        # get corresponding piece on new board
        self_piece = new_board.board[self.position[0]][self.position[1]]
        target_piece = None
        if move[2] != None:
            target_piece = new_board.board[move[2].position[0]][move[2].position[1]]
        new_board.move_piece(self_piece, target_piece, [move[0], move[1]], (self.team + 1) % 2)

        # check the board to see if it is valid
        return new_board.check(self.team)
        