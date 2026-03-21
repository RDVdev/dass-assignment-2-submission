> **Note:** An empty `__init__.py` must exist inside `moneypoly/moneypoly/` for pylint to resolve package imports.

---

## Initial Pylint Score: **9.08 / 10**

---

## Iteration 1 – Missing Docstrings (C0114, C0115, C0116)

**Score after fix: 9.08 → 9.30 / 10 (+0.21)**

### What Are These Warnings?

| Code | Name | Meaning |
|------|------|---------|
| **C0114** | `missing-module-docstring` | Every Python module (`.py` file) should begin with a docstring explaining its purpose |
| **C0115** | `missing-class-docstring` | Every class definition should have a docstring describing its role |
| **C0116** | `missing-function-docstring` | Every public function/method should have a docstring describing what it does |

Docstrings are triple-quoted strings (`"""..."""`) placed immediately after a module, class, or function definition. They serve as built-in documentation accessible via `help()` and documentation generators.

### Pylint Warnings Found (14 total)

| # | File | Line | Pylint Code | Warning Message |
|---|------|------|-------------|-----------------|
| 1 | `main.py` | 1 | C0114 | Missing module docstring |
| 2 | `main.py` | 4 | C0116 | Missing function docstring (`get_player_names`) |
| 3 | `main.py` | 11 | C0116 | Missing function docstring (`main`) |
| 4 | `config.py` | 1 | C0114 | Missing module docstring |
| 5 | `bank.py` | 1 | C0114 | Missing module docstring |
| 6 | `bank.py` | 5 | C0115 | Missing class docstring (`Bank`) |
| 7 | `dice.py` | 1 | C0114 | Missing module docstring |
| 8 | `player.py` | 1 | C0114 | Missing module docstring |
| 9 | `property.py` | 1 | C0114 | Missing module docstring |
| 10 | `property.py` | 64 | C0115 | Missing class docstring (`PropertyGroup`) |
| 11 | `board.py` | 1 | C0114 | Missing module docstring |
| 12 | `cards.py` | 1 | C0114 | Missing module docstring |
| 13 | `game.py` | 1 | C0114 | Missing module docstring |
| 14 | `ui.py` | 1 | C0114 | Missing module docstring |

### Fixes Applied

#### `main.py`
**3 warnings fixed:** C0114, C0116 (×2)

Added a module-level docstring and docstrings for both public functions.

```diff
+"""Main Start for Moneypoly Game."""
+
 from moneypoly.game import Game

 def get_player_names():
+    """Takes user input for player names, returns a list of names."""
     ...

 def main():
+    """Makes game with given names and runs it."""
     ...
```

#### `config.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""Game configuration constants for MoneyPoly."""
+
 STARTING_BALANCE = 1500
```

#### `bank.py`
**2 warnings fixed:** C0114, C0115

Added a module-level docstring and a class docstring for `Bank`.

```diff
+"""Bank module for the game manages funds loans and taxes."""
+
 import math
 ...

 class Bank:
+    """Bank holds reserves, issues loans, and collects payments from players."""
     def __init__(self):
```

#### `dice.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""Dice module simulates rolling two (out of six) dice."""
+
 import random
```

#### `player.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""Player module defines a player in the game, tracking their name, balance, position, properties, and jail status."""
+
 import sys
```

#### `property.py`
**2 warnings fixed:** C0114, C0115

Added a module-level docstring and a class docstring for `PropertyGroup`.

```diff
+"""Property module defines property colour groups, their rents and rules."""
+
 class Property:
     ...

 class PropertyGroup:
+   """Represents a group of properties that share a color and have special rent rules when fully owned as a group."""
     def __init__(self, name, color):
```

#### `board.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""Board module defines and sllows query to the 40-tile moneypoly board."""
+
 from moneypoly.property import Property, PropertyGroup
```

#### `cards.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""Cards module defines the Chance and Community Chest cards and their effects and contains the deck logic"""

+
 import random
