#!/usr/bin/env python3

import os
import sys
import git
from datetime import datetime, timedelta
from dateutil.parser import parse
from pathlib import Path

def is_monday(date):
    """Check if the given date is a Monday."""
    return date.weekday() == 0

def get_week_dates(monday_date):
    """Get all dates from Monday to Friday for the given week."""
    dates = []
    for i in range(5):  # Monday to Friday
        dates.append(monday_date + timedelta(days=i))
    return dates

def is_git_repo(path):
    """Check if the given path is a git repository."""
    try:
        git.Repo(path)
        return True
    except git.InvalidGitRepositoryError:
        return False

def get_commits_for_date(repo, date):
    """Get all commits for a specific date in the repository."""
    commits = []
    start_date = datetime.combine(date, datetime.min.time())
    end_date = datetime.combine(date, datetime.max.time())
    
    for commit in repo.iter_commits():
        commit_date = datetime.fromtimestamp(commit.committed_date)
        if start_date <= commit_date <= end_date:
            commits.append(commit)
    
    return commits

def process_workspace(workspace_path, monday_date):
    """Process the workspace and generate status report."""
    workspace = Path(workspace_path)
    if not workspace.exists():
        print(f"Error: Workspace path {workspace_path} does not exist.")
        return

    week_dates = get_week_dates(monday_date)
    status_report = {}

    # Initialize status report with all dates
    for date in week_dates:
        status_report[date] = "continuing previous day's work"

    print("\nScanning repositories in ~/Workspaces:")
    print("-" * 50)
    
    # Process each item in the workspace
    for item in workspace.iterdir():
        if item.is_dir():
            if is_git_repo(item):
                print(f"✓ Found git repository: {item.name}")
                repo = git.Repo(item)
                for date in week_dates:
                    commits = get_commits_for_date(repo, date)
                    if commits:
                        # Get the first commit message for the day
                        status_report[date] = commits[0].message.strip()
            else:
                print(f"✗ Not a git repository: {item.name}")
    
    print("-" * 50)
    return status_report

def generate_report(status_report, output_file):
    """Generate the status report file."""
    with open(output_file, 'w') as f:
        for date, message in status_report.items():
            f.write(f"{date.strftime('%m/%d/%Y')} - {message}\n")

def main():
    if len(sys.argv) != 2:
        print("Usage: wsr <monday_date>")
        print("Example: wsr 06/02/2026")
        sys.exit(1)

    try:
        monday_date = parse(sys.argv[1]).date()
    except ValueError:
        print("Error: Invalid date format. Please use MM/DD/YYYY format.")
        sys.exit(1)

    if not is_monday(monday_date):
        print("Error: Please provide a Monday date.")
        sys.exit(1)

    workspace_path = os.path.expanduser("~/Workspaces")
    status_report = process_workspace(workspace_path, monday_date)
    
    # Generate output filename based on the week
    output_file = f"status_report_{monday_date.strftime('%Y%m%d')}.txt"
    generate_report(status_report, output_file)
    print(f"\nStatus report generated: {output_file}")

if __name__ == "__main__":
    main() 