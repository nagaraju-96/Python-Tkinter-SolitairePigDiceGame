import unittest
from unittest.mock import patch

from SolitairePigDice import PigDiceGame

class TestPigDiceGame(unittest.TestCase):
    def setUp(self):
        # Initialize the game object for each test case
        self.game = PigDiceGame(2)

    def test_switch_player_normal(self):
        # Test case to check if switching players works normally
        self.game.current_player = 1
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 2, "Switching to the next player should work.")

    def test_switch_player_wraparound(self):
        # Test case to check if switching players wraps around to the first player
        self.game.current_player = 2
        self.game.switch_player()
        self.assertEqual(self.game.current_player, 1, "Switching to the first player after the last one.")

    def test_roll_one(self):
        # Test case to check the behavior when a player rolls a one
        with patch('random.randint', return_value=1), patch('SolitairePigDice.messagebox.showinfo') as mock_showinfo:
            self.game.current_player = 2
            self.game.roll()
            player_data = self.game.players[2]
            self.assertEqual(player_data['round_scores'], [])
            mock_showinfo.assert_called_once_with(
                "Bad Luck!",
                f"Player 2 got 1 Point, score is 0 for this round."
            )

    def test_roll_one_empty_round_scores(self):
        # Test case to check the behavior when a player rolls a one with empty round scores
        with patch('random.randint', return_value=1), patch('SolitairePigDice.messagebox.showinfo') as mock_showinfo:
            self.game.current_player = 1
            self.game.roll()
            player_data = self.game.players[1]
            self.assertEqual(player_data['round_scores'], [])
            mock_showinfo.assert_called_once_with(
                "Bad Luck!",
                f"Player 1 got 1 Point, score is 0 for this round."
            )

    def test_hold_no_winner(self):
        # Test case to check the behavior of holding when there is no winner
        self.game.current_player = 1
        self.game.players[1]["round_scores"] = [2, 3, 4]
        with self.subTest("Test switch_player is called"):
            with patch.object(self.game, "switch_player") as mock_switch_player:
                game_over = self.game.hold()
                self.assertFalse(game_over, "Game over flag should be False when there is no winner.")
                mock_switch_player.assert_called_once()

    def test_hold_winner_exists(self):
        # Test case to check the behavior of holding when a winner exists
        self.game.current_player = 1
        self.game.players[1]["round_scores"] = [5, 5, 5]
        self.game.players[1]["score"] = 95
        self.game.round_winner = None

        with self.subTest("Test get_round_winner is NOT called"):
            with patch.object(self.game, "get_round_winner") as mock_get_round_winner:
                game_over = self.game.hold()
                mock_get_round_winner.assert_not_called()

        with self.subTest("Test round_winner is set"):
            self.assertEqual(self.game.round_winner, 1, "Round winner should be set to the current player.")
            self.assertFalse(game_over, "Game over flag should be False when there is a winner.")

    def test_get_round_winner_single_winner(self):
        # Test case to check the behavior when there is a single winner
        self.game.players[1]["score"] = 10
        self.game.players[2]["score"] = 20

        with patch('random.randint', side_effect=[1, 2]):
            round_winner = self.game.get_round_winner()

        self.assertEqual(round_winner, 2, "There should be a single winner with the highest score.")

    def test_get_round_winner_no_winner(self):
        # Test case to check the behavior when there is no winner
        self.game.players[1]["score"] = 10
        self.game.players[2]["score"] = 10

        with patch('random.randint', side_effect=[1, 2]):
            round_winner = self.game.get_round_winner()

        self.assertIsNone(round_winner, "There should be no winner when scores are equal.")

    def test_get_round_winner_multiple_winners(self):
        # Test case to check the behavior when there are multiple winners
        self.game.players[1]["score"] = 20
        self.game.players[2]["score"] = 20

        with patch('random.randint', side_effect=[1, 2]):
            round_winner = self.game.get_round_winner()

        self.assertIsNone(round_winner, "There should be no winner when there are multiple players with the highest score.")

    def test_reset_game(self):
        # Test case to check the behavior of resetting the game state
        # Set up initial game state
        num_players = 2
        initial_scores = {1: {"score": 10, "current_roll": 3, "round_scores": [3, 4]},
                          2: {"score": 15, "current_roll": 5, "round_scores": [5, 2]}}

        game = PigDiceGame(num_players)
        game.players = initial_scores
        game.current_player = 2
        game.round_winner = 1

        # Call the reset_game method
        game.reset_game()

        # Check if the game state is reset to the initial state
        expected_players = {1: {"score": 0, "current_roll": 0, "round_scores": []},
                            2: {"score": 0, "current_roll": 0, "round_scores": []}}
        
        self.assertEqual(game.players, expected_players, "Players' state should be reset.")
        self.assertEqual(game.current_player, 1, "Current player should be reset to 1.")
        self.assertIsNone(game.round_winner, "Round winner should be reset to None.")

    def test_reset_game_two_players(self):
        # Test case to check the behavior of resetting the game state with 2 players
        num_players = 2
        initial_scores = {1: {"score": 15, "current_roll": 4, "round_scores": [4, 2]},
                          2: {"score": 20, "current_roll": 6, "round_scores": [6, 3]}}

        game = PigDiceGame(num_players)
        game.players = initial_scores
        game.current_player = 2
        game.round_winner = 1

        # Call the reset_game method
        game.reset_game()

        # Check if the game state is reset to the initial state
        expected_players = {1: {"score": 0, "current_roll": 0, "round_scores": []},
                            2: {"score": 0, "current_roll": 0, "round_scores": []}}
        
        self.assertEqual(game.players, expected_players, "Players' state should be reset.")
        self.assertEqual(game.current_player, 1, "Current player should be reset to 1.")
        self.assertIsNone(game.round_winner, "Round winner should be reset to None.")

if __name__ == '__main__':
    unittest.main()
