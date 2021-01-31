import day01

class Game():
    def __init__(self, d1, d2, lvl=1):
        self.game_level = lvl
        self.d1 = d1
        self.d2 = d2
        self.d1_history = []
        self.d2_history = []
        self.round = 0
    
    def game_on(self):
        return len(self.d1) > 0 and len(self.d2) > 0

    def draw_cards(self):
        return self.d1.pop(0), self.d2.pop(0)
    
    def append_cards(self, a_deck, c1, c2):
        if a_deck == 1:
            self.d1.append(c1)
            self.d1.append(c2)
        else:
            self.d2.append(c1)
            self.d2.append(c2)
    
    def game1(self):
        while self.game_on():
            (card1, card2) = self.draw_cards()
            if card1 > card2:
                self.append_cards(1, card1, card2)
            elif card1 < card2:
                self.append_cards(2, card2, card1)

    def score(self):
        if not self.game_on():
            if len(self.d1) == 0:
                deck = self.d2
                winner = 2
            else:
                deck = self.d1
                winner = 1
            score = sum([(len(deck)-j)*x for j, x in enumerate(deck)])
            return score, winner
        else:
            #print(f'Game (level = {self.game_level}) ended prematurely, Winner is Player 1')
            return None, 1

    def game2(self):
        while self.game_on():
            self.round += 1
            # previous game situation check
            if self.d1 in self.d1_history:
                break
            else:
                self.d1_history.append(self.d1[:])
            if self.d2 in self.d2_history:
                break
            else:
                self.d2_history.append(self.d2[:])
            
            (card1, card2) = self.draw_cards()
            
            # sub game
            if len(self.d1) >= card1 and len(self.d2) >= card2:
                win = self.subgame(card1, card2)
                if win == 1:
                    self.append_cards(1, card1, card2)
                else:
                    self.append_cards(2, card2, card1)
            else:
                if card1 > card2:
                    self.append_cards(1, card1, card2)
                elif card1 < card2:
                    self.append_cards(2, card2, card1)


    def subgame(self, card1, card2):
        # define new game object with appropriate decks
        deck1 = [x for x in self.d1[:card1]]
        deck2 = [x for x in self.d2[:card2]]
        g_sub = Game(deck1, deck2, lvl=self.game_level+1)
        g_sub.game2()
        (_, win) = g_sub.score()
        return win

if __name__ == "__main__":
    content = day01.load_data('data22.txt')

    raw_deck1 = []
    raw_deck2 = []
    active = None

    for c in content:
        if 'Player 1' in c:
            active = 1
        elif 'Player 2' in c:
            active = 2
        elif len(c) > 0:
            if active == 1:
                raw_deck1.append(int(c))
            elif active == 2:
                raw_deck2.append(int(c))

    ## part 1
    g = Game(raw_deck1[:], raw_deck2[:])
    g.game1()
    (score, winner) = g.score()
    print(f'Game 1: Player {winner} wins with score {score}')

    ## part 2 (not so fast but it works)
    g = Game(raw_deck1[:], raw_deck2[:])
    g.game2()
    (score, winner) = g.score()
    print(f'Game 2: Player {winner} wins with score: {score}')
