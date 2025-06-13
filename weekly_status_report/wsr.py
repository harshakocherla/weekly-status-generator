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

def get_weeks_until_today(start_monday):
    """Get all Monday dates from start_monday until today's week."""
    weeks = []
    current_monday = start_monday
    today = datetime.now().date()
    
    while current_monday <= today:
        weeks.append(current_monday)
        current_monday += timedelta(days=7)
    
    return weeks

def is_git_repo(path):
    """Check if the given path is a git repository."""
    try:
        git.Repo(path)
        return True
    except git.InvalidGitRepositoryError:
        return False

def get_current_git_user(repo):
    """Get the current git user's email and name."""
    try:
        email = repo.config_reader().get_value("user", "email", "")
        name = repo.config_reader().get_value("user", "name", "")
        return email, name
    except Exception:
        return None, None

def get_commits_for_date(repo, date, user_email=None, user_name=None):
    """Get all commits for a specific date in the repository."""
    commits = []
    start_date = datetime.combine(date, datetime.min.time())
    end_date = datetime.combine(date, datetime.max.time())
    
    for commit in repo.iter_commits():
        commit_date = datetime.fromtimestamp(commit.committed_date)
        if start_date <= commit_date <= end_date:
            # Filter by user if specified
            if user_email and user_name:
                if (commit.author.email == user_email or 
                    commit.author.name == user_name):
                    commits.append(commit)
            else:
                commits.append(commit)
    
    return commits

def process_workspace(workspace_path, monday_date):
    """Process the workspace and generate status report."""
    workspace = Path(workspace_path)
    if not workspace.exists():
        print(f"Error: Workspace path {workspace_path} does not exist.")
        return

    weeks = get_weeks_until_today(monday_date)
    all_reports = {}

    print("\nScanning repositories in ~/Workspaces:")
    print("-" * 50)
    
    # Process each item in the workspace
    for item in workspace.iterdir():
        if item.is_dir():
            if is_git_repo(item):
                print(f"✓ Found git repository: {item.name}")
                repo = git.Repo(item)
                user_email, user_name = get_current_git_user(repo)
                if user_email or user_name:
                    print(f"  👤 Filtering commits for: {user_name or user_email}")
                
                for week_monday in weeks:
                    week_dates = get_week_dates(week_monday)
                    if week_monday not in all_reports:
                        all_reports[week_monday] = {}
                        for date in week_dates:
                            all_reports[week_monday][date] = "continuing previous day's work"
                    
                    for date in week_dates:
                        commits = get_commits_for_date(repo, date, user_email, user_name)
                        if commits:
                            all_reports[week_monday][date] = commits[0].message.strip()
            else:
                print(f"✗ Not a git repository: {item.name}")
    
    print("-" * 50)
    return all_reports

def generate_report(all_reports, output_file):
    """Generate the status report file."""
    with open(output_file, 'w') as f:
        for week_monday, week_report in sorted(all_reports.items()):
            f.write(f"\nReport for week starting at {week_monday.strftime('%m/%d/%Y')}\n")
            f.write("-" * 50 + "\n")
            for date, message in sorted(week_report.items()):
                f.write(f"{date.strftime('%m/%d/%Y')} - {message}\n")
            f.write("-" * 50 + "\n")
        f.write("\nEND of Report\n")

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
    all_reports = process_workspace(workspace_path, monday_date)
    
    # Generate output filename based on the start week
    output_file = f"status_report_{monday_date.strftime('%Y%m%d')}.txt"
    generate_report(all_reports, output_file)
    print(f"\nStatus report generated: {output_file}")

if __name__ == "__main__":
    main() 