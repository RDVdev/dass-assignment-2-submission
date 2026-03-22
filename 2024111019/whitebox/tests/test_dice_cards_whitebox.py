"""White-box tests for dice and card-deck mechanics."""

import unittest
from unittest.mock import patch

from moneypoly.cards import CardDeck
from moneypoly.dice import Dice


class TestDiceWhiteBox(unittest.TestCase):
    """Covers roll bounds, doubles, and reset branches."""

    def test_roll_uses_six_sided_bounds(self):
        die = Dice()

        def expect_six_sided(low, high):
            if (low, high) != (1, 6):
                raise AssertionError(f"Dice bounds must be 1..6, got {(low, high)}")
            return 6

        with patch("moneypoly.dice.random.randint", side_effect=expect_six_sided):
            total = die.roll()
        self.assertEqual(total, 12)

    def test_non_doubles_resets_streak(self):
        die = Dice()
        die.doubles_streak = 2
        die.die1 = 1
        die.die2 = 2
        # Force non-doubles branch without randomness.
        self.assertFalse(die.is_doubles())
        with patch("moneypoly.dice.random.randint", side_effect=[1, 2]):
            die.roll()
        self.assertEqual(die.doubles_streak, 0)


class TestCardDeckWhiteBox(unittest.TestCase):
    """Covers empty, sequential, and wrap-around branches."""

    def test_draw_empty_returns_none(self):
        deck = CardDeck([])
        self.assertIsNone(deck.draw())

    def test_peek_does_not_advance(self):
        cards = [{"id": 1}, {"id": 2}]
        deck = CardDeck(cards)
        first = deck.peek()
        self.assertEqual(first, cards[0])
        self.assertEqual(deck.index, 0)

    def test_draw_wraps_back_to_first(self):
        cards = [{"id": 1}, {"id": 2}]
        deck = CardDeck(cards)
        first = deck.draw()
        second = deck.draw()
        third = deck.draw()
        self.assertEqual(first, cards[0])
        self.assertEqual(second, cards[1])
        self.assertEqual(third, cards[0])


if __name__ == "__main__":
    unittest.main()
