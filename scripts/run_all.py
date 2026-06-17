from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    commands = [
        ["scripts/run_problem1_analysis.py"],
        ["scripts/run_problem2_modeling.py"],
        [
            "scripts/run_problem3_explainability.py",
            "--n-repeats",
            "6",
            "--n-jobs",
            "2",
        ],
    ]
    for command in commands:
        print(f"[run_all] running {' '.join(command)}", flush=True)
        subprocess.run([sys.executable, *command], cwd=PROJECT_ROOT, check=True)
    print("[run_all] all workflows completed", flush=True)


if __name__ == "__main__":
    main()
