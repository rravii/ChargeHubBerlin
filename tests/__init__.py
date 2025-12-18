"""
Test package bootstrap.

Ensures the project root is on sys.path so that imports like
`from community.domain.value_objects import ...` work in all test files.
"""

import os
import sys
from pathlib import Path

# Path to project root (folder that contains `community` and `tests`)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))