"""White-box tests for bank money movement and safety branches."""

import unittest

from moneypoly.bank import Bank
from moneypoly.player import Player


class TestBankWhiteBox(unittest.TestCase):
    """Covers branch-level behavior in Bank."""

    def test_collect_positive_increases_balance(self):
        bank = Bank()
        before = bank.get_balance()
        bank.collect(100)
        self.assertEqual(bank.get_balance(), before + 100)

    def test_collect_zero_is_noop(self):
        bank = Bank()
        before = bank.get_balance()
        bank.collect(0)
        self.assertEqual(bank.get_balance(), before)

    def test_collect_negative_is_ignored(self):
        bank = Bank()
        before = bank.get_balance()
        bank.collect(-250)
        self.assertEqual(bank.get_balance(), before)

    def test_payout_more_than_funds_raises(self):
        bank = Bank()
        with self.assertRaises(ValueError):
            bank.pay_out(bank.get_balance() + 1)

    def test_give_loan_credits_player(self):
        bank = Bank()
        player = Player("Alice", balance=100)
        bank.give_loan(player, 60)
        self.assertEqual(player.balance, 160)

    def test_give_loan_reduces_bank_funds(self):
        """Method docstring says loaning should reduce bank reserves."""
        bank = Bank()
        player = Player("Alice", balance=100)
        before = bank.get_balance()
        bank.give_loan(player, 60)
        self.assertEqual(bank.get_balance(), before - 60)


if __name__ == "__main__":
    unittest.main()
