"""Race management module for creating races and selecting entrants."""

from streetrace_manager.models import Race


class RaceManagementModule:
    """Handles race lifecycle before results are recorded."""

    def __init__(self, system):
        self.system = system

    def create_race(self, name: str, prize_money: int) -> Race:
        """Create and store a race event."""
        if not name.strip():
            raise ValueError("Race name cannot be empty.")
        if prize_money < 0:
            raise ValueError("Prize money cannot be negative.")
        race_id = f"RACE-{self.system.next_race_id}"
        self.system.next_race_id += 1
        race = Race(race_id=race_id, name=name, prize_money=prize_money)
        self.system.races[race_id] = race
        return race

    def enter_driver(self, race_id: str, driver_name: str, car_id: str) -> None:
        """Enter a registered driver and a race-ready car into a race."""
        if race_id not in self.system.races:
            raise ValueError(f"Race '{race_id}' not found.")
        race = self.system.races[race_id]
        if race.status != "created":
            raise ValueError("Cannot modify entries after race starts.")
        if not self.system.registration.is_registered(driver_name):
            raise ValueError("Driver must be registered before entering a race.")
        driver = self.system.members[driver_name]
        if driver.role != "driver":
            raise ValueError("Only crew members with role 'driver' may enter races.")

        if not self.system.garage.is_car_race_ready(car_id):
            raise ValueError("Car is too damaged for race entry.")

        if self.system.heat_management.block_racing:
            raise ValueError("Race blocked due to high police heat.")

        if any(entry_driver == driver_name for entry_driver, _entry_car in race.entries):
            raise ValueError("Driver is already entered in this race.")
        if any(entry_car == car_id for _entry_driver, entry_car in race.entries):
            raise ValueError("Car is already assigned to this race.")

        race.entries.append((driver_name, car_id))

    def start_race(self, race_id: str) -> None:
        """Start race if there is at least one valid entry."""
        if race_id not in self.system.races:
            raise ValueError(f"Race '{race_id}' not found.")
        race = self.system.races[race_id]
        if race.status != "created":
            raise ValueError("Race has already started or finished.")
        if not race.entries:
            raise ValueError("Cannot start race without at least one entry.")
        race.status = "running"
        self.system.heat_management.increase_heat(10)
