class Cup():
    def __init__(self, a_label):
        self.label = a_label
        self.next_cup = None

    def set_next(self, a_cup):
        self.next_cup = a_cup

class Game():
    def __init__(self, a_content, a_extend=0):
        self.cups = [None] * max(len(a_content)+1, a_extend+1)
        self.max_label = 0
        first = True
        last_cup = None
        for c in a_content:
            my_num = int(c)
            my_cup = Cup(my_num)
            self.cups[my_num] = my_cup
            if first:
                self.current = my_cup  # set current cup
                first = False
            else:
                last_cup.next_cup = my_cup
            if my_cup.label > self.max_label:
                self.max_label = my_cup.label
            last_cup = my_cup
        if a_extend > 0:
            for j in range(self.max_label+1, a_extend+1):
                my_cup = Cup(int(j))
                self.cups[int(j)] = my_cup
                last_cup.next_cup = my_cup
                last_cup = my_cup
            self.max_label = a_extend
        last_cup.next_cup = self.current

    def display(self):
        start = self.current.label
        ll = [start]
        c = self.current.next_cup
        while c.label != start:
            ll.append(c.label)
            c = c.next_cup
        print(ll)

    def play(self, rounds):
        cnt = 0
        while cnt < rounds:
            # pick up three cups
            triple = []
            cup = self.current
            for _ in range(3):
                cup = cup.next_cup
                triple.append(cup)
            
            self.current.next_cup = triple[-1].next_cup
            triple[-1].next_cup = None
            # choose destination
            dest = self.current.label - 1 if self.current.label > 1 else self.max_label
            while dest in [x.label for x in triple]:
                dest -= 1
                if dest <= 0:
                    dest = self.max_label
            dest_cup = self.cups[dest]
            #assert dest_cup.label == dest
            after_dest = dest_cup.next_cup

            # put cups back
            dest_cup.next_cup = triple[0]
            triple[-1].next_cup = after_dest
            self.current = self.current.next_cup
            cnt += 1

    def find_label(self, a_label):
        start = self.current.label
        cup = self.current
        while cup.label != a_label:
            cup = cup.next_cup
            if cup.label == start:
                cup = None
                break
        return cup

    def score_part1(self):
        cup = self.find_label(1)
        a_str = ""
        for _ in range(8):
            cup = cup.next_cup
            a_str += f'{cup.label}'
        return a_str

    def score_part2(self):
        cup = self.find_label(1)
        fac = 1
        for _ in range(2):
            cup = cup.next_cup
            fac *= cup.label
        return fac

if __name__ == '__main__':
    content = "476138259"
    
    ## part 1
    g1 = Game(content)
    g1.play(100)
    print(f'Part 1: {g1.score_part1()}')

    ## part 2... no chance of brute forcing this one!
    g2 = Game(content, a_extend=1000000)
    g2.play(10000000)
    print(f'Part 2: {g2.score_part2()}')