```

#### `game.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""Main game module runs the game loop and contains the game logic."""
+
 import os
```

#### `ui.py`
**1 warning fixed:** C0114

Added a module-level docstring.

```diff
+"""ui module contains printing banner and setup to make the game better looking and easier to interact with."""
+
 def print_banner(title):
```

### Summary

| Metric | Value |
|--------|-------|
| Warnings fixed | 14 |
| Files modified | 10 |
| Warning types resolved | C0114 (×9), C0115 (×2), C0116 (×3) |
| Score improvement | +0.21 (9.08 → 9.30) |

---

## Iteration 2 – Unused Imports & Variables (W0611, W0612)

**Score after fix: 9.30 → 9.38 / 10 (+0.08)**

### What Are These Warnings?

| Code | Name | Meaning |
|------|------|---------|
| **W0611** | `unused-import` | A module or name is imported but never used anywhere in the file |
| **W0612** | `unused-variable` | A variable is assigned a value but is never read or referenced |

Unused imports clutter the namespace, mislead readers into thinking the imported module is needed, and can slightly slow down module loading. Unused variables indicate dead code — often a leftover from refactoring — that adds confusion without contributing anything.

### Pylint Warnings Found (6 total)

| # | File | Line | Pylint Code | Warning Message |
|---|------|------|-------------|-----------------|
| 1 | `bank.py` | 1 | W0611 | Unused `import math` |
| 2 | `dice.py` | 2 | W0611 | Unused `BOARD_SIZE` imported from `moneypoly.config` |
| 3 | `player.py` | 1 | W0611 | Unused `import sys` |
| 4 | `player.py` | 45 | W0612 | Unused variable `old_position` |
| 5 | `game.py` | 1 | W0611 | Unused `import os` |
| 6 | `game.py` | 3 | W0611 | Unused `GO_TO_JAIL_POSITION` imported from `moneypoly.config` |

### Fixes Applied

#### `bank.py`
**1 warning fixed:** W0611

Removed `import math` — the `math` module was imported but never used anywhere in the file.

```diff

-import math
 from moneypoly.config import BANK_STARTING_FUNDS
```

#### `dice.py`
**1 warning fixed:** W0611

Removed `from moneypoly.config import BOARD_SIZE` — the `BOARD_SIZE` constant was imported but never referenced in the dice module.

```diff

 import random
-from moneypoly.config import BOARD_SIZE
```

#### `player.py`
**2 warnings fixed:** W0611, W0612

1. Removed `import sys` — the `sys` module was imported but never used.
2. Removed the variable `old_position` in `move()` — it was assigned `self.position` but never read afterwards.

```diff

-import sys
 from moneypoly.config import STARTING_BALANCE, BOARD_SIZE, GO_SALARY, JAIL_POSITION
```

```diff
     def move(self, steps):
         ...
-        old_position = self.position
         self.position = (self.position + steps) % BOARD_SIZE
```

#### `game.py`
**2 warnings fixed:** W0611 (×2)

1. Removed `import os` — the `os` module was imported but never used.
2. Removed `GO_TO_JAIL_POSITION` from the config import — it was imported but the code uses the string `"go_to_jail"` tile type instead.

```diff
 
-import os
-
 from moneypoly.config import (
-    GO_TO_JAIL_POSITION,
     JAIL_FINE,
     AUCTION_MIN_INCREMENT,
     ...
```

### Summary

| Metric | Value |
|--------|-------|
| Warnings fixed | 6 |
| Files modified | 4 (`bank.py`, `dice.py`, `player.py`, `game.py`) |
| Warning types resolved | W0611 (×5), W0612 (×1) |
| Score improvement | +0.08 (9.30 → 9.38) |

---

## Iteration 3 – Code Style & Formatting (C0301, C0304, C0121, C0325, W1309)

**Score after fix: 9.38 → 9.85 / 10 (+0.47)**

### What Are These Warnings?

| Code | Name | Meaning |
|------|------|---------|
| **C0301** | `line-too-long` | A line exceeds 100 characters (pylint's default limit) |
| **C0304** | `missing-final-newline` | The file does not end with a newline character |
| **C0121** | `singleton-comparison` | Using `== True` or `== False` instead of truthiness checks or `is True` |
| **C0325** | `superfluous-parens` | Unnecessary parentheses after a keyword like `not` |
| **W1309** | `f-string-without-interpolation` | An f-string is used but contains no `{…}` expressions |

### Pylint Warnings Found (30 total)

| # | File | Line | Pylint Code | Warning Message |
|---|------|------|-------------|-----------------|
| 1–24 | `cards.py` | 6–32 | C0301 | 24 lines exceeding 100 characters |
| 25 | `player.py` | 87 | C0304 | Missing final newline |
| 26 | `game.py` | 467 | C0304 | Missing final newline |
| 27 | `board.py` | 110 | C0121 | `prop.is_mortgaged == True` — singleton comparison |
| 28 | `game.py` | 452 | C0325 | Superfluous parens after `not` |
| 29 | `game.py` | 461 | C0325 | Superfluous parens after `not` |
| 30 | `game.py` | 380 | W1309 | f-string `f"GAME OVER"` has no interpolation |

### Fixes Applied

#### `cards.py`
**24 warnings fixed:** C0301 (×24)

All card definitions used single-line dicts padded with spaces to align columns, causing every line to exceed 100 characters. Reformatted each dict to split the `"description"` key onto its own line, with `"action"` and `"value"` on the next line.

```diff
 CHANCE_CARDS = [
-    {"description": "Advance to Go. Collect $200.",                          "action": "move_to",  "value": 0},
+    {"description": "Advance to Go. Collect $200.",
+     "action": "move_to", "value": 0},
     ...  # same pattern applied to all 24 card entries
 ]
```

#### `board.py`
**1 warning fixed:** C0121

Changed `== True` to a simple truthiness check. Using `== True` can yield surprising results with non-boolean truthy values and is considered non-Pythonic.

```diff
-        if prop.is_mortgaged == True:
+        if prop.is_mortgaged:
             return False
```

#### `player.py`
**1 warning fixed:** C0304

Added a trailing newline at the end of the file. POSIX defines a "line" as a sequence ending with a newline, so the last line of every file should end with one.

#### `game.py`
**4 warnings fixed:** C0304, C0325 (×2), W1309

1. **W1309** — Changed `f"GAME OVER"` to `"GAME OVER"`. There are no `{…}` placeholders, so the `f` prefix is unnecessary.

```diff
-            ui.print_banner(f"GAME OVER")
+            ui.print_banner("GAME OVER")
```

2. **C0325 (×2)** — Removed superfluous parentheses around the chained comparison after `not`. Python's operator precedence already handles `not 0 <= idx < len(…)` correctly without extra parens.

```diff
-        if not (0 <= idx < len(others)):
+        if not 0 <= idx < len(others):
```

```diff
-        if not (0 <= pidx < len(player.properties)):
+        if not 0 <= pidx < len(player.properties):
```

3. **C0304** — Added a trailing newline at end of file.

### Summary

| Metric | Value |
|--------|-------|
| Warnings fixed | 30 |
| Files modified | 4 (`cards.py`, `board.py`, `player.py`, `game.py`) |
| Warning types resolved | C0301 (×24), C0304 (×2), C0121 (×1), C0325 (×2), W1309 (×1) |
| Score improvement | +0.47 (9.38 → 9.85) |

---

## Iteration 4 – Control Flow & Error Handling (R1705, R1723, W0702, W0201)

**Score after fix: 9.85 → 9.91 / 10 (+0.06)**

### What Are These Warnings?

| Code | Name | Meaning |
|------|------|---------|
| **R1705** | `no-else-return` | An `else` block follows a `return` statement — the `else` is unnecessary since `return` already exits the function |
| **R1723** | `no-else-break` | An `elif` follows a `break` — the `elif` can be a plain `if` since `break` already exits the loop |
| **W0702** | `bare-except` | Using `except:` without specifying an exception type catches everything including `KeyboardInterrupt` and `SystemExit` |
| **W0201** | `attribute-defined-outside-init` | An instance attribute is first defined in a method other than `__init__`, making the class schema harder to understand at a glance |

### Pylint Warnings Found (4 total)

| # | File | Line | Pylint Code | Warning Message |
|---|------|------|-------------|-----------------|
| 1 | `property.py` | 51 | R1705 | Unnecessary `else` after `return` in `unmortgage()` |
| 2 | `game.py` | 401 | R1723 | Unnecessary `elif` after `break` in `interactive_menu()` |
| 3 | `ui.py` | 72 | W0702 | No exception type(s) specified (bare except) |
| 4 | `dice.py` | 26 | W0201 | `doubles_streak` defined outside `__init__` |

### Fixes Applied

#### `property.py`
**1 warning fixed:** R1705

Removed the unnecessary `else` after `return 0` in `unmortgage()` and de-indented the code block. After a `return`, execution cannot continue, so `else` is dead syntax that adds needless indentation depth.

```diff
     def unmortgage(self):
         if not self.is_mortgaged:
             return 0
-        else:
-            cost = int(self.mortgage_value * 1.1)
-            self.is_mortgaged = False
-            return cost
+        cost = int(self.mortgage_value * 1.1)
+        self.is_mortgaged = False
+        return cost
```

#### `game.py`
**1 warning fixed:** R1723

Changed `elif` to `if` after `break` in `interactive_menu()`. Since `break` exits the loop, the `elif` can never be reached via fall-through from the `break` branch — so `if` is semantically equivalent and removes misleading coupling.

```diff
             if choice == 0:
                 break
-            elif choice == 1:
+            if choice == 1:
                 ui.print_standings(self.players)
```

#### `ui.py`
**1 warning fixed:** W0702

Changed `except:` to `except ValueError:` in `safe_int_input()`. A bare `except` catches *every* exception — including `KeyboardInterrupt` (Ctrl+C) and `SystemExit` — which should normally propagate. Since `int()` only raises `ValueError` on bad input, that is the only exception we need to catch.

```diff
     try:
         return int(input(prompt))
-    except:
+    except ValueError:
         return default
```

#### `dice.py`
**1 warning fixed:** W0201

Replaced `self.reset()` with `self.doubles_streak = 0` directly in `__init__()`. Pylint expects all instance attributes to be visible in `__init__` so readers can see the full object shape in one place. Calling `self.reset()` set the attribute indirectly, but pylint could not trace through the method call.

```diff
     def __init__(self):
         self.die1 = 0
         self.die2 = 0
-        self.reset()
+        self.doubles_streak = 0
```

> **Note:** The `reset()` method still exists and works correctly when called later — it just no longer needs to be the initial setter.

### Summary

| Metric | Value |
|--------|-------|
| Warnings fixed | 4 |
| Files modified | 4 (`property.py`, `game.py`, `ui.py`, `dice.py`) |
| Warning types resolved | R1705 (×1), R1723 (×1), W0702 (×1), W0201 (×1) |
| Score improvement | +0.06 (9.85 → 9.91) |

