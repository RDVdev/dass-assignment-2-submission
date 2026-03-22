## Module Responsibilities

### Registration Module
File: `streetrace_manager/registration.py`
- Registers crew members with `name` and `role`.
- Prevents duplicates.
- Validates role names.

### Crew Management Module
File: `streetrace_manager/crew_management.py`
- Assigns/changes role for registered crew members.
- Stores skill levels per crew member.
- Checks role availability.

### Inventory Module
File: `streetrace_manager/inventory.py`
- Tracks cars, spare parts, tools, and cash balance.
- Tracks car damage.
- Manages part consumption for repairs.

### Race Management Module
File: `streetrace_manager/race_management.py`
- Creates races.
- Enters only valid drivers and race-ready cars.
- Blocks race entry when heat is too high.

### Results Module
File: `streetrace_manager/results.py`
- Records race outcomes.
- Updates ranking points.
- Updates inventory cash with race prize.
- Marks cars as damaged when race damage is reported.

### Mission Planning Module
File: `streetrace_manager/mission_planning.py`
- Creates missions with required roles.
- Validates role availability before start.
- Blocks damaged-car missions when no mechanic is available.
- Awards mission cash on completion.

### Additional Module A: Garage
File: `streetrace_manager/garage.py`
- Repairs damaged cars.
- Requires mechanic role and `repair_kit` stock.

### Additional Module B: Heat Management
File: `streetrace_manager/heat_management.py`
- Tracks heat accumulation.
- Provides race blocking state based on threshold.

## 3. Business Rule Integration

Implemented business rules from specification:
- A member must be registered before role assignment.
- Only members with role `driver` can enter races.
- Mission start validates required roles.
- If linked mission car is damaged, mechanic availability is required.
- Race results update inventory cash balance.
- Mission cannot start if required roles are unavailable.

## Integration Test Case Matrix

| ID | Scenario | Modules Involved | Expected Result | Actual Result | Errors Found / Fix |
|----|----------|------------------|-----------------|---------------|--------------------|
| IT-01 | Register driver then enter race | Registration, Race Management, Inventory | Entry accepted | PASS | None |
| IT-02 | Enter race with unregistered driver | Race Management, Registration | Reject with error | PASS | None |
| IT-03 | Enter race with non-driver role | Registration, Crew Management, Race Management | Reject with error | PASS | None |
| IT-04 | Assign role before registration | Crew Management, Registration | Reject with error | PASS | Prevented invalid cross-module state |
| IT-05 | Complete race updates cash and rankings | Race Management, Results, Inventory | Cash + prize, rankings updated | PASS | None |
| IT-06 | Record result before race start | Race Management, Results | Reject with error | PASS | Fixed by enforcing `running` race state before result recording |
| IT-07 | Damaged-car mission without mechanic | Mission Planning, Inventory, Crew Management | Mission blocked | PASS | None |
| IT-08 | Mission with missing required role | Mission Planning, Crew Management | Mission blocked | PASS | None |
| IT-09 | Mission with all required roles | Mission Planning, Crew Management, Inventory | Mission starts and completes, reward added | PASS | None |
| IT-10 | Repair damaged car with mechanic and parts | Garage, Crew Management, Inventory | Damage reduced, part consumed | PASS | None |
| IT-11 | Attempt repair without mechanic | Garage, Crew Management | Repair blocked | PASS | None |
| IT-12 | High heat blocks race entry | Heat Management, Race Management | Entry blocked | PASS | None |
| IT-13 | End-to-end flow race→damage→repair→mission | Race Management, Results, Garage, Mission Planning, Inventory | All state transitions valid | PASS | None |

## 6. Why These Integration Tests Are Needed (Simple Explanation)

- IT-01 ensures modules can perform the normal happy path across registration and race entry.
- IT-02 checks data dependency: race module must not accept unknown people.
- IT-03 checks business rule enforcement: only drivers can race.
- IT-04 checks the rule that role management depends on prior registration.
- IT-05 checks cross-module data flow correctness: race outcome must affect money and rankings.
- IT-06 checks lifecycle correctness so results cannot be recorded for a race that never started.
- IT-07 checks mission safety logic when required roles are missing because of a damaged linked car.
- IT-08 checks mission blocking when a directly required role is unavailable.
- IT-09 checks successful mission data flow and reward update.
- IT-10 verifies repair dependencies (mechanic + part inventory) and car-state updates.
- IT-11 verifies negative branch behavior for unavailable mechanic.
- IT-12 verifies global risk state (heat) correctly blocks race operations.
- IT-13 verifies a realistic multi-module sequence, not just isolated function calls.


Actual output summary:
- Total tests: 13
- Passed: 13
- Failed: 0

Status:
- All integration tests passed.
- All required module interactions behaved as expected.

## 8. Errors or Logical Issues Detected

No runtime integration failures were observed in the final test run.
