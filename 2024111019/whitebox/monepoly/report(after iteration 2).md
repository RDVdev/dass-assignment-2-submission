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

