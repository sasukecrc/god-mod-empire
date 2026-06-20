"""
GOD MOD MULTI-AGENT FREELANCE EMPIRE v3.0
Supreme AI Workforce Commander - 105+ Employees
100% AUTOPILOT - ZERO MANUAL WORK FOR THE BOSS
"""
import json
import logging
import time
import sys
import os
from datetime import datetime
from typing import Dict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ["PYTHONIOENCODING"] = "utf-8"

from config import *
from core.composio_client import set_api_key

os.makedirs("data", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("data/god_mod.log"), logging.StreamHandler()]
)
logger = logging.getLogger("GOD_MOD")


class SelfHealingDecorator:
    @staticmethod
    def retry(max_attempts=3):
        def decorator(func):
            def wrapper(*args, **kwargs):
                for attempt in range(1, max_attempts + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        logger.warning(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                        if attempt < max_attempts:
                            time.sleep(2 * (2 ** (attempt - 1)))
                logger.error(f"  Failed after {max_attempts} attempts")
                return None
            return wrapper
        return decorator


class Employee:
    def __init__(self, emp_id: int, name: str, role: str, division: str):
        self.id = emp_id
        self.name = name
        self.role = role
        self.division = division
        self.status = "idle"
        self.tasks_completed = 0
        self.errors = 0

    def work(self, task: str, func, *args, **kwargs):
        self.status = "working"
        logger.info(f"    Emp#{self.id} {self.name}: {task}")
        try:
            result = func(*args, **kwargs)
            self.tasks_completed += 1
            self.status = "idle"
            return result
        except Exception as e:
            self.errors += 1
            self.status = "error"
            logger.error(f"    Emp#{self.id} failed: {e}")
            return {"error": str(e)}


class Division:
    def __init__(self, name: str, employee_count: int, role: str):
        self.name = name
        self.employees = [Employee(i, f"{role}-{i}", role, name) for i in range(1, employee_count + 1)]
        self.available = self.employees.copy()
        self.busy = []

    def get_employee(self):
        if self.available:
            emp = self.available.pop(0)
            self.busy.append(emp)
            return emp
        new_id = len(self.employees) + 1
        emp = Employee(new_id, f"{self.name}-{new_id}", self.name, self.name)
        self.employees.append(emp)
        self.busy.append(emp)
        logger.info(f"    Created new Emp#{new_id}")
        return emp

    def release(self, emp):
        if emp in self.busy:
            self.busy.remove(emp)
            self.available.append(emp)


class GODModOrchestrator:
    def __init__(self):
        logger.info("")
        logger.info("="*70)
        logger.info("  GOD MOD MULTI-AGENT FREELANCE EMPIRE v3.0")
        logger.info("  Supreme AI Workforce - 105+ Employees")
        logger.info(f"  Boss Goals: ${TOTAL_TARGET}")
        logger.info("="*70)
        logger.info("")

        set_api_key(COMPOSIO_API_KEY)

        self.divisions = {}
        divs = [
            ("Client Acquisition", 25, "Acquirer"),
            ("Website Creation", 25, "Creator"),
            ("Quality & Review", 18, "Reviewer"),
            ("Marketing & Outreach", 17, "Marketer"),
            ("Self-Healing", 12, "Healer"),
            ("Finance & Tracking", 8, "Accountant"),
        ]
        for name, count, role in divs:
            self.divisions[name] = Division(name, count, role)
            logger.info(f"  {name}: {count} employees")
        logger.info(f"  TOTAL WORKFORCE: {sum(len(d.employees) for d in self.divisions.values())} employees")
        logger.info("")

        self.total_earnings = 0
        self.total_apps = 0
        self.cycle_count = 0
        self.goals = MONEY_GOALS

    def run_full_cycle(self):
        self.cycle_count += 1
        logger.info("")
        logger.info(f"  CYCLE #{self.cycle_count} STARTING")
        logger.info("="*70)

        results = {"jobs_found": 0, "applications_sent": 0, "websites_created": 0,
                    "linkedin_posts": 0, "earnings": 0, "errors": []}

        # Phase 1: Client Acquisition
        logger.info("  PHASE 1: CLIENT ACQUISITION")
        try:
            from divisions.acquisition import run_acquisition_cycle
            div = self.divisions["Client Acquisition"]
            emp = div.get_employee()
            r = emp.work("Acquisition Cycle", run_acquisition_cycle) or {}
            div.release(emp)
            results["jobs_found"] += r.get("jobs_found", 0)
            results["applications_sent"] += r.get("applications_sent", 0)
        except Exception as e:
            logger.error(f"  Phase 1 error: {e}")
            results["errors"].append(str(e))

        # Phase 2: Website Creation
        logger.info("  PHASE 2: WEBSITE CREATION")
        try:
            from divisions.creation import run_creation_cycle
            div = self.divisions["Website Creation"]
            emp = div.get_employee()
            r = emp.work("Creation Cycle", run_creation_cycle) or {}
            div.release(emp)
            results["websites_created"] += r.get("websites_created", 0)
        except Exception as e:
            logger.error(f"  Phase 2 error: {e}")
            results["errors"].append(str(e))

        # Phase 3: Marketing
        logger.info("  PHASE 3: MARKETING & OUTREACH")
        try:
            from divisions.creation import run_marketing_cycle
            div = self.divisions["Marketing & Outreach"]
            emp = div.get_employee()
            r = emp.work("Marketing Cycle", run_marketing_cycle) or {}
            div.release(emp)
            results["linkedin_posts"] += r.get("linkedin_posts", 0)
        except Exception as e:
            logger.error(f"  Phase 3 error: {e}")
            results["errors"].append(str(e))

        # Phase 4: Quality & Self-Healing
        logger.info("  PHASE 4: QUALITY & SELF-HEALING")
        try:
            from divisions.quality import run_quality_cycle
            div = self.divisions["Quality & Review"]
            emp = div.get_employee()
            r = emp.work("Quality Cycle", run_quality_cycle) or {}
            div.release(emp)
        except Exception as e:
            logger.error(f"  Phase 4 error: {e}")

        # Phase 5: Finance
        logger.info("  PHASE 5: FINANCE & TRACKING")
        try:
            from divisions.finance import run_finance_cycle
            div = self.divisions["Finance & Tracking"]
            emp = div.get_employee()
            r = emp.work("Finance Cycle", run_finance_cycle) or {}
            div.release(emp)
            results["earnings"] += r.get("earnings", 0)
            for g_name, g_data in r.get("goals_report", {}).items():
                if g_name in self.goals:
                    self.goals[g_name]["progress"] = g_data.get("progress", 0)
        except Exception as e:
            logger.error(f"  Phase 5 error: {e}")

        self.total_earnings += results["earnings"]
        self.total_apps += results["applications_sent"]

        self._print_report(results)
        return results

    def _print_report(self, results):
        total_progress = sum(g["progress"] for g in self.goals.values())
        total_target = sum(g["target"] for g in self.goals.values())
        pct = (total_progress / total_target * 100) if total_target > 0 else 0

        logger.info("")
        logger.info("="*70)
        logger.info("  BOSS - CYCLE REPORT")
        logger.info("="*70)
        logger.info(f"  Jobs Found: {results['jobs_found']}")
        logger.info(f"  Applications Sent: {results['applications_sent']}")
        logger.info(f"  Websites Created: {results['websites_created']}")
        logger.info(f"  LinkedIn Posts: {results['linkedin_posts']}")
        logger.info("")
        logger.info(f"  TOTAL EARNINGS: ${self.total_earnings:.2f}")
        logger.info("")
        logger.info("  GOALS PROGRESS:")
        for name, goal in self.goals.items():
            gp = (goal["progress"] / goal["target"] * 100) if goal["target"] > 0 else 0
            bar = "#" * int(gp / 5) + "." * (20 - int(gp / 5))
            logger.info(f"    {goal['description']}: ${goal['progress']:.0f}/${goal['target']} [{bar}] {gp:.1f}%")
        logger.info("")
        logger.info(f"  Overall: {pct:.1f}% to ALL GOALS")
        if pct >= 100:
            logger.info("  ALL GOALS REACHED!")
        logger.info(f"  GOD MOD: Boss, relax and enjoy!")
        logger.info("")

    def run_continuously(self, cycles=None):
        logger.info("RUNNING GOD MOD EMPIRE - CONTINUOUS OPERATION")
        c = 0
        try:
            while cycles is None or c < cycles:
                c += 1
                self.run_full_cycle()
                total_progress = sum(g["progress"] for g in self.goals.values())
                total_target = sum(g["target"] for g in self.goals.values())
                if total_progress >= total_target:
                    logger.info("ALL BOSS GOALS ACHIEVED!")
                if cycles is None or c < cycles:
                    logger.info("Waiting 30 min for next cycle...")
                    time.sleep(1800)
        except KeyboardInterrupt:
            logger.info("Paused. Resume anytime boss!")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="GOD MOD Empire")
    parser.add_argument("--once", action="store_true", help="Run one cycle")
    parser.add_argument("--cycles", type=int, default=None, help="Number of cycles")
    parser.add_argument("--report", action="store_true", help="Show earnings report")
    args = parser.parse_args()

    god = GODModOrchestrator()

    if args.report:
        from divisions.finance import print_boss_report
        print_boss_report()
    elif args.once:
        god.run_full_cycle()
    else:
        god.run_continuously(cycles=args.cycles)
