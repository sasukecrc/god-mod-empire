"""
Finance and Tracking Division - Tracks all earnings and reports to boss
Employees: 3 accountants
Goal: Help boss pay father's loan and buy mother a scooter
"""
import json
import logging
import os
from datetime import datetime

from config import *

logger = logging.getLogger("FinanceDiv")


def load_earnings():
    try:
        if os.path.exists(TRACKING_FILE):
            with open(TRACKING_FILE, "r") as f:
                return json.load(f)
    except:
        pass
    return {"total_earned": 0, "applications_sent": 0, "websites_created": 0, "linkedin_posts": 0, "goals": {"father_loan": {"target": FATHER_LOAN_AMOUNT, "progress": 0, "description": "Help pay father's loan"}, "mother_scooter": {"target": MOTHER_SCOOTER_COST, "progress": 0, "description": "Buy mother a scooter"}, "living_expenses": {"target": MONTHLY_LIVING_COST, "progress": 0, "description": "Monthly living costs"}}, "transactions": [], "last_updated": datetime.utcnow().isoformat()}


def save_earnings(data):
    os.makedirs("data", exist_ok=True)
    data["last_updated"] = datetime.utcnow().isoformat()
    with open(TRACKING_FILE, "w") as f:
        json.dump(data, f, indent=2)


def run_finance_cycle():
    logger.info("  Finance Division: Crunching numbers...")
    data = load_earnings()
    apps_sent = data.get("applications_sent", 0)
    estimated_projects = apps_sent * 0.05
    estimated_earnings = estimated_projects * 500
    results = {"earnings": data.get("total_earned", 0), "estimated_earnings": estimated_earnings, "applications_sent": apps_sent, "goals_report": {}}
    for goal_name, goal_data in data.get("goals", {}).items():
        progress = goal_data["progress"]
        target = goal_data["target"]
        remaining = max(0, target - progress)
        pct = (progress / target * 100) if target > 0 else 0
        results["goals_report"][goal_name] = {"progress": progress, "target": target, "remaining": remaining, "percentage": round(pct, 1)}
        if goal_name in MONEY_GOALS:
            MONEY_GOALS[goal_name]["progress"] = goal_data["progress"]
    total_progress = sum(g["progress"] for g in data.get("goals", {}).values())
    total_target = sum(g["target"] for g in data.get("goals", {}).values())
    overall_pct = (total_progress / total_target * 100) if total_target > 0 else 0
    logger.info(f"     Current: ${data.get('total_earned', 0):.2f} | Progress: {overall_pct:.1f}%")
    return results


def print_boss_report():
    data = load_earnings()
    print("\n" + "="*60)
    print("           BOSS EARNINGS REPORT")
    print("="*60)
    print(f"  Total Earned: ${data.get('total_earned', 0):.2f}")
    print(f"  Applications: {data.get('applications_sent', 0)}")
    print(f"  Websites: {data.get('websites_created', 0)}")
    print(f"  LinkedIn Posts: {data.get('linkedin_posts', 0)}")
    print("")
    print("  BOSS GOALS:")
    for name, goal in data.get("goals", {}).items():
        pct = (goal["progress"] / goal["target"] * 100) if goal["target"] > 0 else 0
        bar = "#" * int(pct / 5) + "." * (20 - int(pct / 5))
        print(f"     {goal['description']}: ${goal['progress']:.0f}/${goal['target']}")
        print(f"     [{bar}] {pct:.1f}%")
    print("")
    print("  GOD MOD: Boss, I'm working 24/7 for you!")
    print("")
