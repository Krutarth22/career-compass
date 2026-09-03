"""Pytest configuration for career-compass tests.

Inserts the career-compass scripts directory into sys.path so tests can import
modules directly (e.g., import profile_io, import resolution, etc).
"""

import sys
from pathlib import Path

# Compute repo root from this file's location
repo_root = Path(__file__).parent.parent

# Add scripts directory to sys.path (college-plan's curriculum_planner.py
# lives here too, folded into career-compass as its college-plan mode).
scripts_dir = repo_root / ".claude" / "skills" / "career-compass" / "scripts"
sys.path.insert(0, str(scripts_dir))
