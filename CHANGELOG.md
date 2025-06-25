# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0] - 2024-03-19

### Changed
- Generate one `.docx` status report per week: Now, for a given Monday, the tool creates a separate `.docx` file for each week (Monday–Friday) using the provided template.
- Table formatting improvements: All generated tables now have visible borders and added cell padding for improved readability and a more professional look.
- Helper functions: Added utility functions to set table cell borders and padding using `python-docx`.
- Retain `.txt` report: The tool still generates a single `.txt` report for all weeks as before.
- Improved user experience: The generated reports are now easier to read and ready for direct use in status updates.

## [0.1.0] - 2024-03-19

### Added
- Initial release of Weekly Status Report Generator
- Basic functionality to generate weekly status reports from git commits
- Command-line interface with `wsr` command
- Support for scanning git repositories in ~/Workspaces
- Daily commit message tracking from Monday to Friday
- Unit test suite with pytest
- Test coverage reporting
- Comprehensive test cases for date handling and validation
- User-specific commit filtering
  - Automatically detects git user from repository config
  - Filters commits by current user's email and name
  - Shows user information during repository scanning

### Changed
- Enhanced report generation to support multiple weeks
- Added weekly section headers in the report
- Improved report formatting with separators
- Added "END of Report" marker
- Added test dependencies to setup.py
- Improved commit filtering to focus on user's own commits

### Features
- Generate reports for any past Monday date
- Automatically includes all weeks from the given date until today
- Shows "continuing previous day's work" for days without commits
- Displays repository scanning progress
- Creates formatted text reports with weekly sections
- Comprehensive test coverage for core functionality
- Smart commit filtering by current git user 