import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_DATABASE_PATH = os.path.join(BASE_DIR, "test_database.json")
ERROR_NO_RESULTS_FOUND = "No results found in this time window"
ERROR_INVALID_DATE_FORMAT = "Invalid date format"
