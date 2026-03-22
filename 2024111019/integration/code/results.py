"""Results module for race outcomes, rankings, and prize updates."""


class ResultsModule:
    """Records race outcomes and applies standings/cash effects."""

    POINTS = [10, 6, 3, 1]

    def __init__(self, system):
        self.system = system
        self.race_history = []

    def record_race_result(self, race_id: str, placements: list[str], damaged_cars=None) -> None:
        """Record race placements and update ranking + cash balance."""
        if race_id not in self.system.races:
            raise ValueError(f"Race '{race_id}' not found.")
        race = self.system.races[race_id]
        if race.status != "running":
            raise ValueError("Race must be running before results can be recorded.")
        if not placements:
            raise ValueError("Placements cannot be empty.")

        entered_drivers = {driver for driver, _car in race.entries}
        if len(placements) != len(set(placements)):
            raise ValueError("Placements cannot contain duplicate drivers.")
        if set(placements) != entered_drivers:
            raise ValueError("Placements must contain every entered driver exactly once.")

        for idx, driver in enumerate(placements):
            points = self.POINTS[idx] if idx < len(self.POINTS) else 0
            self.system.rankings[driver] = self.system.rankings.get(driver, 0) + points

        winner = placements[0]
        self.system.inventory.add_cash(race.prize_money)

        if damaged_cars:
            for car_id in damaged_cars:
                self.system.inventory.mark_car_damaged(car_id, 60)

        race.status = "completed"
        self.race_history.append(
            {
                "race_id": race_id,
                "winner": winner,
                "placements": list(placements),
                "prize": race.prize_money,
            }
        )

    def get_rankings(self) -> list[tuple[str, int]]:
        """Return rankings in descending score order."""
        return sorted(self.system.rankings.items(), key=lambda pair: pair[1], reverse=True)
