"""
Clone of 2048 game.
"""

import poc_2048_gui
import random


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = []
    for item in range(0,len(line)):
        if line[item] !=0:
            result.append(line[item])
    print result
    jerry =0
    while jerry<len(result)-1:
        if result[jerry] == result[jerry+1]:
            result[jerry] = 2*result[jerry]
            result[jerry+1] = 0
            jerry +=2
        else:
            jerry+=1
    final_result = []
    for item in range(0,len(result)):
        if result[item] != 0:
            final_result.append(result[item])
    for item in range(0,len(line)-len(final_result)):
        final_result.append(0)
    return final_result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._grid = []
        self.reset()
        self._initial_tiles = {}
        up_row = [0 for x in range(self._width)]  # grid_width
        up_col = [x for x in range(self._width)]
        down_row = [self._height-1 for x in range(self._width)]
        down_col = [x for x in range(self._width)]
        left_row = [x for x in range(self._height)]
        left_col = [0 for x in range(self._height)]
        right_row = [x for x in range(self._height)]
        right_col = [self._width-1 for x in range(self._height)]
        self._initial_tiles[UP] = zip(up_row,up_col)
        self._initial_tiles[DOWN] = zip(down_row,down_col)
        self._initial_tiles[LEFT] = zip(left_row,left_col)
        self._initial_tiles[RIGHT] = zip(right_row,right_col)

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grid = [[0 for dummy_col in range(self._width)] for dummy_row in range(self._height)]
        self.new_tile()
        self.new_tile()
        

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
    
        return str(self._grid)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        # replace with your code
        change = 0
        initial_list = self._initial_tiles[direction]
        if direction == UP or direction == DOWN:
            for item in range(0,self._width):
                line = []
                row = initial_list[item][0]
                col = initial_list[item][1]
                temp_row = OFFSETS[direction][0]
                temp_col = OFFSETS[direction][1]
                for dummy_j in range(0,self._height):
                    new_row = row+dummy_j*temp_row
                    new_col = col + dummy_j* temp_col
                    tile = self.get_tile(new_row,new_col)
                    line.append(tile)
                old_line = line[:]
                line = merge(line)
                if old_line != line:
                    change =1
                for dummy_j in range(0,self._height):
                    new_row = row+dummy_j*temp_row
                    new_col = col + dummy_j* temp_col
                    self.set_tile(new_row,new_col,line[dummy_j])
        else:
            for item  in range(0,self._height):
                line = []
                row = initial_list[item][0]
                col = initial_list[item][1]
                temp_row = OFFSETS[direction][0]
                temp_col = OFFSETS[direction][1]
                for dummy_j in range(0,self._width):
                    new_row = row+dummy_j*temp_row
                    new_col = col + dummy_j* temp_col
                    tile = self.get_tile(new_row,new_col)
                    line.append(tile)
                old_line = line[:]
                line = merge(line)
                if old_line != line:
                    change =1
                for dummy_j in range(0,self._width):
                    new_row = row+dummy_j*temp_row
                    new_col = col + dummy_j* temp_col
                    self.set_tile(new_row,new_col,line[dummy_j])
        if change == 1:
            self.new_tile()


    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        # replace with your code
        non_zero = []
        for item  in range(0,self._width*self._height):
            row = int(item /self._width)
            col = item  % self._width
            if self._grid[row][col] == 0:
                non_zero.append(item)
        if len(non_zero) !=0:
            cell1 = random.choice(non_zero)
            row1 = int(cell1/self._width)
            col1 = cell1%self._width
            prob1 = random.choice(range(0,10))
            if prob1 == 0:
                self.set_tile(row1,col1,4)
            else:
                self.set_tile(row1,col1,2)



    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value


    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]
# x = TwentyFortyEight(3,3)
# x.set_tile(0, 0, 2)
# print x.__str__()
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))