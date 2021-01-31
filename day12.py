import day01

class Ship():
    def __init__(self, a_start, a_face):
        self.pos = a_start
        self.face = a_face

    def grab_vector(self, a_dir):
        vector_dict = {'W': (-1, 0), 'S': (0, -1), 'E': (1, 0), 'N': (0, 1)}
        assert a_dir in vector_dict.keys(), f'Unknown moving direction {a_dir}'
        return vector_dict[a_dir]

    def turn_face(self, a_dir, a_val):
        assert a_dir in ['R', 'L'], f'Unknown turning direction {a_dir}'
        turn_idx = a_val // 90
        turn_idx = turn_idx if a_dir == 'L' else -turn_idx
        face_order = ['E', 'N', 'W', 'S']
        new_idx = (face_order.index(self.face) + turn_idx + 4) % 4
        self.face = face_order[new_idx]
        
    def move(self, a_dir, val):
        if a_dir == 'F':
            my_dir = self.grab_vector(self.face)
        else:
            my_dir = self.grab_vector(a_dir)
        
        self.pos[0] += my_dir[0] * val
        self.pos[1] += my_dir[1] * val

    def do(self, a_cmd):
        (instr, val) = decipher(a_cmd)
        val = int(a_cmd[1:])
        if instr in ['L', 'R']:
            self.turn_face(instr, val)
        else:
            self.move(instr, val)

    def move_to(self, dx, dy):
        self.pos[0] = dx
        self.pos[1] = dy
        #print(self.pos)

class ShipWP(Ship):
    def __init__(self, a_start, a_face, a_wp):
        super().__init__(a_start, a_face)
        self.wp = a_wp

    def move_wp(self, a_dx, a_dy):
        self.wp[0] += a_dx
        self.wp[1] += a_dy
    
    def move(self, a_dir, val):
        if a_dir == 'F':
            dx = (self.wp[0]-self.pos[0]) * val
            dy = (self.wp[1]-self.pos[1]) * val
            self.pos[0] += dx
            self.pos[1] += dy
            self.move_wp(dx, dy)
        else:
            my_dir = self.grab_vector(a_dir)
            self.move_wp(my_dir[0] * val, my_dir[1] * val)
        
    def turn_face(self, a_dir, val):
        """ turn waypoint """
        val = val // 90
        dxi = self.wp[0] - self.pos[0]
        dyi = self.wp[1] - self.pos[1]
        #print(dxi, dyi)
        if val == 2:
            dx = -2*dxi
            dy = -2*dyi
        elif (val == 1 and a_dir == 'L') or (val == 3 and a_dir == 'R'):
            dx = -dxi-dyi
            dy = -dyi+dxi
        else:
            dx = -dxi+dyi
            dy = -dyi-dxi
        self.move_wp(dx, dy)

def decipher(a_cmd):
    instr = a_cmd[0]
    val = int(a_cmd[1:])
    return instr, val

if __name__ == '__main__':
    content = day01.load_data('data12.txt')

    ## part 1
    ship = Ship([0, 0], 'E')
    for cmd in content:
        ship.do(cmd)
    print(f'Current ship position: {ship.pos} (Manhatten distance form start = {abs(ship.pos[0]) + abs(ship.pos[1])})')

    ## part 2
    ship = ShipWP([0, 0], 'E', [10, 1])
    for cmd in content:
        ship.do(cmd)
    print(f'Current ship position: {ship.pos} (Manhatten distance form start = {abs(ship.pos[0]) + abs(ship.pos[1])})')
