import unittest
from unittest.mock import patch
import tkinter as tk
from n import NmapGUI  # Replace with the actual module name

class TestNmapGUI(unittest.TestCase):

    def setUp(self):
        # Create an instance of NmapGUI
        self.app = NmapGUI()
        # Create a window to avoid errors related to missing Tkinter mainloop
        self.app.update()

    def test_empty_input(self):
        # Simulate empty target and port input
        self.app.target_entry.delete(0, tk.END)
        self.app.ports_entry.delete(0, tk.END)
        with patch('nmap.PortScanner') as mock_scanner:
            mock_scanner.return_value = None
            self.app.scan()
            output = self.app.output_text.get('1.0', tk.END)
            self.assertIn("Please enter both target and port range.", output)

    def tearDown(self):
        # Clean up after each test
        self.app.destroy()

if __name__ == "__main__":
    unittest.main()