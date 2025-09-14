# Copilot Instructions for ccna Project

## Project Overview
This repository is a network automation toolkit for CCNA exam preparation. It is organized into modular components for device management, scanning, and configuration, with a focus on extensibility and practical workflows.

## Architecture & Key Components
- **Netmiko/main_netmiko.py**: Entry point for automation scripts. Orchestrates device interactions and module usage.
- **Netmiko/core/**: Core logic for scanning (`scanner.py`), startup routines (`startup.py`), and device synchronization (`sync.py`).
- **Netmiko/modules/**: Contains specialized modules:
  - `bastion_router/`: Bastion host connection and scanning logic.
  - `database_manager/`: Database utilities for device inventory.
  - `scanner/`: Network scanning utilities.
  - `switches/`: Switch management and configuration.
  - `telnet_manager/`: Telnet session management.
- **Netmiko/database/**: SQLite database for device inventory (`net_devices.db`).
- **Netmiko/scripts/**: Utility scripts for DB management and project checks.

## Developer Workflows
- **Run main automation**: `python Netmiko/main_netmiko.py`
- **Database reset**: Use `scripts/reset_db.py` or `scripts/reset_db_full.py` for DB cleanup.
- **Update DB schema**: Use `scripts/update_lldp_model_column.py` for schema changes.
- **Check project health**: Run `scripts/check_project.py`.

## Patterns & Conventions
- **Modular imports**: Modules are imported using relative paths within `Netmiko`.
- **Database access**: Use `database_manager/db_utils.py` for all DB operations.
- **Device scanning**: Extend `core/scanner.py` and `modules/scanner/network_scanner.py` for new scan types.
- **Configuration files**: Device configs are stored in `Bastion_init.cfg` and `Switches_init.cfg`.
- **No test framework detected**: Scripts are validated by direct execution and DB inspection.

## External Dependencies
- **Netmiko**: Used for network device communication (see `requirements.txt`).
- **SQLite**: Local DB for device inventory.

## Integration Points
- **Cross-module communication**: Modules interact via shared DB and orchestrator scripts.
- **Extending functionality**: Add new modules under `Netmiko/modules/` and register in `main_netmiko.py`.

## Example: Adding a New Device Type
1. Create a new module in `Netmiko/modules/`.
2. Implement connection logic and scanning routines.
3. Update `main_netmiko.py` to include the new module.
4. Add DB schema changes to `scripts/update_lldp_model_column.py` if needed.

---
For questions or unclear patterns, review `README.md` or ask for clarification.
