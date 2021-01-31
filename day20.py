import math
import re
import day01


class Tile():
    # square tile
    edge_sort = ['T', 'L', 'B', 'R']
    def __init__(self, a_num):
        self.num = a_num
        self.rot = 0
        self.flips = 0
        # edges
        self.sides = {'T': None, 'L': None, 'B': None, 'R': None}
        self.content = None
        self.width = None
        self.no_match = [False] * 4
    
    def set_content(self, a_con):
        self.content = a_con
        self.width = len(self.content)
        self.load_sides()

    def load_sides(self):
        self.sides['T'] = self.content[0]
        self.sides['B'] = self.content[-1]
        self.sides['L'] = ''.join([x[0] for x in self.content])
        self.sides['R'] = ''.join([x[-1] for x in self.content])

    def display_tile(self):
        for c in self.content:
            print(c)

    @classmethod
    def new_tile(cls, a_num, a_con):
        t = cls(a_num)
        t.set_content(a_con)
        return t

    def get_side(self, a_dir):
        s = None
        try:
            s = self.sides[a_dir]
        except KeyError:
            print(f"'Tile': no direction {a_dir}")
        return s

    def get_side_type(self, a_side):
        for k in self.edge_sort:
            x = self.get_side(k)
            if x == a_side:
                return k

    def rotate(self, a_times):
        """ Rotate tile clockwise by a_times*90degrees """
        # clockwise
        new_content = []
        if a_times == 1:
            for j in range(self.width):
                new_content.append(''.join([self.content[self.width-1-i][j] for i in range(self.width)]))
        elif a_times == 2:
            for j in range(self.width):
                new_content.append(''.join([self.content[self.width-1-j][self.width-1-i] for i in range(self.width)]))
        elif a_times == 3:
            for j in range(self.width):
                new_content.append(''.join([self.content[i][self.width-1-j] for i in range(self.width)]))
        self.set_content(new_content)
        self.no_match = self.no_match[a_times:] + self.no_match[:a_times]
    
    def flip(self, a_type):
        """ Flip tile either via horizonal (a_type=2) or vertical (a_type=1) axis """
        if a_type == 1:
            new_content = []
            for c in self.content:
                new_content.append(c[::-1])
            self.set_content(new_content)
            self.no_match = [self.no_match[0], self.no_match[3], self.no_match[2], self.no_match[1]]
        elif a_type == 2:
            self.set_content(self.content[::-1])
            self.no_match = [self.no_match[2], self.no_match[1], self.no_match[0], self.no_match[3]]
    
