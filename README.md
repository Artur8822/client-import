# Client Data Import Tool

A Python automation tool for importing, validating, and separating client data from a CSV file.

## Features

- Email and age validation
- Duplicate email detection
- Error logging to `error_log.txt`
- Export of valid data to:
  - `valid_clients.csv`
  - `valid_clients.json`
  - `clients.sqlite`
- Parametrized tests with `pytest`

---

## Project Structure

client_import/
|--- clients.csv # Input file with client data
|--- process.py # Main logic (validation, logging, output)
|--- test_process.py # PyTest test cases
|--- error_log.txt # Automatically generated log for invalid records
|--- valid_clients.csv # Output file with valid data
|--- valid_clients.json # Output file with valid data
|--- valid_clients.sqlite # Output file with valid data
|--- README.md # This file


---

## How to Run

Make sure you have Python 3.8+ and install dependencies:

```bash
pip install -r requirements.txt

python process.py


To run unit tests with pytest:

```bash
pytest -v


---

### 2. Section

## Requirements

- Python 3.8+
- pytest
- import csv
- import json
- import sqlite3

---

## Author

Artur  
Client Data Import Project, 2025





