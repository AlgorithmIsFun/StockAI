import unittest
from unittest.mock import MagicMock, patch
from ..DatabaseHandlers.DatabaseHandler import DatabaseHandler
from io import StringIO
import subprocess

class TestCouchDBHandler(unittest.TestCase):

    @patch("sys.stdout", new_callable=StringIO)
    def test_createUser(self, mock_stdout):
        handler = DatabaseHandler()
        handler.createUser("CouchDB", "alex", "password", [], "testdb")
        output = mock_stdout.getvalue().strip().split("\n")
        last_message = output[-1] if output else ""
        self.assertIn(f"User 'alex' created successfully", last_message)

if __name__ == '__main__':
    unittest.main()
