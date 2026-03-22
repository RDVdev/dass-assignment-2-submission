"""Extra module: Heat tracking for police attention and race risk."""


class HeatManagementModule:
    """Tracks police heat and can block races when threshold is exceeded."""

    def __init__(self):
        self.heat_level = 0
        self.block_threshold = 100

    @property
    def block_racing(self) -> bool:
        """Return True when heat level is too high for race operations."""
        return self.heat_level >= self.block_threshold

    def increase_heat(self, amount: int) -> None:
        """Increase heat by a non-negative amount."""
        if amount < 0:
            raise ValueError("Heat increase must be non-negative.")
        self.heat_level += amount

    def cool_down(self, amount: int) -> None:
        """Decrease heat by a non-negative amount, not below zero."""
        if amount < 0:
            raise ValueError("Cooldown amount must be non-negative.")
        self.heat_level = max(0, self.heat_level - amount)
