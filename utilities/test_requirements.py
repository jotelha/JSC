#!/usr/bin/env python3
"""Test availability of required packages.

  python test_requirements.py path/to/requirements.txt
"""

import unittest
import sys
from pathlib import Path
import pkg_resources

class TestRequirements(unittest.TestCase):
    """Test availability of required packages."""
    REQUIREMENTS_PATH = Path(__file__).with_name("requirements.txt")

    def test_requirements(self):
        """Test that each required package is available."""
        # Ref: https://stackoverflow.com/a/45474387/
        requirements = pkg_resources.parse_requirements(self.REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement)
            with self.subTest(requirement=requirement):
                pkg_resources.require(requirement)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        TestRequirements.REQUIREMENTS_PATH = Path(sys.argv.pop())
    unittest.main()

