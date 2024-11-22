from board import Board
from colorama import Fore
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
# define user interaction with the game

# setup the initial pieces and draw the board
# does not print turn nor draw the board
# these steps are done in the main loop
def initialize_board(board: Board):
    # print initialization message and turn
    #print("\nBEGIN")
    #print("<<TURN 0::RED TO MOVE>>\n")

    # initialize the pawns
    for i in range(0, 8):
        p0 = Pawn([6, i], team=0)
        p1 = Pawn([1, i], team=1)
        board.red.append(p0)
        board.blue.append(p1)
        board.add_piece(p0)
        board.add_piece(p1)
    # initialize the rest of the pieces
    #########
    # ROOKS
    #########
    p = Rook(position=[7, 0], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Rook(position=[7, 7], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Rook(position=[0, 0], team=1)
    board.blue.append(p)
    board.add_piece(p)

    p = Rook(position=[0, 7], team=1)
    board.blue.append(p)
    board.add_piece(p)

    ##########
    # KNIGHTS
    ##########
    p = Knight(position=[7, 1], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Knight(position=[7, 6], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Knight(position=[0, 1], team=1)
    board.blue.append(p)
    board.add_piece(p)

    p = Knight(position=[0, 6], team=1)
    board.blue.append(p)
    board.add_piece(p)

    ##########
    # BISHOPS
    ##########
    p = Bishop(position=[7, 2], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Bishop(position=[7, 5], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Bishop(position=[0, 2], team=1)
    board.blue.append(p)
    board.add_piece(p)

    p = Bishop(position=[0, 5], team=1)
    board.blue.append(p)
    board.add_piece(p)

    #########
    # QUEENS
    #########
    p = Queen(position=[7, 3], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = Queen(position=[0, 3], team=1)
    board.blue.append(p)
    board.add_piece(p)

    #########
    # KINGS
    #########
    p = King(position=[7, 4], team=0)
    board.red.append(p)
    board.add_piece(p)

    p = King(position=[0, 4], team=1)
    board.blue.append(p)
    board.add_piece(p)

    # draw the board
    #board.draw_board()

def process_move(move: str, board, turn, team_pieces):
    # process the move and convert it to array coordinates
    # assuming correct input, positions[0] contains initial row and col
    # positions[1] contains final row and col

    # check for castle
    if move.find("castle") != -1:
        try:
            dir = move.split(" ")[1]
            # get the moving team
            team = team_pieces[0].team
            # find the position of the king
            king_piece = None
            if team == 0:
                king_piece = board.board[7][4]
            else:
                king_piece = board.board[0][4]
            # check if the position contains the king
            valid = False
            if king_piece != None and king_piece.id == "k":
                valid = king_piece.castle(dir, board)
            if not valid:
                print("INVALID MOVE")
                return False
            return True
        except:
            print("BAD INPUT")
            return False
    try:
        # ensure there are no exceptions in parsing the string
        positions = move.split("->")
        # input validation
        if len(positions) != 2:
            print("BAD INPUT")
            return False
        positions[0] = positions[0].split(",")
        if len(positions[0]) != 2:
            print("BAD INPUT")
            return False
        positions[1] = positions[1].split(",")
        if len(positions[1]) != 2:
            print("BAD INPUT")
            return False
    except:
        # return false if the input cannot be processed
        print("BAD INPUT")
        return False
    # convert string coordinates to int
    for i in range(len(positions)):
        for j in range(len(positions[i])):
            positions[i][j] = int(positions[i][j])

    # get initial and final positions
    pos0 = positions[0]
    pos1 = positions[1]
    # get the piece to move
    piece = board.board[pos0[0]][pos0[1]]

    # check if the piece is on the right team
    if piece not in team_pieces:
        print("INVALID MOVE")
        return False
    
    valid, target, pos_moves = piece.compute_move(positions, board=board, checking=True)

    if valid:
        board.move_piece(piece, target, pos1, (turn + 1) % 2)
        board.check(turn % 2)
        return True
    else:
        print("INVALID MOVE")
        return False

def main():
    # turn counter
    turn = 0
    # lists to contain each player's pieces
    # red = []
    # blue = []


    # initialize the main board
    m_board = Board()


    # game start, menu of sorts
    welcome_msg = "###########################\n" +\
                  "###### WELCOME TO TCP #####\n" +\
                  "###########################\n"
    print(welcome_msg)

    while True:
        cmd = input("START -> `s`\nQUIT -> `q`\n>> ")
        if cmd.upper() == "S":
            initialize_board(board=m_board)
            break
        elif cmd.upper() == "Q":
            print("Farewell")
            exit(0)
        else:
            print("Bad input. Try again.")

    ################
    # main game loop
    ################
    print("\nBEGIN")
    while True:
        # player turn
        # if turn number is even, red to move, else blue to move
        ########################################
        # print next turn and state of the board
        ########################################
        if turn % 2 == 0:
            print(Fore.WHITE + "\n<<TURN " + str(turn) + "::RED TO MOVE>>\n")
        else:
            print(Fore.WHITE + "\n<<TURN " + str(turn) + "::BLUE TO MOVE>>\n")
        m_board.draw_board(turn)
        ## player choice loop
        # player can choose to move, offer draw, or resign
        while True:
            choice = ""
            if turn % 2 == 0:
                choice = input(Fore.RED + "\nENTER A CHOICE [MOVE, DRAW, RESIGN] >> ")
            else:
                choice = input(Fore.BLUE + "\nENTER A CHOICE [MOVE, DRAW, RESIGN] >> ")
            if choice.upper() == "MOVE":
                # movement loop, keep reading until a valid move is made
                while True:
                    # if a move is valid, progress to the next turn
                    # by breaking to the outermost loop
                    valid_move = False
                    # determines if the user chose to go back to the choic menus
                    back = False
                    if turn % 2 == 0:
                        move = input(Fore.RED + "\nENTER A MOVE [r0,c0->r1,c1, BACK] >> ")
                        if move.upper() == "BACK":
                            back = True
                            break
                        valid_move = process_move(move=move, 
                                                  board=m_board, 
                                                  turn=turn, 
                                                  team_pieces=m_board.red) 
                    else:
                        move = input(Fore.BLUE + "\nENTER A MOVE [r0,c0->r1,c1, BACK] >> ")
                        if move.upper() == "BACK":
                            back = True
                            break
                        valid_move = process_move(move=move, 
                                                  board=m_board, 
                                                  turn=turn, 
                                                  team_pieces=m_board.blue)
                    if valid_move:
                        break
                if not back:
                    turn += 1
                    break
            
            elif choice.upper() == "DRAW":
                pass
            elif choice.upper() == "RESIGN":
                if turn % 2 == 0:
                    print(Fore.WHITE + "BLUE WINS")
                else:
                    print(Fore.WHITE + "RED WINS")
                exit(0)
            else:
                print("BAD INPUT")


    
if __name__ == "__main__":
    main()