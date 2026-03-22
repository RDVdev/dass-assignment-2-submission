"""White-box tests for player state, money flow, and movement branches."""

import unittest

from moneypoly.config import GO_SALARY, STARTING_BALANCE
from moneypoly.player import Player


class TestPlayerWhiteBox(unittest.TestCase):
    """Covers branch-level behavior in Player."""

    def test_default_state(self):
        player = Player("Alice")
        self.assertEqual(player.balance, STARTING_BALANCE)
        self.assertEqual(player.position, 0)
        self.assertFalse(player.in_jail)
        self.assertEqual(player.jail_turns, 0)
        self.assertEqual(player.get_out_of_jail_cards, 0)

    def test_add_negative_raises(self):
        player = Player("Alice")
        with self.assertRaises(ValueError):
            player.add_money(-1)

    def test_deduct_negative_raises(self):
        player = Player("Alice")
        with self.assertRaises(ValueError):
            player.deduct_money(-1)

    def test_bankrupt_boundaries(self):
        self.assertFalse(Player("A", balance=1).is_bankrupt())
        self.assertTrue(Player("B", balance=0).is_bankrupt())
        self.assertTrue(Player("C", balance=-1).is_bankrupt())

    def test_move_without_crossing_go_has_no_salary(self):
        player = Player("Alice", balance=1000)
        player.position = 5
        player.move(4)
        self.assertEqual(player.position, 9)
        self.assertEqual(player.balance, 1000)

    def test_move_landing_on_go_gets_salary(self):
        player = Player("Alice", balance=1000)
        player.position = 35
        player.move(5)
        self.assertEqual(player.position, 0)
        self.assertEqual(player.balance, 1000 + GO_SALARY)

    def test_move_passing_go_gets_salary(self):
        """Expected Monopoly behavior: passing Go should also grant salary."""
        player = Player("Alice", balance=1000)
        player.position = 38
        player.move(5)
        self.assertEqual(player.position, 3)
        self.assertEqual(player.balance, 1000 + GO_SALARY)

    def test_status_line_shows_jail_tag(self):
        player = Player("Alice")
        player.in_jail = True
        self.assertIn("[JAILED]", player.status_line())


if __name__ == "__main__":
    unittest.main()
