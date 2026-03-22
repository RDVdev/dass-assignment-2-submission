"""Extra module: Garage operations for repairs and vehicle readiness."""


class GarageModule:
    """Repairs damaged cars using mechanics and spare parts."""

    def __init__(self, system):
        self.system = system

    def repair_car(self, car_id: str, use_part: str = "repair_kit") -> None:
        """Repair car damage if mechanic and required parts are available."""
        if not self.system.crew_management.has_role_available("mechanic"):
            raise ValueError("Cannot repair car without an available mechanic.")

        if not self.system.inventory.consume_part(use_part, 1):
            raise ValueError(f"Repair requires one '{use_part}' part in inventory.")

        car = self.system.inventory.get_car(car_id)
        car.damage_level = max(0, car.damage_level - 60)

    def is_car_race_ready(self, car_id: str) -> bool:
        """Return True when the selected car is race ready."""
        return self.system.inventory.get_car(car_id).race_ready
