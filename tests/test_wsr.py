import unittest
from datetime import datetime, timedelta
from dateutil.parser import parse
from weekly_status_report.wsr import (
    is_monday,
    get_week_dates,
    get_weeks_until_today,
    is_git_repo,
    get_commits_for_date
)

class TestWSR(unittest.TestCase):
    def test_is_monday(self):
        # Test a Monday
        monday = parse("2024-03-18").date()  # This is a Monday
        self.assertTrue(is_monday(monday))
        
        # Test a non-Monday
        tuesday = parse("2024-03-19").date()  # This is a Tuesday
        self.assertFalse(is_monday(tuesday))

    def test_get_week_dates(self):
        monday = parse("2024-03-18").date()
        week_dates = get_week_dates(monday)
        
        # Should return 5 dates (Monday to Friday)
        self.assertEqual(len(week_dates), 5)
        
        # First date should be Monday
        self.assertEqual(week_dates[0], monday)
        
        # Last date should be Friday
        self.assertEqual(week_dates[-1], monday + timedelta(days=4))
        
        # All dates should be in sequence
        for i in range(1, 5):
            self.assertEqual(week_dates[i], week_dates[i-1] + timedelta(days=1))

    def test_get_weeks_until_today(self):
        # Test with a date 2 weeks ago
        two_weeks_ago = datetime.now().date() - timedelta(days=14)
        # Adjust to previous Monday
        while two_weeks_ago.weekday() != 0:
            two_weeks_ago -= timedelta(days=1)
            
        weeks = get_weeks_until_today(two_weeks_ago)
        
        # Should include the start date
        self.assertIn(two_weeks_ago, weeks)
        
        # Should include current week's Monday
        current_monday = datetime.now().date()
        while current_monday.weekday() != 0:
            current_monday -= timedelta(days=1)
        self.assertIn(current_monday, weeks)
        
        # All dates should be Mondays
        for week in weeks:
            self.assertEqual(week.weekday(), 0)
        
        # Dates should be in sequence
        for i in range(1, len(weeks)):
            self.assertEqual(weeks[i], weeks[i-1] + timedelta(days=7))

    def test_invalid_date_format(self):
        with self.assertRaises(ValueError):
            parse("invalid-date")

if __name__ == '__main__':
    unittest.main() 