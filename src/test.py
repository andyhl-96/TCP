tile = "\u25A6"
tile2 = "\u25A1"
tiles = [tile, tile2]
def draw_board():
    t_count = 0
    r_count = 0
    for row in range(8):
        if r_count % 2 == 0:
            t_count = 0
            row_tiles = ""
            for col in range(8):
                row_tiles += tiles[t_count % 2] + " "
                t_count += 1
            print(row_tiles)
        else:
            t_count = 1
            row_tiles = ""
            for col in range(8):
                row_tiles += tiles[t_count % 2] + " "
                t_count += 1
            print(row_tiles)
        r_count += 1
        
draw_board()