import random

class Tile:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Mahjong:
    suits = ['Bamboo', 'Characters', 'Dots']
    ranks = [str(i) for i in range(1, 10)]

    def __init__(self):
        self.tiles = self.generate_tiles()
        self.player_hand = []

    def generate_tiles(self):
        tiles = []
        for suit in Mahjong.suits:
            for rank in Mahjong.ranks:
                for _ in range(4):  # 4 copies of each tile
                    tiles.append(Tile(suit, rank))
        random.shuffle(tiles)
        return tiles

    def draw_tile(self):
        return self.tiles.pop()

    def deal_hand(self):
        for _ in range(13):
            self.player_hand.append(self.draw_tile())

    def show_hand(self):
        hand = []
        for tile in self.player_hand:
            hand.append(f"{tile.rank} of {tile.suit}")
        return hand

game = Mahjong()
game.deal_hand()
print(game.show_hand())
