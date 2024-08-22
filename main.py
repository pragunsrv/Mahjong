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
        self.flower_tiles = []
        self.season_tiles = []
        self.players = [self.player_hand, [], [], []]  
        self.current_player = 0

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
        for i in range(1, 5):
            self.flower_tiles.append(Tile('Flower', str(i)))
            self.season_tiles.append(Tile('Season', str(i)))
        tiles.extend(self.flower_tiles * 4)
        tiles.extend(self.season_tiles * 4)
        random.shuffle(tiles)
        return tiles

    def draw_tile(self):
        tile = self.tiles.pop()
        self.wall_tiles.remove(tile)
        return tile

    def deal_hand(self):
        for player in self.players:
            for _ in range(13):
                player.append(self.draw_tile())

    def discard_tile(self, tile):
        if tile in self.players[self.current_player]:
            self.players[self.current_player].remove(tile)
            self.discarded_tiles.append(tile)

    def show_hand(self, player=None):
        if player is None:
            player = self.current_player
        return [str(tile) for tile in self.players[player]]

    def show_discarded_tiles(self):
        return [str(tile) for tile in self.discarded_tiles]

    def draw_from_wall(self):
        if len(self.wall_tiles) > 0:
            return self.draw_tile()
        return None

    def check_for_win(self):
        return len(self.players[self.current_player]) == 14

    def play_turn(self):
        drawn_tile = self.draw_from_wall()
        if drawn_tile:
            self.players[self.current_player].append(drawn_tile)
            self.discard_tile(self.players[self.current_player][0])
            win = self.check_for_win()
            self.current_player = (self.current_player + 1) % 4
            return win
        return False

    def play_game(self):
        self.deal_hand()
        while True:
            print(f"Player {self.current_player + 1}'s turn")
            print("Current hand:", self.show_hand())
            print("Discarded tiles:", self.show_discarded_tiles())
            win = self.play_turn()
            if win:
                print(f"Player {self.current_player + 1} has a winning hand!")
                break
            print("\n" + "-"*20 + "\n")

game = Mahjong()
game.play_game()
