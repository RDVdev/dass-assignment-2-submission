"""White-box tests for game flow branches and side-effects."""

import unittest
from unittest.mock import patch

from moneypoly.config import JAIL_FINE
from moneypoly.game import Game


class TestGameWhiteBox(unittest.TestCase):
    """Covers constructor, transactions, jail, and winner logic branches."""

    def test_constructor_rejects_less_than_two_players(self):
        with self.assertRaises(ValueError):
            Game(["OnlyOne"])

    def test_buy_property_with_exact_balance_should_succeed(self):
        game = Game(["A", "B"])
        buyer = game.players[0]
        prop = game.board.get_property_at(1)
        buyer.balance = prop.price
        self.assertTrue(game.buy_property(buyer, prop))

    def test_pay_rent_transfers_money_to_owner(self):
        game = Game(["A", "B"])
        owner = game.players[0]
        tenant = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = owner
        rent = prop.get_rent()
        owner_before = owner.balance
        tenant_before = tenant.balance
        game.pay_rent(tenant, prop)
        self.assertEqual(tenant.balance, tenant_before - rent)
        self.assertEqual(owner.balance, owner_before + rent)

    def test_trade_credits_seller(self):
        game = Game(["A", "B"])
        seller = game.players[0]
        buyer = game.players[1]
        prop = game.board.get_property_at(1)
        prop.owner = seller
        seller.add_property(prop)
        seller_before = seller.balance
        buyer_before = buyer.balance
        self.assertTrue(game.trade(seller, buyer, prop, 100))
        self.assertEqual(seller.balance, seller_before + 100)
        self.assertEqual(buyer.balance, buyer_before - 100)

    def test_find_winner_returns_highest_net_worth(self):
        game = Game(["A", "B", "C"])
        game.players[0].balance = 100
        game.players[1].balance = 500
        game.players[2].balance = 200
        self.assertEqual(game.find_winner(), game.players[1])

    def test_mortgage_does_not_reduce_total_collected_stat(self):
        game = Game(["A", "B"])
        owner = game.players[0]
        prop = game.board.get_property_at(1)
        prop.owner = owner
        owner.add_property(prop)
        before_total = game.bank._total_collected  # white-box assertion of internal metric
        self.assertTrue(game.mortgage_property(owner, prop))
        self.assertGreaterEqual(game.bank._total_collected, before_total)

    def test_voluntary_jail_fine_deducts_player_balance(self):
        game = Game(["A", "B"])
        player = game.players[0]
        player.go_to_jail()
        before = player.balance
        with patch("moneypoly.ui.confirm", return_value=True), patch.object(
            game.dice, "roll", return_value=0
        ), patch.object(game, "_move_and_resolve", return_value=None):
            game._handle_jail_turn(player)
        self.assertEqual(player.balance, before - JAIL_FINE)


if __name__ == "__main__":
    unittest.main()
