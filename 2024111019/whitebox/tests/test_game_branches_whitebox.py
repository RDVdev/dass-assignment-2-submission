"""Additional white-box branch tests for card flow and tile handlers."""

import unittest
from unittest.mock import patch

from moneypoly.game import Game


class TestGameBranchesWhiteBox(unittest.TestCase):
    """Covers less-traveled branches in Game methods."""

    def test_apply_card_collect(self):
        game = Game(["A", "B"])
        player = game.players[0]
        before = player.balance
        game._apply_card(player, {"description": "Collect", "action": "collect", "value": 50})
        self.assertEqual(player.balance, before + 50)

    def test_apply_card_pay(self):
        game = Game(["A", "B"])
        player = game.players[0]
        before = player.balance
        game._apply_card(player, {"description": "Pay", "action": "pay", "value": 30})
        self.assertEqual(player.balance, before - 30)

    def test_apply_card_jail(self):
        game = Game(["A", "B"])
        player = game.players[0]
        game._apply_card(player, {"description": "Jail", "action": "jail", "value": 0})
        self.assertTrue(player.in_jail)
        self.assertEqual(player.position, 10)

    def test_apply_card_jail_free(self):
        game = Game(["A", "B"])
        player = game.players[0]
        game._apply_card(player, {"description": "Free", "action": "jail_free", "value": 0})
        self.assertEqual(player.get_out_of_jail_cards, 1)

    def test_move_to_railroad_card_triggers_property_flow(self):
        """Moving to a railroad should route into property handling flow."""
        game = Game(["A", "B"])
        player = game.players[0]
        player.position = 1
        fake_prop = object()
        with patch.object(game.board, "get_property_at", return_value=fake_prop), patch.object(
            game, "_handle_property_tile"
        ) as handle_mock:
            game._card_move_to(player, 5)
        self.assertTrue(handle_mock.called)

    def test_handle_property_tile_skip_branch(self):
        game = Game(["A", "B"])
        player = game.players[0]
        prop = game.board.get_property_at(1)
        with patch("builtins.input", return_value="s"):
            game._handle_property_tile(player, prop)
        self.assertIsNone(prop.owner)

    def test_handle_property_tile_buy_branch(self):
        game = Game(["A", "B"])
        player = game.players[0]
        prop = game.board.get_property_at(1)
        with patch("builtins.input", return_value="b"):
            game._handle_property_tile(player, prop)
        self.assertEqual(prop.owner, player)

    def test_handle_property_tile_auction_branch(self):
        game = Game(["A", "B"])
        player = game.players[0]
        prop = game.board.get_property_at(1)
        with patch("builtins.input", return_value="a"), patch(
            "moneypoly.ui.safe_int_input", side_effect=[0, 0]
        ):
            game._handle_property_tile(player, prop)
        self.assertIsNone(prop.owner)

    def test_check_bankruptcy_releases_properties(self):
        game = Game(["A", "B"])
        player = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = player
        prop.is_mortgaged = True
        player.add_property(prop)
        player.balance = 0
        game._check_bankruptcy(player)
        self.assertNotIn(player, game.players)
        self.assertIsNone(prop.owner)
        self.assertFalse(prop.is_mortgaged)


if __name__ == "__main__":
    unittest.main()
