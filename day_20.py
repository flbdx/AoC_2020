#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

if len(sys.argv) == 1:
    sys.argv += ["input_20"]
    
sample_input=open("input_20_sample").read()

monster ="""                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """


# edges are represented by their string value, from left to right or from
# top to bottom
# the "normalized" edge is min(edge, reversed(edge))
# it is used to connect the tiles without bothering with the flippin's

class Tile(object):
    def __init__(self, number, grid):
        self.number = number
        self.grid = grid

    def normalize_edge(self, e):
        er = "".join(reversed(e))
        return min(e, er)

    def edge_top(self, normalize=False):
        if normalize:
            return self.normalize_edge(self.edge_top(False))
        else:
            return "".join(self.grid[x,0] for x in range(10))
    def edge_bot(self, normalize=False):
        if normalize:
            return self.normalize_edge(self.edge_bot(False))
        else:
            return "".join(self.grid[x,9] for x in range(10))
    def edge_lft(self, normalize=False):
        if normalize:
            return self.normalize_edge(self.edge_lft(False))
        else:
            return "".join(self.grid[0,y] for y in range(10))
    def edge_rgt(self, normalize=False):
        if normalize:
            return self.normalize_edge(self.edge_rgt(False))
        else:
            return "".join(self.grid[9,y] for y in range(10))
    
    def rotate_right(self):
        ngrid = {}
        for (x,y), v in self.grid.items():
            ngrid[9-y, x] = v
        self.grid = ngrid
    def flip_v(self):
        ngrid = {}
        for (x,y), v in self.grid.items():
            ngrid[x, 9-y] = v
        self.grid = ngrid
    def flip_h(self):
        ngrid = {}
        for (x,y), v in self.grid.items():
            ngrid[9-x, y] = v
        self.grid = ngrid
    
    def __repr__(self):
        s = "Tile {0}\n".format(self.number)
        for y in range(10):
            s_ = ""
            for x in range(10):
                s_ += self.grid[x,y]
            s += s_ + "\n"
        return s

