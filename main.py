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
        self.turn_history = []
        self.special_rules = {"heavenly_hand": False, "earthly_hand": False, "thirteen_orphans": False}
        self.play_log = []
        self.strategy_mode = False
        self.strategy_info = []
        self.dealer_tiles = [None] * 4
        self.current_dealer = 0
        self.replacement_tiles = [None] * 4
        self.num_draws = 0
        self.round_wins = [0] * 4
        self.rounds_played = 0
        self.max_rounds = 4
        self.highest_score = [0, 0, 0, 0]
        self.card_counts = {suit: {rank: 0 for rank in Mahjong.ranks} for suit in Mahjong.suits}
        self.suit_frequency = {suit: 0 for suit in Mahjong.suits}
        self.rank_frequency = {rank: 0 for rank in Mahjong.ranks}
        self.special_hand_counts = { "all_pong": 0, "pure_triplets": 0 }
        self.opponent_strategies = [self.default_strategy] * 3
        self.game_statistics = {'turns': 0, 'draws': 0, 'discards': 0}

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
        self.game_statistics['draws'] += 1
        return tile

    def deal_hand(self):
        for player in self.players:
            for _ in range(13):
                tile = self.draw_tile()
                player.append(tile)
                self.check_special_tiles(player, tile)

    def discard_tile(self, tile):
        if tile in self.players[self.current_player]:
            self.players[self.current_player].remove(tile)
            self.discarded_tiles.append(tile)
            self.turn_history.append((self.current_player, tile))
            self.game_statistics['discards'] += 1
            self.log_play(f"Player {self.current_player + 1} discarded {tile}")

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
            self.log_play(f"Player {self.players.index(player) + 1} drew a {tile.suit} tile and replaced it")

    def add_to_meld(self, player, tiles):
        if len(tiles) == 3:
            self.melds[self.players.index(player)].append(tiles)
            for tile in tiles:
                player.remove(tile)
            self.log_play(f"Player {self.players.index(player) + 1} formed a meld with {tiles}")

    def add_to_kong(self, player, tiles):
        if len(tiles) == 4:
            self.kongs[self.players.index(player)].append(tiles)
            for tile in tiles:
                player.remove(tile)
            self.log_play(f"Player {self.players.index(player) + 1} formed a kong with {tiles}")

    def calculate_points(self, player):
        points = 0
        points += len(self.melds[player]) * 2
        points += len(self.kongs[player]) * 8
        points += len(self.flowers[player]) * 4
        if self.special_rules["heavenly_hand"] and player == 0 and self.turn_count == 0:
            points += 100
        if self.special_rules["earthly_hand"] and player == 0 and self.turn_count == 1:
            points += 50
        if self.check_thirteen_orphans(player):
            points += 200
            self.special_rules["thirteen_orphans"] = True
        self.points[player] = points
        self.update_highest_score(player, points)
        return points

    def check_special_rules(self):
        if self.turn_count == 0 and self.check_for_win():
            self.special_rules["heavenly_hand"] = True
        if self.turn_count == 1 and self.check_for_win():
            self.special_rules["earthly_hand"] = True

    def check_thirteen_orphans(self, player):
        necessary_tiles = [
            Tile('Characters', '1'), Tile('Characters', '9'),
            Tile('Bamboo', '1'), Tile('Bamboo', '9'),
            Tile('Dots', '1'), Tile('Dots', '9'),
            Tile('Wind', 'East'), Tile('Wind', 'South'),
            Tile('Wind', 'West'), Tile('Wind', 'North'),
            Tile('Dragon', 'Red'), Tile('Dragon', 'Green'),
            Tile('Dragon', 'White')
        ]
        hand_tiles = self.players[player]
        for necessary_tile in necessary_tiles:
            if not any(str(necessary_tile) == str(tile) for tile in hand_tiles):
                return False
        return True

    def log_play(self, message):
        self.play_log.append(message)

    def activate_strategy_mode(self):
        self.strategy_mode = True
        self.log_play("Strategy mode activated.")
        self.analyze_player_hands()

    def deactivate_strategy_mode(self):
        self.strategy_mode = False
        self.log_play("Strategy mode deactivated.")

    def analyze_player_hands(self):
        for i, player in enumerate(self.players):
            possible_melds = self.find_possible_melds(player)
            possible_kongs = self.find_possible_kongs(player)
            self.strategy_info.append({
                "player": i + 1,
                "possible_melds": possible_melds,
                "possible_kongs": possible_kongs,
                "hand": [str(tile) for tile in player]
            })
            self.log_play(f"Player {i + 1} has {len(possible_melds)} possible meld(s) and {len(possible_kongs)} possible kong(s).")

    def find_possible_melds(self, player):
        possible_melds = []
        tile_counts = {}
        for tile in player:
            key = (tile.suit, tile.rank)
            if key not in tile_counts:
                tile_counts[key] = 0
            tile_counts[key] += 1
        for (suit, rank), count in tile_counts.items():
            if count >= 3:
                possible_melds.append([Tile(suit, rank)] * 3)
        return possible_melds

    def find_possible_kongs(self, player):
        possible_kongs = []
        tile_counts = {}
        for tile in player:
            key = (tile.suit, tile.rank)
            if key not in tile_counts:
                tile_counts[key] = 0
            tile_counts[key] += 1
        for (suit, rank), count in tile_counts.items():
            if count >= 4:
                possible_kongs.append([Tile(suit, rank)] * 4)
        return possible_kongs

    def suggest_discard(self):
        if not self.players[self.current_player]:
            return None
        possible_melds = self.find_possible_melds(self.players[self.current_player])
        possible_kongs = self.find_possible_kongs(self.players[self.current_player])
        for tile in self.players[self.current_player]:
            if self.is_tile_safe_to_discard(tile, possible_melds, possible_kongs):
                return tile
        return None

    def is_tile_safe_to_discard(self, tile, possible_melds, possible_kongs):
        for meld in possible_melds:
            if tile in meld:
                return False
        for kong in possible_kongs:
            if tile in kong:
                return False
        return True

    def play_turn(self):
        drawn_tile = self.draw_from_wall()
        if drawn_tile:
            self.players[self.current_player].append(drawn_tile)
            self.check_special_tiles(self.players[self.current_player], drawn_tile)
            self.log_play(f"Player {self.current_player + 1} drew {drawn_tile}")
            suggested_discard = self.suggest_discard()
            if suggested_discard:
                self.discard_tile(suggested_discard)
            else:
                self.discard_tile(self.players[self.current_player][0])
            win = self.check_for_win()
            self.check_special_rules()
            if win:
                self.winning_tiles.append(drawn_tile)
                self.log_play(f"Player {self.current_player + 1} wins with a winning tile {drawn_tile}")
                self.round_wins[self.current_player] += 1
                self.reset_round()
            self.current_player = (self.current_player + 1) % 4
            self.turn_count += 1
            self.game_statistics['turns'] += 1
            return win
        return False

    def reset_round(self):
        self.turn_count = 0
        self.discarded_tiles.clear()
        self.current_dealer = (self.current_dealer + 1) % 4
        self.players = [[] for _ in range(4)]
        self.deal_hand()
        self.log_play("Round reset completed.")

    def play_game(self):
        while self.rounds_played < self.max_rounds:
            self.deal_hand()
            while True:
                print(f"Player {self.current_player + 1}'s turn")
                print("Current hand:", self.show_hand())
                print("Discarded tiles:", self.show_discarded_tiles())
                print("Melds:", self.melds[self.current_player])
                print("Kongs:", self.kongs[self.current_player])
                print("Flowers:", self.flowers[self.current_player])
                if not self.strategy_mode:
                    self.activate_strategy_mode()
                win = self.play_turn()
                if win:
                    print(f"Player {self.current_player + 1} has won this round!")
                    break
            self.rounds_played += 1
        self.display_final_scores()

    def display_final_scores(self):
        for i, points in enumerate(self.points):
            print(f"Player {i + 1} scored {points} points")
        for i, wins in enumerate(self.round_wins):
            print(f"Player {i + 1} won {wins} rounds")
        self.log_play("Final scores displayed.")

    def start(self):
        self.play_game()

    def update_highest_score(self, player, points):
        if points > self.highest_score[player]:
            self.highest_score[player] = points
            self.log_play(f"Player {player + 1} set a new highest score of {points}")

    def track_tile_frequency(self):
        self.card_counts = {suit: {rank: 0 for rank in Mahjong.ranks} for suit in Mahjong.suits}
        for suit in Mahjong.suits:
            for rank in Mahjong.ranks:
                self.card_counts[suit][rank] = sum(tile.rank == rank for tile in self.wall_tiles if tile.suit == suit)

    def track_suit_frequency(self):
        self.suit_frequency = {suit: sum(tile.suit == suit for tile in self.wall_tiles) for suit in Mahjong.suits}

    def track_rank_frequency(self):
        self.rank_frequency = {rank: sum(tile.rank == rank for tile in self.wall_tiles) for rank in Mahjong.ranks}
    def show_hand_(self, player=None):
        if player is None:
            player = self.current_player
        return [str(tile) for tile in self.players[player]]

    def show_discarrded_tiles(self):
        return [str(tile) for tile in self.discarded_tiles]

    def draw_from_walll(self):
        if len(self.wall_tiles) > 0:
            return self.draw_tile()
        return None

    def check_for_wiin(self):
        return len(self.players[self.current_player]) == 14

    def check_special_tiiles(self, player, tile):
        if tile.suit == 'Flower' or tile.suit == 'Season':
            player.remove(tile)
            self.flowers[self.players.index(player)].append(tile)
            player.append(self.draw_from_wall())
            self.log_play(f"Player {self.players.index(player) + 1} drew a {tile.suit} tile and replaced it")

    def add_to_melld(self, player, tiles):
        if len(tiles) == 3:
            self.melds[self.players.index(player)].append(tiles)
            for tile in tiles:
                player.remove(tile)
            self.log_play(f"Player {self.players.index(player) + 1} formed a meld with {tiles}")

    def add_to_kongg(self, player, tiles):
        if len(tiles) == 4:
            self.kongs[self.players.index(player)].append(tiles)
            for tile in tiles:
                player.remove(tile)
            self.log_play(f"Player {self.players.index(player) + 1} formed a kong with {tiles}")

    def calculate_poiints(self, player):
        points = 0
        points += len(self.melds[player]) * 2
        points += len(self.kongs[player]) * 8
        points += len(self.flowers[player]) * 4
        if self.special_rules["heavenly_hand"] and player == 0 and self.turn_count == 0:
            points += 100
        if self.special_rules["earthly_hand"] and player == 0 and self.turn_count == 1:
            points += 50
        if self.check_thirteen_orphans(player):
            points += 200
            self.special_rules["thirteen_orphans"] = True
        self.points[player] = points
        self.update_highest_score(player, points)
        return points
    def update_speciial_hand_counts(self, player):
        hand = self.players[player]
        all_pong = all(tile.rank in ['1', '9'] for tile in hand) and len(hand) == 14
        if all_pong:
            self.special_hand_counts["all_pong"] += 1
            self.log_play(f"Player {player + 1} has an all-pong hand.")
        pure_triplets = all(tile.suit == 'Characters' and tile.rank in ['1', '9'] for tile in hand)
        if pure_triplets:
            self.special_hand_counts["pure_triplets"] += 1
            self.log_play(f"Player {player + 1} has a pure triplets hand.")

    def default_strategy(self, player):
        if self.strategy_mode:
            return self.suggest_discard()
        return None

if __name__ == "__main__":
    game = Mahjong()
    game.start()
