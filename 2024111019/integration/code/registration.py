"""Registration module for onboarding crew members."""

from streetrace_manager.models import CrewMember, VALID_ROLES


class RegistrationModule:
    """Registers and stores crew members in the shared system state."""

    def __init__(self, system):
        self.system = system

    def register_member(self, name: str, role: str) -> CrewMember:
        """Register a new member with name and role."""
        clean_name = name.strip()
        clean_role = role.strip().lower()
        if not clean_name:
            raise ValueError("Member name cannot be empty.")
        if clean_name in self.system.members:
            raise ValueError(f"Member '{clean_name}' already exists.")
        if clean_role not in VALID_ROLES:
            raise ValueError(f"Invalid role '{clean_role}'.")

        member = CrewMember(name=clean_name, role=clean_role)
        self.system.members[clean_name] = member
        self.system.rankings.setdefault(clean_name, 0)
        return member

    def is_registered(self, name: str) -> bool:
        """Return True when the given member exists."""
        return name in self.system.members
