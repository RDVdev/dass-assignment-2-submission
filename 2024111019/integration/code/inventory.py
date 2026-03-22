"""Inventory module for cars, parts, tools, and cash."""

from streetrace_manager.models import Car


class InventoryModule:
    """Tracks the crew's cars, parts/tools, and cash balance."""

    def __init__(self, system):
        self.system = system
        self.cash_balance = 0
        self.cars = {}
        self.spare_parts = {}
        self.tools = set()

    def add_cash(self, amount: int) -> None:
        """Add cash to inventory."""
        if amount < 0:
            raise ValueError("Use spend_cash for deductions.")
        self.cash_balance += amount

    def spend_cash(self, amount: int) -> None:
        """Spend cash from inventory."""
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        if amount > self.cash_balance:
            raise ValueError("Insufficient cash.")
        self.cash_balance -= amount

    def add_car(self, car_id: str, model: str) -> Car:
        """Add a new car to inventory."""
        if car_id in self.cars:
            raise ValueError(f"Car '{car_id}' already exists.")
        car = Car(car_id=car_id, model=model)
        self.cars[car_id] = car
        return car

    def get_car(self, car_id: str) -> Car:
        """Get a car by id."""
        if car_id not in self.cars:
            raise ValueError(f"Car '{car_id}' not found.")
        return self.cars[car_id]

    def mark_car_damaged(self, car_id: str, damage: int) -> None:
        """Increase damage level for a car up to 100."""
        car = self.get_car(car_id)
        if damage < 0:
            raise ValueError("Damage increment must be non-negative.")
        car.damage_level = min(100, car.damage_level + damage)

    def add_part(self, part_name: str, quantity: int) -> None:
        """Add spare parts stock."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        self.spare_parts[part_name] = self.spare_parts.get(part_name, 0) + quantity

    def consume_part(self, part_name: str, quantity: int) -> bool:
        """Consume parts if enough stock exists."""
        if quantity <= 0:
            return False
        current = self.spare_parts.get(part_name, 0)
        if current < quantity:
            return False
        self.spare_parts[part_name] = current - quantity
        return True

    def add_tool(self, tool_name: str) -> None:
        """Add a tool to inventory."""
        self.tools.add(tool_name)
