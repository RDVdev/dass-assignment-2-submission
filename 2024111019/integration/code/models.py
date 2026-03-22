"""Data models used by StreetRace Manager modules."""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


VALID_ROLES = {"driver", "mechanic", "strategist", "scout", "hacker"}


@dataclass
class CrewMember:
    """Represents a crew member with one primary role and skill levels."""

    name: str
    role: str
    skills: Dict[str, int] = field(default_factory=dict)


@dataclass
class Car:
    """Represents a race car tracked by inventory."""

    car_id: str
    model: str
    damage_level: int = 0

    @property
    def race_ready(self) -> bool:
        """Return True when the car damage is low enough to race."""
        return self.damage_level < 50


@dataclass
class Race:
    """Represents a race and its entries/results."""

    race_id: str
    name: str
    prize_money: int
    entries: List[Tuple[str, str]] = field(default_factory=list)
    status: str = "created"


@dataclass
class Mission:
    """Represents an underground mission with role requirements."""

    mission_id: str
    name: str
    required_roles: List[str]
    reward: int
    status: str = "planned"
    linked_car_id: str | None = None
