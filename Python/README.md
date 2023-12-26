# Python Scripts for AeTrade

## Overview
This directory contains Python scripts developed for various automation and data management tasks within the AeTrade Group. These scripts are essential tools that aid in streamlining processes, managing data, and enhancing operational efficiency.

## Scripts in This Directory

### DHIS2 Organizational Unit Creation Script

- **Filename**: `create_org_units.py`
- **Description**: 
  - This script is designed to automate the creation of organizational units in DHIS2, specifically tailored for operations in Rwanda. It reads from a CSV file and creates a hierarchy of organizational units in DHIS2 using provided credentials. The script uses the `requests` library for API interactions and handles CSV processing to build the necessary structure within DHIS2.
- **Usage**:
  - Update the `api_url`, `username`, and `password` with your DHIS2 instance details.
  - Provide the path to your CSV file in the `process_csv_and_create_hierarchy` function call.
  - Run the script to create the organizational units in DHIS2.

### [Other Script Titles]

- **Filename**: `other_script.py`
- **Description**: 
  - [Brief description of the other scripts and their purposes.]
- **Usage**:
  - [Instructions or notes on how to use these additional scripts.]

## Getting Started

To use the scripts in this directory:

1. Ensure Python is installed on your system.
2. Install any required dependencies (if applicable).
3. Run the script with necessary parameters or inputs.

## Contributing

Contributions to improve or add new scripts are always welcome. Please follow the standard practices for code quality, documentation, and pull request processes.

