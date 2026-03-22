"""White-box tests for property, group, and board branches."""

import unittest

from moneypoly.board import Board
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup


class TestPropertyGroupWhiteBox(unittest.TestCase):
    """Covers ownership and rent multiplier branches."""

    def test_partial_group_is_not_full_ownership(self):
        group = PropertyGroup("Brown", "brown")
        p1 = Property("P1", 1, (60, 2), group)
        Property("P2", 3, (60, 4), group)
        owner = Player("Owner")
        p1.owner = owner
        self.assertFalse(group.all_owned_by(owner))

    def test_full_group_doubles_rent(self):
        group = PropertyGroup("Brown", "brown")
        p1 = Property("P1", 1, (60, 2), group)
        p2 = Property("P2", 3, (60, 4), group)
        owner = Player("Owner")
        p1.owner = owner
        p2.owner = owner
        self.assertEqual(p1.get_rent(), 4)

    def test_mortgaged_property_has_zero_rent(self):
        p = Property("P", 1, (60, 2))
        p.is_mortgaged = True
        self.assertEqual(p.get_rent(), 0)


class TestBoardWhiteBox(unittest.TestCase):
    """Covers board tile routing and purchasability branches."""

    def test_tile_type_resolution(self):
        board = Board()
        self.assertEqual(board.get_tile_type(0), "go")
        self.assertEqual(board.get_tile_type(10), "jail")
        self.assertEqual(board.get_tile_type(1), "property")
        self.assertEqual(board.get_tile_type(28), "blank")

    def test_purchasable_requires_unowned_and_unmortgaged(self):
        board = Board()
        prop = board.get_property_at(1)
        self.assertTrue(board.is_purchasable(1))
        prop.owner = Player("Owner")
        self.assertFalse(board.is_purchasable(1))
        prop.owner = None
        prop.is_mortgaged = True
        self.assertFalse(board.is_purchasable(1))


if __name__ == "__main__":
    unittest.main()
