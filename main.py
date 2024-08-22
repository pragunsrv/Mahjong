import random

class Tile:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

class Mahjong:
    suits = ['Bamboo', 'Characters', 'Dots', 'Winds', 'Dragons']
    ranks = [str(i) for i in range(1, 10)]
    wind_tiles = ['East', 'South', 'West', 'North']
    dragon_tiles = ['Red', 'Green', 'White']

    def __init__(self):
        self.tiles = self.generate_tiles()
        self.player_hand = []
        self.discarded_tiles = []
        self.wall_tiles = self.tiles.copy()

    def generate_tiles(self):
        tiles = []
        for suit in Mahjong.suits[:3]:
            for rank in Mahjong.ranks:
                for _ in range(4):
                    tiles.append(Tile(suit, rank))
        for wind in Mahjong.wind_tiles:
            for _ in range(4):
                tiles.append(Tile('Wind', wind))
        for dragon in Mahjong.dragon_tiles:
            for _ in range(4):
                tiles.append(Tile('Dragon', dragon))
        random.shuffle(tiles)
        return tiles

    def draw_tile(self):
        tile = self.tiles.pop()
        self.wall_tiles.remove(tile)
        return tile

    def deal_hand(self):
        for _ in range(13):
            self.player_hand.append(self.draw_tile())

    def discard_tile(self, tile):
        if tile in self.player_hand:
            self.player_hand.remove(tile)
            self.discarded_tiles.append(tile)

    def show_hand(self):
        return [str(tile) for tile in self.player_hand]

    def show_discarded_tiles(self):
        return [str(tile) for tile in self.discarded_tiles]

    def draw_from_wall(self):
        if len(self.wall_tiles) > 0:
            return self.draw_tile()
        return None

    def check_for_win(self):
        return len(self.player_hand) == 14

    def play_turn(self):
        drawn_tile = self.draw_from_wall()
        if drawn_tile:
            self.player_hand.append(drawn_tile)
            self.discard_tile(self.player_hand[0])
            return self.check_for_win()
        return False

game = Mahjong()
game.deal_hand()

while not game.check_for_win():
    print("Current hand:", game.show_hand())
    print("Discarded tiles:", game.show_discarded_tiles())
    win = game.play_turn()
    if win:
        print("You have a winning hand!")

print("Final hand:", game.show_hand())
