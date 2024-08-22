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
        self.flower_tiles = []
        self.season_tiles = []
        self.players = [[] for _ in range(4)]
        self.discarded_tiles = []
        self.wall_tiles = self.tiles.copy()
        self.current_player = 0
        self.turn_count = 0
        self.melds = [[] for _ in range(4)]
        self.kongs = [[] for _ in range(4)]
        self.flowers = [[] for _ in range(4)]
        self.points = [0, 0, 0, 0]
        self.winning_tiles = []

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
                self.check_special_tiles(player, player[-1])

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

    def check_special_tiles(self, player, tile):
        if tile.suit == 'Flower' or tile.suit == 'Season':
            player.remove(tile)
            self.flowers[self.players.index(player)].append(tile)
            player.append(self.draw_from_wall())

    def add_to_meld(self, player, tiles):
        if len(tiles) == 3:
            self.melds[self.players.index(player)].append(tiles)
            for tile in tiles:
                player.remove(tile)

    def add_to_kong(self, player, tiles):
        if len(tiles) == 4:
            self.kongs[self.players.index(player)].append(tiles)
            for tile in tiles:
                player.remove(tile)
    def degenerate_tiles(self):
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
    def calculate_points(self, player):
        points = 0
        points += len(self.melds[player]) * 2
        points += len(self.kongs[player]) * 8
        points += len(self.flowers[player]) * 4
        self.points[player] = points
        return points

    def play_turn(self):
        drawn_tile = self.draw_from_wall()
        if drawn_tile:
            self.players[self.current_player].append(drawn_tile)
            self.check_special_tiles(self.players[self.current_player], drawn_tile)
            self.discard_tile(self.players[self.current_player][0])
            win = self.check_for_win()
            if win:
                self.winning_tiles.append(drawn_tile)
            self.current_player = (self.current_player + 1) % 4
            self.turn_count += 1
            return win
        return False

    def play_game(self):
        self.deal_hand()
        while True:
            print(f"Player {self.current_player + 1}'s turn")
            print("Current hand:", self.show_hand())
            print("Discarded tiles:", self.show_discarded_tiles())
            print("Melds:", self.melds[self.current_player])
            print("Kongs:", self.kongs[self.current_player])
            print("Flowers:", self.flowers[self.current_player])
            win = self.play_turn()
            if win:
                print(f"Player {self.current_player + 1} has a winning hand!")
                break
            print("\n" + "-"*20 + "\n")
            if self.turn_count >= 100:
                print("Game ends in a draw due to too many turns.")
                break
        for i in range(4):
            print(f"Player {i + 1} scored {self.calculate_points(i)} points.")
        winning_player = self.points.index(max(self.points))
        print(f"Player {winning_player + 1} wins the game with {self.points[winning_player]} points!")

game = Mahjong()
game.play_game()
