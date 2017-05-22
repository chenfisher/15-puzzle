import os
import sys
import argparse
import math
import readchar
import random

class Board:
    def __init__(self, size=16):
        self.rows = self.cols = int(math.sqrt(size))
        self.blocks = [str(i+1) for i in range(size)]
        self.blocks[size-1] = ""
        self.blank = size - 1

    def show(self):
        # os.system('clear')
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

class Game:
    def __init__(self, size=16):
        self.board = Board(size)

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
                's': lambda: self.board.shuffle(1000)
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
parser.add_argument("-s", "--size", default=16, help="size of the board. board is always square so rows == columns == sqrt(size)")
args = parser.parse_args()

# init the game and run
game = Game(size=int(args.size))

game.run()
