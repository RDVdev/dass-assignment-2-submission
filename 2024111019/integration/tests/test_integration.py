"""Integration tests for StreetRace Manager module interactions."""

from pathlib import Path
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from streetrace_manager.core import StreetRaceSystem


class TestStreetRaceIntegration(unittest.TestCase):
    """Validates cross-module behavior and business rules."""

    def setUp(self):
        self.system = StreetRaceSystem()
        self.system.inventory.add_cash(1000)
        self.system.inventory.add_car("CAR-1", "Nissan Skyline")
        self.system.inventory.add_part("repair_kit", 3)

    def test_register_driver_then_enter_race_success(self):
        """Registered driver with driver role should be enterable in race."""
        self.system.registration.register_member("Aki", "driver")
        race = self.system.race_management.create_race("NightSprint", 500)
        self.system.race_management.enter_driver(race.race_id, "Aki", "CAR-1")
        self.assertEqual(len(race.entries), 1)
        self.assertEqual(race.entries[0], ("Aki", "CAR-1"))

    def test_enter_race_without_registered_driver_fails(self):
        """Race entry should reject unregistered member."""
        race = self.system.race_management.create_race("HarborRun", 300)
        with self.assertRaises(ValueError):
            self.system.race_management.enter_driver(race.race_id, "Ghost", "CAR-1")

    def test_only_driver_role_can_enter_race(self):
        """Registered non-driver should be rejected by race module."""
        self.system.registration.register_member("Mio", "mechanic")
        race = self.system.race_management.create_race("TunnelDash", 450)
        with self.assertRaises(ValueError):
            self.system.race_management.enter_driver(race.race_id, "Mio", "CAR-1")

    def test_assign_role_requires_registered_member(self):
        """Crew role assignment must reject members who were not registered first."""
        with self.assertRaises(ValueError):
            self.system.crew_management.assign_role("Ghost", "driver")

    def test_race_results_update_cash_and_rankings(self):
        """Results module should update inventory cash and ranking points."""
        self.system.registration.register_member("Aki", "driver")
        self.system.registration.register_member("Ren", "driver")
        race = self.system.race_management.create_race("CityLoop", 700)
        self.system.race_management.enter_driver(race.race_id, "Aki", "CAR-1")
        self.system.inventory.add_car("CAR-2", "Toyota Supra")
        self.system.race_management.enter_driver(race.race_id, "Ren", "CAR-2")
        self.system.race_management.start_race(race.race_id)

        before_cash = self.system.inventory.cash_balance
        self.system.results.record_race_result(race.race_id, ["Ren", "Aki"])

        self.assertEqual(self.system.inventory.cash_balance, before_cash + 700)
        self.assertEqual(self.system.rankings["Ren"], 10)
        self.assertEqual(self.system.rankings["Aki"], 6)

    def test_results_require_started_race(self):
        """Results should not be recordable before a race has started."""
        self.system.registration.register_member("Aki", "driver")
        race = self.system.race_management.create_race("NeonRun", 250)
        self.system.race_management.enter_driver(race.race_id, "Aki", "CAR-1")

        with self.assertRaises(ValueError):
            self.system.results.record_race_result(race.race_id, ["Aki"])

    def test_damaged_car_mission_requires_mechanic(self):
        """Mission planning should block mission when linked car is damaged and no mechanic exists."""
        self.system.registration.register_member("Aki", "driver")
        self.system.inventory.mark_car_damaged("CAR-1", 70)

        mission = self.system.mission_planning.create_mission(
            name="RescueRun",
            required_roles=["driver"],
            reward=400,
            linked_car_id="CAR-1",
        )

        ready, reason = self.system.mission_planning.can_start_mission(mission.mission_id)
        self.assertFalse(ready)
        self.assertIn("mechanic", reason)

    def test_mission_cannot_start_when_required_role_is_missing(self):
        """Mission planning must reject missions whose required roles are unavailable."""
        self.system.registration.register_member("Aki", "driver")
        mission = self.system.mission_planning.create_mission(
            name="IntelRun",
            required_roles=["driver", "strategist"],
            reward=300,
        )

        ready, reason = self.system.mission_planning.can_start_mission(mission.mission_id)
        self.assertFalse(ready)
        self.assertIn("strategist", reason)

    def test_mission_starts_when_required_roles_available(self):
        """Mission should start and complete when all roles exist."""
        self.system.registration.register_member("Aki", "driver")
        self.system.registration.register_member("Mio", "mechanic")

        mission = self.system.mission_planning.create_mission(
            name="Delivery",
            required_roles=["driver", "mechanic"],
            reward=350,
            linked_car_id="CAR-1",
        )

        self.system.inventory.mark_car_damaged("CAR-1", 30)
        self.system.mission_planning.start_mission(mission.mission_id)
        before_cash = self.system.inventory.cash_balance
        self.system.mission_planning.complete_mission(mission.mission_id)

        self.assertEqual(self.system.missions[mission.mission_id].status, "completed")
        self.assertEqual(self.system.inventory.cash_balance, before_cash + 350)

    def test_garage_repairs_damaged_car_with_mechanic_and_parts(self):
        """Extra Garage module should repair vehicle using crew + parts interaction."""
        self.system.registration.register_member("Mio", "mechanic")
        self.system.inventory.mark_car_damaged("CAR-1", 80)

        self.system.garage.repair_car("CAR-1")

        self.assertLess(self.system.inventory.get_car("CAR-1").damage_level, 80)
        self.assertEqual(self.system.inventory.spare_parts["repair_kit"], 2)

    def test_garage_repair_fails_without_mechanic(self):
        """Garage module should enforce mechanic-role dependency."""
        self.system.inventory.mark_car_damaged("CAR-1", 80)
        with self.assertRaises(ValueError):
            self.system.garage.repair_car("CAR-1")

    def test_high_heat_blocks_race_entry(self):
        """Extra Heat module should block race operations at high risk threshold."""
        self.system.registration.register_member("Aki", "driver")
        race = self.system.race_management.create_race("Dockline", 200)
        self.system.heat_management.increase_heat(100)

        with self.assertRaises(ValueError):
            self.system.race_management.enter_driver(race.race_id, "Aki", "CAR-1")

    def test_full_flow_race_damage_then_repair_then_mission(self):
        """End-to-end integration flow across race, results, garage, and mission modules."""
        self.system.registration.register_member("Aki", "driver")
        self.system.registration.register_member("Mio", "mechanic")

        race = self.system.race_management.create_race("StormRace", 600)
        self.system.race_management.enter_driver(race.race_id, "Aki", "CAR-1")
        self.system.race_management.start_race(race.race_id)
        self.system.results.record_race_result(race.race_id, ["Aki"], damaged_cars=["CAR-1"])

        damaged_level = self.system.inventory.get_car("CAR-1").damage_level
        self.assertGreaterEqual(damaged_level, 60)

        self.system.garage.repair_car("CAR-1")
        self.assertTrue(self.system.garage.is_car_race_ready("CAR-1"))

        mission = self.system.mission_planning.create_mission(
            "Resupply",
            ["driver", "mechanic"],
            reward=200,
            linked_car_id="CAR-1",
        )
        self.system.mission_planning.start_mission(mission.mission_id)
        self.system.mission_planning.complete_mission(mission.mission_id)

        self.assertEqual(self.system.missions[mission.mission_id].status, "completed")


if __name__ == "__main__":
    unittest.main()