class Map():
    def __init__(self, a_width, a_tiles, a_edges):
        self.grid = []
        for _ in range(a_width):
            self.grid.append([None] * a_width)
        self.width = a_width
        self.tiles = a_tiles
        self.edges = a_edges
        self.image = []
        self.image_width = None

    @staticmethod
    def place_tile(a_tile:Tile, a_left, a_left_flip):
        """ align tile according to left edge needs """
        if a_left == 'L':
            if a_left_flip:
                a_tile.flip(2)
        elif a_left == 'R':
            if not a_left_flip:
                a_tile.flip(1)
            else:
                a_tile.rotate(2)
        elif a_left == 'B':
            if a_left_flip:
                a_tile.flip(1)
            a_tile.rotate(1)
        else:
            if not a_left_flip:
                a_tile.flip(1)
            a_tile.rotate(3)
    
    @staticmethod
    def place_tile_top(a_tile:Tile, a_top, a_top_flip):
        """ align tile according to top edge needs """
        if a_top == 'L':
            if a_top_flip:
                a_tile.rotate(1)
            else:
                a_tile.flip(1)
                a_tile.rotate(3)
        elif a_top == 'R':
            if a_top_flip:
                a_tile.flip(1)
                a_tile.rotate(1)
            else:
                a_tile.rotate(3)
        elif a_top == 'B':
            if not a_top_flip:
                a_tile.flip(2)
            else:
                a_tile.rotate(2)
        else:
            if a_top_flip:
                a_tile.flip(1)
    
    @staticmethod
    def assert_top(a_tile: Tile, a_top_should):
        if a_top_should is not None:
            my_top = a_tile.get_side('T')
            assert my_top == a_top_should

    def get_next_tile(self, a_side, a_num):
        """ Get next tile with matches a_side """
        try:
            next_tile_num = [v for v in self.edges[a_side] if v != a_num][0]
        except KeyError:
            next_tile_num = [v for v in self.edges[a_side[::-1]] if v != a_num][0]
        # find side in next tile with no partner
        return self.tiles[next_tile_num]

    def fill_map(self, corners):
        # start with first row and first column (as two constraints known)
        for y in range(self.width):
            for x in range(self.width):
                if x == 0:
                    if y == 0:
                        # pick arbitrary corner to start with
                        this_tile = self.tiles[corners[0]]
                        if this_tile.no_match == [False, True, True, False]:
                            this_tile.flip(2)
                        assert this_tile.no_match == [True, True, False, False]
                    else:
                        # get bottom side of top tile
                        top_tile = self.grid[y-1][x]
                        this_tile = self.get_next_tile(top_tile.get_side('B'), top_tile.num)
                        if y < self.width -1:
                            assert this_tile.no_match.count(True) == 1
                        else:
                            assert this_tile.no_match.count(True) == 2
                        # flip the tile such that left is unmatched and top matches tile above
                        top = this_tile.get_side_type(top_tile.get_side('B'))
                        top_flip = False
                        if top is None:
                            top = this_tile.get_side_type(top_tile.get_side('B')[::-1])
                            top_flip = True
                        self.place_tile_top(this_tile, top, top_flip)
                        # assert that left side is unmatched
                        assert this_tile.no_match[1]
                        if y == self.width - 1:
                            assert this_tile.no_match[2]
                        
                # find matching tile
                else:
                    my_right = this_tile.sides['R']
                    next_tile = self.get_next_tile(my_right, this_tile.num)
                    if y == 0 or y == self.width - 1:
                        if x < self.width - 1:
                            assert next_tile.no_match.count(True) == 1
                        else:
                            assert next_tile.num in corners
                    left = next_tile.get_side_type(my_right)
                    flip_left = False
                    if left is None:
                        left = next_tile.get_side_type(my_right[::-1])
                        flip_left = True
                    # turn/flip tile as required
                    self.place_tile(next_tile, left, flip_left)
                    this_tile = next_tile
                    if y == 0:
                        # check that top is unmatched
                        assert this_tile.no_match.index(True) == this_tile.edge_sort.index('T')
                        # for last tile in line, assert additionally that right is unmatched
                        if x == self.width - 1:
                            assert this_tile.no_match[3]
                self.grid[y][x] = this_tile

    def draw_map(self):
        content_height = len(self.grid[0][0].content)
        for y in range(self.width):
            for sub_y in range(1, content_height-1): # disregard border
                self.image.append(''.join([tile_xi.content[sub_y][1:-1] for tile_xi in self.grid[y]]))
                if self.image_width is None:
                    self.image_width = len(self.image[-1])
    
    def display_map(self):
        for mi in self.image:
            print(mi)

    def rotate_map(self, a_times):
        """ Rotate tile clockwise by a_times*90degrees """
        # clockwise
        new_image = []
        if a_times == 1:
            for j in range(self.image_width):
                new_image.append(''.join([self.image[self.image_width-1-i][j] for i in range(self.image_width)]))
        elif a_times == 2:
            for j in range(self.width):
                new_image.append(''.join([self.image[self.image_width-1-j][self.image_width-1-i] for i in range(self.image_width)]))
        elif a_times == 3:
            for j in range(self.width):
                new_image.append(''.join([self.image[i][self.image_width-1-j] for i in range(self.image_width)]))
        self.image = new_image
    
    def flip_map(self, a_type):
        """ Flip map either via horizonal (a_type=2) or vertical (a_type=1) axis """
        if a_type == 1:
            new_content = []
            for c in self.image:
                new_content.append(c[::-1])
            self.image = new_content
        elif a_type == 2:
            self.image = self.image[::-1]

    def monsters_possible(self, a_regex):
        founds = [False] * len(a_regex)
        for mi in self.image:
            for i in range(len(a_regex)):
                if re.search(a_regex[i], mi) is not None:
                    founds[i] = True
        return False not in founds

