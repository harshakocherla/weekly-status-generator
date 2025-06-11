# Weekly Status Report Generator

A command-line tool that generates weekly status reports from git commits in your workspace.

## Features

- Scans through your ~/Workspaces directory
- Identifies git repositories
- Generates a weekly status report (Monday to Friday)
- Shows commit messages for each day
- Indicates "continuing previous day's work" for days without commits

## Installation

1. Clone this repository
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the package in development mode:
   ```bash
   pip install -e .
   ```

## Usage

Run the `wsr` command with a Monday date as an argument:

```bash
wsr MM/DD/YYYY
```

Example:
```bash
wsr 06/02/2026
```

The script will:
1. Verify that the provided date is a Monday
2. Scan through your ~/Workspaces directory
3. Generate a status report file named `status_report_YYYYMMDD.txt`

## Output Format

The generated report will look like this:
```
06/02/2026 - commit message for Monday
06/03/2026 - commit message for Tuesday
06/04/2026 - continuing previous day's work
06/05/2026 - commit message for Thursday
06/06/2026 - continuing previous day's work
```

## Requirements

- Python 3.6 or higher
- gitpython
- python-dateutil 