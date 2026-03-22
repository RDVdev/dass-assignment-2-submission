"""System orchestration class wiring all StreetRace Manager modules."""

from streetrace_manager.crew_management import CrewManagementModule
from streetrace_manager.garage import GarageModule
from streetrace_manager.heat_management import HeatManagementModule
from streetrace_manager.inventory import InventoryModule
from streetrace_manager.mission_planning import MissionPlanningModule
from streetrace_manager.race_management import RaceManagementModule
from streetrace_manager.registration import RegistrationModule
from streetrace_manager.results import ResultsModule


class StreetRaceSystem:
    """Central state container and module integration point."""

    def __init__(self):
        self.members = {}
        self.rankings = {}
        self.races = {}
        self.missions = {}
        self.next_race_id = 1
        self.next_mission_id = 1

        self.heat_management = HeatManagementModule()
        self.registration = RegistrationModule(self)
        self.crew_management = CrewManagementModule(self)
        self.inventory = InventoryModule(self)
        self.race_management = RaceManagementModule(self)
        self.results = ResultsModule(self)
        self.mission_planning = MissionPlanningModule(self)
        self.garage = GarageModule(self)