def read_data(a_content):
    raw_tiles = {}
    active_tile = None
    for c in a_content:
        if len(c) < 1:
            active_tile = None
        elif 'Tile ' in c:
            active_tile = int(c.split(' ')[1].strip(':'))
            raw_tiles[active_tile] = []
        else:
            raw_tiles[active_tile].append(c)
    r_tiles = {}
    r_edges = {}
    for t, v in raw_tiles.items():
        tile = Tile.new_tile(t, v)
        for side in tile.sides.values():
            if side not in r_edges.keys():
                # try flipped
                if side[::-1] not in r_edges.keys():
                    r_edges[side] = [t]
                else:
                    r_edges[side[::-1]].append(t)
            else:
                r_edges[side].append(t)
        r_tiles[t] = tile
    
    return r_tiles, r_edges

def find_corners(a_edges):
    single_edges = [v for v in a_edges.values() if len(v) == 1]

    corners = []
    for se in single_edges:
        if se[0] not in corners:
            cnt = single_edges.count(se)
            if cnt == 2:
                corners.append(se[0])
                if len(corners) == 4:
                    break
    return corners


if __name__ == '__main__':
    content = day01.load_data('data20.txt')
    tiles, edges = read_data(content)

    # store no match in Tile objects
    for k, v in edges.items():
        if len(v) == 1:
            side_type = tiles[v[0]].get_side_type(k)
            side_idx = Tile.edge_sort.index(side_type)
            tiles[v[0]].no_match[side_idx] = True

    ## part 1: find corner pieces and assemble image
    corners = find_corners(edges)
    tot = 1
    for c in corners:
        tot *= c
    print(f'Part 1: {tot}')

    ## part 2
    m = Map(int(math.sqrt(len(tiles.keys()))), tiles, edges)
    m.fill_map(corners)
    # remove borders
    m.draw_map()

    # describe the sea monster with three regex expressions, length 20 each
    sea_regex = [r'..................#.', 
                 r'#....##....##....###', 
                 r'.#..#..#..#..#..#...']

    # start by finding orientation via sea2
    map_ok = m.monsters_possible(sea_regex)

    if not map_ok:
        # try flipping first
        for flp in range(1, 3):
            m.flip_map(flp)
            rot = 0
            while rot < 4:
                map_ok = m.monsters_possible(sea_regex)
                if map_ok:
                    break
                else:
                    rot += 1
                    m.rotate_map(1)
            if map_ok:
                break

    # actually look for the damn sea monsters (careful, map might be flipped)
    matches = {}
    for j, sea in enumerate(sea_regex):
        matches[j] = []
        for jj, mi in enumerate(m.image):
            sea_matches = re.finditer(fr'(?=({sea}))', mi)  # define lookahead assertion
            x_vals = [match.span(1)[0] for match in sea_matches]
            for x in x_vals:
                matches[j].append((x, jj))
    # for all matches in matches[2], verify that the corresponding match index can be found
    # in matches[1] and matches[0]
    real_matches = []
    attempt = 0
    while len(real_matches) == 0 and attempt < 4:
        if attempt % 2 == 0:
            factor = -1
        else:
            factor = 1
        for ma in matches[2]:
            if (ma[0], ma[1]+1*factor) in matches[1]:
                if (ma[0], ma[1]+2*factor) in matches[0]:
                    real_matches.append(ma)
        attempt += 1
    
    sea_monster_hashes = 15
    all_hashes = sum([len(x.replace('.', '')) for x in m.image])
    print(f'Part 2: {all_hashes - sea_monster_hashes * len(real_matches)}')
