from piece import Piece
class TestPiece(Piece):
    # a list of moves to populate
    moves: list
    def __init__(self, name, id, icon, position, team):
        super().__init__(name, id, icon, position, team)