"""
GOD MOD Multi-Agent Freelance Empire - Configuration
"""
import os
import json

BOSS_NAME = "Boss"
FATHER_LOAN_AMOUNT = 5000
MOTHER_SCOOTER_COST = 1500
MONTHLY_LIVING_COST = 2000
TOTAL_TARGET = FATHER_LOAN_AMOUNT + MOTHER_SCOOTER_COST + MONTHLY_LIVING_COST

COMPOSIO_API_KEY = os.environ.get("COMPOSIO_API_KEY", "")
if not COMPOSIO_API_KEY:
    try:
        with open("secrets.json") as f:
            COMPOSIO_API_KEY = json.load(f).get("composio_api_key", "")
    except:
        pass

MIN_HOURLY_RATE = 50
TARGET_HOURLY_RATE = 100
MAX_HOURLY_RATE = 150
MIN_PROJECT_VALUE = 500
TARGET_DAILY_EARNINGS = 1000
APPLICATIONS_PER_CYCLE = 25
CYCLES_PER_DAY = 6

EMPLOYEE_POOLS = {
    "job_searchers": 10, "job_appliers": 15,
    "website_designers": 10, "website_developers": 15,
    "website_reviewers": 8, "website_upgraders": 10,
    "linkedin_marketers": 5, "client_communicators": 5,
    "error_healers": 7, "quality_analysts": 5,
    "finance_trackers": 3, "market_researchers": 5,
    "follow_up_agents": 7,
}
TOTAL_EMPLOYEES = sum(EMPLOYEE_POOLS.values())

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 2
ERROR_LOG_FILE = "data/errors.json"
SELF_HEALING_ENABLED = True
AUTO_SCALE_EMPLOYEES = True

WEBSITE_OUTPUT_DIR = "websites"
TRACKING_FILE = "data/earnings_tracker.json"

MONEY_GOALS = {
    "father_loan": {"target": FATHER_LOAN_AMOUNT, "progress": 0, "description": "Help pay father's loan"},
    "mother_scooter": {"target": MOTHER_SCOOTER_COST, "progress": 0, "description": "Buy mother a scooter"},
    "living_expenses": {"target": MONTHLY_LIVING_COST, "progress": 0, "description": "Monthly living costs"},
}

HIGH_PAYING_JOB_QUERIES = [
    "urgent web developer needed build website $2000 $5000 budget freelance 2026",
    "freelance full stack developer react node website build project $3000+ 2026",
    "hire web developer Shopify WooCommerce e-commerce store $2000+ 2026",
    "WordPress developer needed rebuild redesign site performance optimization $1500+",
    "webflow developer freelance project product showcase website $1500+ 2026",
    "senior web developer contract $100-$150 per hour remote 2026",
    "freelance web developer build landing page business website $2000+ 2026",
    "looking for web developer small business website redesign 2026 budget $3000+",
    "react nextjs developer freelance website application $4000+ 2026",
    "frontend developer freelance react nextjs website 2026 budget $2000+",
    "full stack developer freelance hourly $75-$150 remote contract 2026",
    "web developer consultant $100 per hour project basis 2026",
    "ecommerce website developer shopify magento $5000+ project 2026",
    "custom web application developer freelance $10000+ budget 2026",
    "website redesign project $3000+ budget freelance developer 2026",
]

PLATFORM_QUERIES = [
    "site:upwork.com web developer freelance project budget $2000+ 2026",
    "site:fiverr.com web developer gig website build premium 2026",
    "site:freelancer.com web development project $2000+ 2026",
    "site:peopleperhour.com web developer job budget $2000+ 2026",
    "site:toptal.com web developer opportunity 2026",
    "site:linkedin.com/jobs web developer freelance contract $100+ hour 2026",
]

LINKEDIN_POSTS = [
    {"type": "service", "content": "I build high-end websites that grow businesses.\n\nMy services:\nPremium Landing Pages - $499+\nFull E-commerce Stores - $999+\nCustom Web Applications - $2999+\nWebsite Redesign & Optimization - $599+\n\nEvery site is mobile-optimized, SEO-friendly, and built for conversions.\n\nDM me for a free consultation. Let's build something amazing!\n\n#WebDeveloper #Freelance #WebDesign #BusinessGrowth #Premium"},
    {"type": "portfolio", "content": "Just delivered another stunning website for a client!\n\nThe result? Clean UI, blazing fast load times, and a seamless mobile experience.\n\nI have capacity for 3 more premium projects this week.\n\nLet's talk about your vision: sasukecrcr@gmail.com\n\n#WebDevelopment #ClientWork #FreelanceLife #PremiumWebDesign"},
    {"type": "tip", "content": "5 things every business website NEEDS in 2026:\n\n1. Mobile-first responsive design\n2. Under 2-second load time\n3. Clear CTAs above the fold\n4. SSL security & HTTPS\n5. SEO-optimized content structure\n\nI build all of this into every site. Want a site that actually performs?\n\nEmail: sasukecrcr@gmail.com\n\n#WebDevTips #BusinessGrowth #WebsiteDesign #DigitalMarketing"},
    {"type": "offer", "content": "SPECIAL LAUNCH OFFER - 40% OFF for first 5 clients!\n\nProfessional web development:\nLanding Pages - $299 (was $499)\nBusiness Websites - $599 (was $999)\nE-commerce Stores - $999 (was $1699)\nCustom Web Apps - From $1999\n\nEach site includes: mobile optimization, SEO setup, performance tuning.\n\nLimited spots! Email: sasukecrcr@gmail.com\n\n#WebDeveloper #SpecialOffer #Freelance #WebsiteDesign #SmallBusiness"},
    {"type": "value", "content": "Your website is your 24/7 salesperson. Is it working for you?\n\nA professionally built website:\nIncreases conversions by 200%+\nLoads in under 2 seconds\nWorks perfectly on all devices\nRanks higher on Google\n\nI build websites that generate real results for your business.\n\nLet's talk: sasukecrcr@gmail.com\n\n#WebDesign #Business #Marketing #Growth #DigitalTransformation"},
]
