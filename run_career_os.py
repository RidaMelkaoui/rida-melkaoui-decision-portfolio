#!/usr/bin/env python3
"""
Career OS — Decision Engineer Application Controller
Unified entrypoint for Rida Melkaoui's automated job application system.
"""

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Add application-system to sys.path
APP_SYS_DIR = Path(__file__).resolve().parent / "application-system"
sys.path.insert(0, str(APP_SYS_DIR))

from cli_manager import main

if __name__ == "__main__":
    main()
