# DASS Assignment 2 - Testing Submission

This repository contains comprehensive testing implementations across three testing paradigms: **Black-Box Testing**, **Integration Testing**, and **White-Box Testing**.

**GitHub Repository**: [https://github.com/RDVdev/dass-assignment-2-submission](https://github.com/RDVdev/dass-assignment-2-submission)

---

## Project Structure

```
2024111019/
├── blackbox/          # Black-box testing for QuickCart API
├── integration/       # Integration testing for StreetRace Manager
├── whitebox/          # White-box testing for game components
└── README.md          # This file
```

---

## 1. Black-Box Testing (QuickCart API)

### Overview
This section contains black-box tests for the **QuickCart REST API** based on the published API contract. Tests are designed without knowledge of internal implementation details.

### Location
- Test file: `blackbox/tests/test_quickcart.py`
- API Specification: `QuickCart System.md` (referenced from main assignment)

### Prerequisites
- **Python 3.8+**
- **pytest** - Test framework
- **requests** - HTTP client library
- **QuickCart API server** running on `http://127.0.0.1:8080/api/v1`

### Installation
```bash
pip install pytest requests
```

### Running the Tests

**Run all black-box tests:**
```bash
cd blackbox
pytest tests/test_quickcart.py -v
```

**Run with custom configuration (environment variables):**
```bash
QUICKCART_BASE_URL=http://localhost:8080/api/v1 \
QUICKCART_ROLL=2024111019 \
pytest tests/test_quickcart.py -v
```

**Run specific test cases:**
```bash
pytest tests/test_quickcart.py::test_function_name -v
```

**Generate detailed test report:**
```bash
pytest tests/test_quickcart.py -v --tb=long
```

### Test Coverage
- Valid API requests and responses
- Invalid inputs and error handling
- Missing fields and headers validation
- Boundary value testing
- HTTP status code verification
- JSON response structure validation

### Notes
- Ensure the QuickCart API server is running before executing tests
- Default base URL: `http://127.0.0.1:8080/api/v1`
- Default roll number header: `2024111019`
- See `blackbox/Report.md` for detailed test results and analysis

---

## 2. Integration Testing (StreetRace Manager)

### Overview
This section contains integration tests for the **StreetRace Manager System**, validating cross-module interactions and business rules.

### Location
- Test file: `integration/tests/test_integration.py`
- Main entry point: `integration/main.py`
- Source code: `integration/code/` containing modules like:
  - `core.py` - Main system orchestration
  - `registration.py` - Crew member registration
  - `crew_management.py` - Role assignment
  - `race_management.py` - Race operations
  - `inventory.py` - Asset management
  - `results.py` - Race outcome recording

### Prerequisites
- **Python 3.8+**
- **unittest** - Built-in testing framework
- **pytest** (optional, for running with pytest)

### Installation
```bash
# No additional packages needed (uses built-in unittest)
# Or if using pytest runner:
pip install pytest
```

### Running the Tests

**Run all integration tests using unittest:**
```bash
cd integration
python -m unittest discover tests/ -v
```

**Or run all tests using pytest:**
```bash
cd integration
pytest tests/ -v
```

**Run a specific test class:**
```bash
cd integration
python -m unittest tests.test_integration.TestStreetRaceIntegration -v
```

**Run a specific test method:**
```bash
cd integration
python -m unittest tests.test_integration.TestStreetRaceIntegration.test_register_driver_then_enter_race_success -v
```

**Run the CLI application:**
```bash
cd integration
python main.py
```

### Test Coverage
- Driver registration and role assignment
- Race creation and entry validation
- Crew member qualification checks
- Inventory and cash management
- Race results and ranking updates
- Error handling and boundary conditions

### Notes
- Tests verify module isolation and proper interaction
- See `integration/report(after testing).md` for detailed results

---

## 3. White-Box Testing (Game Components)

### Overview
This section contains white-box tests for game components, with detailed knowledge of internal implementation. Tests cover individual modules and the main game flow.

### Location
- Test files in `whitebox/tests/`:
  - `test_main_flow_whitebox.py` - Entry point and input parsing
  - `test_bank_whitebox.py` - Banking system
  - `test_dice_cards_whitebox.py` - Dice and card mechanics
  - `test_game_whitebox.py` - Game state management
  - `test_game_branches_whitebox.py` - Game flow branches
  - `test_player_whitebox.py` - Player mechanics
  - `test_property_board_whitebox.py` - Board and property management
- Source code: `whitebox/moneypoly/` (game implementation)

### Prerequisites
- **Python 3.8+**
- **unittest** - Built-in testing framework
- **unittest.mock** - Mocking support (built-in)
- **pytest** (optional, for running with pytest)

### Installation
```bash
# No additional packages needed (uses built-in unittest and mock)
# Or if using pytest runner:
pip install pytest
```

### Running the Tests

**Run all white-box tests using unittest:**
```bash
cd whitebox
python -m unittest discover tests/ -v
```

**Or run all tests using pytest:**
```bash
cd whitebox
pytest tests/ -v
```

**Run tests for a specific component:**
```bash
cd whitebox
python -m unittest tests.test_player_whitebox -v
python -m unittest tests.test_property_board_whitebox -v
python -m unittest tests.test_game_whitebox -v
```

**Run a single test:**
```bash
cd whitebox
python -m unittest tests.test_main_flow_whitebox.TestMainFlowWhiteBox.test_name_parsing_trims_and_filters -v
```

**Run with coverage analysis (if coverage is installed):**
```bash
pip install coverage
cd whitebox
coverage run -m unittest discover tests/
coverage report
```

### Test Coverage
- Main game flow and input parsing
- Banking operations
- Dice rolling and card mechanics
- Player state and movements
- Property acquisition and management
- Board functionality
- Game state transitions
- Exception handling and edge cases

### Notes
- Uses mocking to isolate components
- Tests cover both normal flows and error branches
- See `whitebox/report(whitebox).md` for detailed test results

---

## Running All Tests

To run all tests across all three sections from the root directory:

```bash
# Black-box tests (requires QuickCart API running)
pytest blackbox/tests/ -v

# Integration tests
python -m unittest discover integration/tests/ -v

# White-box tests
python -m unittest discover whitebox/tests/ -v
```

Or using a single pytest command for integration and white-box:
```bash
pytest integration/tests/ whitebox/tests/ -v
```

---

## Dependencies Summary

| Section | Primary Framework | Dependencies | Status |
|---------|------------------|--------------|--------|
| Black-Box | pytest | pytest, requests | Requires external API |
| Integration | unittest | (built-in) | Self-contained |
| White-Box | unittest | (built-in) | Self-contained |

---

## Reports

Each section includes detailed testing reports:
- **Black-Box**: `blackbox/Report.md`
- **Integration**: `integration/report(after testing).md`
- **White-Box**: `whitebox/report(whitebox).md`
and also a report.pdf

---

## Contact & Submission

- **Roll Number**: 2024111019
- **Repository**: https://github.com/RDVdev/dass-assignment-2-submission.git
- **Assignment**: DASS Assignment 2 - Software Testing

