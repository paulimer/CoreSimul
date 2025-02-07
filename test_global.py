#!/usr/bin/env python3

import os
import pathlib
import subprocess as sp

import pytest

CONTROL_FILE = "control.txt"

def run_coresimul_master(control_file, output_dir):
    """Runs the coresimul_master.py script with the given control file."""
    control_path = pathlib.Path(control_file)
    control_text = control_path.read_text()
    control_text = "\n".join(
        line for line in control_text.splitlines() if not line.startswith("OUTPUT=")
    )
    control_text = f"OUTPUT={output_dir}\n" + control_text
    control_path.write_text(control_text)
    sp.run(["python", "coresimul_master.py", control_file], check=True)


def test_output_files(file_regression, tmp_path):
    """Tests the main function to fix CoreSimul's global behavior."""
    tmp_output_dir = tmp_path / "output"
    tmp_output_dir.mkdir()

    run_coresimul_master(CONTROL_FILE, tmp_output_dir)

    # delete the output line in the control file
    control_path = pathlib.Path(CONTROL_FILE)
    control_text = control_path.read_text()
    control_text = "\n".join(
        line for line in control_text.splitlines() if not line.startswith("OUTPUT=")
    )
    control_path.write_text(control_text)

    for f in tmp_output_dir.glob("**/*"):
        if f.is_file():
            print(f"Checking {f.name}...")
            file_regression.check(f.read_text(), basename=f.stem, extension=f.suffix)
