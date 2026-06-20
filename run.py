"""
GOD MOD Multi-Agent Freelance Empire - RUNNER
Launches the entire AI workforce on autopilot

Usage:
    python run.py              # Run continuously
    python run.py --once       # Run single cycle
    python run.py --report     # Show earnings report
    python run.py --scale      # Scale up workforce
"""
import sys
import os
import subprocess

if __name__ == "__main__":
    args = " ".join(sys.argv[1:])
    cmd = f"python GOD_MOD.py {args}"
    print("="*60)
    print("  GOD MOD EMPIRE LAUNCHER")
    print("="*60)
    print(f"  Command: {cmd}")
    print("  Starting all 105+ AI employees...")
    print("="*60)
    print("")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.call(cmd, shell=True)
