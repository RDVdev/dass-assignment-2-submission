"""Crew management module for roles and skill levels."""

from streetrace_manager.models import VALID_ROLES


class CrewManagementModule:
    """Manages role assignment and skills for registered crew members."""

    def __init__(self, system):
        self.system = system

    def assign_role(self, member_name: str, role: str) -> None:
        """Assign a role to a registered member."""
        if not self.system.registration.is_registered(member_name):
            raise ValueError("Member must be registered before role assignment.")
        clean_role = role.strip().lower()
        if clean_role not in VALID_ROLES:
            raise ValueError(f"Invalid role '{clean_role}'.")
        self.system.members[member_name].role = clean_role

    def set_skill(self, member_name: str, skill: str, level: int) -> None:
        """Set a skill level (1-10) for a member."""
        if not self.system.registration.is_registered(member_name):
            raise ValueError("Member is not registered.")
        if not 1 <= level <= 10:
            raise ValueError("Skill level must be between 1 and 10.")
        self.system.members[member_name].skills[skill] = level

    def members_with_role(self, role: str):
        """Return all registered members with the role."""
        clean_role = role.strip().lower()
        return [m for m in self.system.members.values() if m.role == clean_role]

    def has_role_available(self, role: str) -> bool:
        """Return True if at least one member with the role exists."""
        return bool(self.members_with_role(role))
