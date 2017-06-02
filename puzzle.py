import os
import sys
import argparse
import math
import readchar
import random
import solver
import numpy as np

class Board:
    def __init__(self, dim=4):
	size = dim * dim
        self.rows = self.cols = int(math.sqrt(size))
        self.blocks = [str(i+1) for i in range(size)]
        self.blocks[size-1] = ""
        self.blank = size - 1

	self.solver = solver.Solver(dim)

    def show(self):
        os.system('clear')
        sys.stdout.write("\033[F"*self.rows*2)

        for r in range(self.rows):
            for c in range(self.cols):
                print self.blocks[r * self.cols + c].ljust(4),
            print "\n\n",

    def move_left(self):
        current_row = self.row(self.blank)
        target_row = self.row(self.blank + 1)

        if target_row != current_row:
            return

        self.swap(self.blank + 1, self.blank)

    def move_right(self):
        current_row = self.row(self.blank)
        target_row = self.row(self.blank - 1)

        if target_row != current_row:
            return

        self.swap(self.blank - 1, self.blank)

    def move_down(self):
        current_row = self.row(self.blank)
        target_row = self.row(self.blank - self.cols)

        if target_row < 0:
            return

        self.swap(self.blank - self.cols, self.blank)

    def move_up(self):
        current_row = self.row(self.blank)
        target_row = self.row(self.blank + self.cols)

        if target_row > self.rows - 1:
            return

        self.swap(self.blank + self.cols, self.blank)

    def swap(self, i, j):
        iv = self.blocks[i]
        self.blocks[i] = self.blocks[j]
        self.blocks[j] = iv
        self.blank = i

    def row(self, i):
        return i/self.cols

    def shuffle(self, n=1):
        moves = [self.move_left, self.move_right, self.move_up, self.move_down]

        for i in range(n):
            random.choice(moves)()

    def solve(self):
	array = np.array([int(s) if s else 0 for s in self.blocks])
        empty_spot = self.blocks.index("")
        cost, path = self.solver.solve(solver.State(array, empty_spot))
        print "cost = ", cost
        print "path:"
        for state in path:
            print state
        wait = raw_input("PRESS ENTER TO CONTINUE.")


class Game:
    def __init__(self, dim=4):
        self.board = Board(dim)

    def run(self):
        left = ''.join(chr(x) for x in [27, 91, 68])
        right = ''.join(chr(x) for x in [27, 91, 67])
        down = ''.join(chr(x) for x in [27, 91, 66])
        up = ''.join(chr(x) for x in [27, 91, 65])

        options = { 
                left: self.board.move_left,
                right: self.board.move_right,
                up: self.board.move_up,
                down: self.board.move_down,
                'h': self.board.move_left,
                'l': self.board.move_right,
                'j': self.board.move_down,
                'k': self.board.move_up,
                'p': self.board.show,
                's': lambda: self.board.shuffle(1000),
                'x': self.board.solve
                }

        self.board.show()
        while (True):
            k = readchar.readkey()
            if k == 'q':
                break

            options.get(k, lambda: 'do nothing')()
            self.board.show()


os.system('clear')

# get size from arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--dim", default=4, help="dimension of the board, num_rows == num_columns == dim")
args = parser.parse_args()

# init the game and run
game = Game(dim=int(args.dim))

game.run()

