"""White-box tests for main entry flow and input parsing."""

import unittest
from unittest.mock import patch

import main


class TestMainFlowWhiteBox(unittest.TestCase):
    """Covers input parsing and exception branches in entrypoint."""

    def test_name_parsing_trims_and_filters(self):
        with patch("builtins.input", return_value=" Alice, , Bob ,,  Carol "):
            self.assertEqual(main.get_player_names(), ["Alice", "Bob", "Carol"])

    def test_main_handles_keyboard_interrupt(self):
        with patch("main.get_player_names", return_value=["A", "B"]), patch(
            "main.Game"
        ) as game_cls, patch("builtins.print") as print_mock:
            game_cls.return_value.run.side_effect = KeyboardInterrupt
            main.main()
            printed = "\n".join(str(call) for call in print_mock.call_args_list)
            self.assertIn("Game interrupted", printed)


if __name__ == "__main__":
    unittest.main()
