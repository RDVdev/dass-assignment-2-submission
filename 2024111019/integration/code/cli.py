"""Simple command-line interface for StreetRace Manager."""

from streetrace_manager.core import StreetRaceSystem


def print_help():
    """Print available CLI commands."""
    print("Commands:")
    print("  register <name> <role>")
    print("  assign-role <name> <role>")
    print("  set-skill <name> <skill> <level>")
    print("  add-car <car_id> <model>")
    print("  add-part <part_name> <quantity>")
    print("  add-tool <tool_name>")
    print("  add-cash <amount>")
    print("  spend-cash <amount>")
    print("  create-race <name> <prize>")
    print("  enter-race <race_id> <driver_name> <car_id>")
    print("  start-race <race_id>")
    print("  record-result <race_id> <winner> [runner_up ...]")
    print("  create-mission <name> <reward> <role1,role2,...>")
    print("  start-mission <mission_id>")
    print("  complete-mission <mission_id>")
    print("  repair-car <car_id>")
    print("  cool-down <amount>")
    print("  rankings")
    print("  status")
    print("  quit")


def run_cli():
    """Run interactive CLI loop."""
    system = StreetRaceSystem()
    print("StreetRace Manager CLI")
    print_help()

    while True:
        raw = input("\n> ").strip()
        if not raw:
            continue
        parts = raw.split()
        cmd = parts[0].lower()

        try:
            if cmd == "quit":
                break
            if cmd == "help":
                print_help()
            elif cmd == "register":
                member = system.registration.register_member(parts[1], parts[2])
                print(f"Registered {member.name} as {member.role}.")
            elif cmd == "assign-role":
                system.crew_management.assign_role(parts[1], parts[2])
                print("Role updated.")
            elif cmd == "set-skill":
                system.crew_management.set_skill(parts[1], parts[2], int(parts[3]))
                print("Skill updated.")
            elif cmd == "add-car":
                system.inventory.add_car(parts[1], " ".join(parts[2:]))
                print("Car added.")
            elif cmd == "add-part":
                system.inventory.add_part(parts[1], int(parts[2]))
                print("Part stock updated.")
            elif cmd == "add-tool":
                system.inventory.add_tool(parts[1])
                print("Tool added.")
            elif cmd == "add-cash":
                system.inventory.add_cash(int(parts[1]))
                print("Cash added.")
            elif cmd == "spend-cash":
                system.inventory.spend_cash(int(parts[1]))
                print("Cash spent.")
            elif cmd == "create-race":
                race = system.race_management.create_race(parts[1], int(parts[2]))
                print(f"Race created: {race.race_id}")
            elif cmd == "enter-race":
                system.race_management.enter_driver(parts[1], parts[2], parts[3])
                print("Race entry accepted.")
            elif cmd == "start-race":
                system.race_management.start_race(parts[1])
                print("Race started.")
            elif cmd == "record-result":
                system.results.record_race_result(parts[1], parts[2:])
                print("Result recorded.")
            elif cmd == "create-mission":
                roles = parts[3].split(",")
                mission = system.mission_planning.create_mission(parts[1], roles, int(parts[2]))
                print(f"Mission created: {mission.mission_id}")
            elif cmd == "start-mission":
                system.mission_planning.start_mission(parts[1])
                print("Mission started.")
            elif cmd == "complete-mission":
                system.mission_planning.complete_mission(parts[1])
                print("Mission completed.")
            elif cmd == "repair-car":
                system.garage.repair_car(parts[1])
                print("Car repaired.")
            elif cmd == "cool-down":
                system.heat_management.cool_down(int(parts[1]))
                print("Heat reduced.")
            elif cmd == "rankings":
                for name, points in system.results.get_rankings():
                    print(f"{name}: {points}")
            elif cmd == "status":
                print(f"Cash: {system.inventory.cash_balance}")
                print(f"Heat: {system.heat_management.heat_level}")
                print(f"Cars: {len(system.inventory.cars)}")
                print(f"Members: {len(system.members)}")
            else:
                print("Unknown command. Type 'help'.")
        except (IndexError, ValueError) as exc:
            print(f"Error: {exc}")


def main():
    """CLI entrypoint."""
    run_cli()


if __name__ == "__main__":
    main()