class Puzzle(object):
    def __init__(self):
        self.tiles = {}
        self.array = {}
        self.solved_grid = {}
        self.solved_grid_width = 0
    
    def read_input(self, lines):
        tile_grid = {}
        tile_number = 0
        y = 0
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                self.add_tile(tile_number, tile_grid)
                tile_grid = {}
                tile_number = 0
                continue
            if line.startswith("Tile "):
                tile_number=int(line[5:9])
                y = 0
            else:
                for x, c in enumerate(line):
                    tile_grid[x,y] = c#1 if c == '#' else 0
                y += 1
        
        if len(tile_grid) != 0:
            self.add_tile(tile_number, tile_grid)
        
    
    def add_tile(self, tile_number, tile_grid):
        self.tiles[tile_number] = Tile(tile_number, tile_grid)
    
    def solve_puzzle(self):
        # first collect all the normalized edges and the associated tiles IDs
        edges = {}
        for t_number, tile in self.tiles.items():
            edge_top = tile.edge_top(True)
            edge_bot = tile.edge_bot(True)
            edge_lft = tile.edge_lft(True)
            edge_rgt = tile.edge_rgt(True)
            
            edges[edge_top] = edges.get(edge_top, []) + [t_number]
            edges[edge_bot] = edges.get(edge_bot, []) + [t_number]
            edges[edge_lft] = edges.get(edge_lft, []) + [t_number]
            edges[edge_rgt] = edges.get(edge_rgt, []) + [t_number]
        
        # and collect the links between 2 tiles
        links = {}
        for e, l in edges.items():
            l = sorted(l)
            edges[e] = l
            #print(e, l)
            if len(l) == 2:
                links[l[0]] = links.get(l[0], 0) + 1
                links[l[1]] = links.get(l[1], 0) + 1
        
        # corner tiles are tiles linked to only 2 other tiles
        corners = [tile_number for tile_number, n in links.items() if n == 2]
        
        puzzle_width = int(len(self.tiles)**0.5)
        
        # let's pick one corner for our top left corner
        corner_top_left = corners[0]
        self.array[0,0] = corner_top_left
        tile_top_left = self.tiles[corner_top_left]
        
        # rotate our top left until its free edges are on the top and on the left
        while True:
            if len(edges[tile_top_left.edge_lft(True)]) == 1 and len(edges[tile_top_left.edge_top(True)]) == 1:
                break
            else:
                tile_top_left.rotate_right()
        
        # now fill in the puzzle
        # for each row
        for py in range(0, puzzle_width):
            # if it's not the first row, create the left node
            if py != 0:
                # get the edge with the upper node
                tabove = self.tiles[self.array[0, py-1]]
                norm_edge = tabove.edge_bot(True)
                next_tile_number = [n for n in edges[norm_edge] if n != tabove.number][0]
                next_tile = self.tiles[next_tile_number]
                # rotate and flip until it fits
                while True:
                    if next_tile.edge_top(True) == norm_edge:
                        break
                    next_tile.rotate_right()
                if next_tile.edge_top(False) != tabove.edge_bot(False):
                    next_tile.flip_h()
                self.array[0,py] = next_tile_number
            
            # then the other tils on the row
            for px in range(1, puzzle_width):
                tleft = self.tiles[self.array[px-1, py]]
                norm_edge = tleft.edge_rgt(True)
                next_tile_number = [n for n in edges[norm_edge] if n != tleft.number][0]
                next_tile = self.tiles[next_tile_number]
                while True:
                    if next_tile.edge_lft(True) == norm_edge:
                        break
                    next_tile.rotate_right()
                if next_tile.edge_lft(False) != tleft.edge_rgt(False):
                    next_tile.flip_v()
                self.array[px,py] = next_tile_number
        
        # it's solved, so lets create the final grid
        for py in range(puzzle_width):
            for px in range(puzzle_width):
                tile = self.tiles[self.array[px,py]]
                for ty in range(1, 9):
                    for tx in range(1, 9):
                        self.solved_grid[8*px+tx-1,8*py+ty-1] = tile.grid[tx,ty]
        self.solved_grid_width = puzzle_width * 8
    
    # rotation and flips for the solved puzzle
    def rotate_right(self):
        ngrid = {}
        for (x,y), v in self.solved_grid.items():
            ngrid[self.solved_grid_width-1-y, x] = v
        self.solved_grid = ngrid
    def flip_v(self):
        ngrid = {}
        for (x,y), v in self.solved_grid.items():
            ngrid[x, self.solved_grid_width-1-y] = v
        self.solved_grid = ngrid
    def flip_h(self):
        ngrid = {}
        for (x,y), v in self.solved_grid.items():
            ngrid[self.solved_grid_width-1-x, y] = v
        self.solved_grid = ngrid
    
    # P1 could be way shorted without solving the puzzle
    def p1(self):
        puzzle_width = int(len(self.tiles)**0.5)
        return self.array[0,0] * self.array[0,puzzle_width-1] * self.array[puzzle_width-1,0] * self.array[puzzle_width-1,puzzle_width-1]
    
    def p2(self):
        # read the monster signature
        monster_set = set()
        monster_width = 0
        monster_height = 0
        for y, line in enumerate(monster.splitlines()):
            for x, c in enumerate(line):
                monster_width = max(monster_width, x+1)
                if c == '#':
                    monster_set.add((x,y))
            monster_height = max(monster_height, y+1)
        
        # transform and count the monsters
        # some forms will repeat.
        # but don't care, we can break as soon as we found some monsters
        max_monsters = 0
        for flip in [Puzzle.flip_h, Puzzle.flip_v, Puzzle.flip_h, Puzzle.flip_v]: # no flip, flip H, flip H + flip V, flip V
            for rot in range(0, 4):
                n_monsters = 0
                for sy in range(0, self.solved_grid_width - monster_height+1):
                    for sx in range(0, self.solved_grid_width - monster_width+1):
                        ok = True
                        for mx,my in monster_set:
                            if self.solved_grid[sx + mx, sy + my] != '#':
                                ok = False
                                break
                        if ok:
                            n_monsters += 1
                #print(n_monsters)
                max_monsters = max(n_monsters, max_monsters)
                
                if max_monsters != 0:
                    break
                
                self.rotate_right()
            
            if max_monsters != 0:
                break
            
            flip(self)

        return sum(1 for v in self.solved_grid.values() if v == '#') - max_monsters * len(monster_set)

def test():
    puzzle = Puzzle()
    puzzle.read_input(sample_input.splitlines())
    puzzle.solve_puzzle()
    assert puzzle.p1() == 20899048083289
    assert puzzle.p2() == 273
test()

def p():
    puzzle = Puzzle()
    puzzle.read_input(fileinput.input())
    puzzle.solve_puzzle()
    print(puzzle.p1())
    print(puzzle.p2())
p()
