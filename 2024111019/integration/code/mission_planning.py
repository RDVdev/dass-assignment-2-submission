"""Mission planning module for role-based mission readiness and completion."""

from streetrace_manager.models import Mission


class MissionPlanningModule:
    """Creates missions and verifies role availability before start."""

    def __init__(self, system):
        self.system = system

    def create_mission(self, name: str, required_roles: list[str], reward: int, linked_car_id=None) -> Mission:
        """Create a mission with required crew roles."""
        if not name.strip():
            raise ValueError("Mission name cannot be empty.")
        if not required_roles:
            raise ValueError("Mission must require at least one role.")
        if reward < 0:
            raise ValueError("Mission reward cannot be negative.")
        mission_id = f"MIS-{self.system.next_mission_id}"
        self.system.next_mission_id += 1
        mission = Mission(
            mission_id=mission_id,
            name=name,
            required_roles=[r.lower() for r in required_roles],
            reward=reward,
            linked_car_id=linked_car_id,
        )
        self.system.missions[mission_id] = mission
        return mission

    def can_start_mission(self, mission_id: str) -> tuple[bool, str]:
        """Return mission start readiness and reason."""
        if mission_id not in self.system.missions:
            raise ValueError(f"Mission '{mission_id}' not found.")
        mission = self.system.missions[mission_id]

        for role in mission.required_roles:
            if not self.system.crew_management.has_role_available(role):
                return False, f"Required role '{role}' is unavailable."

        if mission.linked_car_id is not None:
            car = self.system.inventory.get_car(mission.linked_car_id)
            if car.damage_level > 0 and not self.system.crew_management.has_role_available("mechanic"):
                return False, "Damaged car mission requires mechanic availability."

        return True, "Mission ready."

    def start_mission(self, mission_id: str) -> None:
        """Start mission if required roles are available."""
        if mission_id not in self.system.missions:
            raise ValueError(f"Mission '{mission_id}' not found.")
        mission = self.system.missions[mission_id]
        if mission.status != "planned":
            raise ValueError("Mission has already started or finished.")
        ready, reason = self.can_start_mission(mission_id)
        if not ready:
            raise ValueError(reason)
        mission.status = "running"
        self.system.heat_management.increase_heat(5)

    def complete_mission(self, mission_id: str) -> None:
        """Complete mission and award cash."""
        if mission_id not in self.system.missions:
            raise ValueError(f"Mission '{mission_id}' not found.")
        mission = self.system.missions[mission_id]
        if mission.status != "running":
            raise ValueError("Mission must be running before completion.")
        self.system.inventory.add_cash(mission.reward)
        mission.status = "completed"
