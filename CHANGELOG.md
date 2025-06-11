# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2024-03-19

### Added
- Initial release of Weekly Status Report Generator
- Basic functionality to generate weekly status reports from git commits
- Command-line interface with `wsr` command
- Support for scanning git repositories in ~/Workspaces
- Daily commit message tracking from Monday to Friday

### Changed
- Enhanced report generation to support multiple weeks
- Added weekly section headers in the report
- Improved report formatting with separators
- Added "END of Report" marker

### Features
- Generate reports for any past Monday date
- Automatically includes all weeks from the given date until today
- Shows "continuing previous day's work" for days without commits
- Displays repository scanning progress
- Creates formatted text reports with weekly sections 