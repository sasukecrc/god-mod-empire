"""
Client Acquisition Division - Finds high-paying jobs and applies to them
Employees: 25 (10 searchers + 15 appliers)
Target: $50-150/hr freelance jobs
"""
import json
import logging
import time
from datetime import datetime
from typing import Dict, List

from config import *
from core.composio_client import search_jobs, send_application_email

logger = logging.getLogger("AcquisitionDiv")

APPLICATION_TEMPLATES = {
    "webdev": """Hi there,

I am a professional web developer with extensive experience building modern, high-performance websites. I saw your project and I'm confident I can deliver exactly what you need.

What I offer:
Modern, responsive design (works on all devices)
Fast load times (optimized for speed)
SEO-friendly structure
Clean, maintainable code
Free 30-day support after delivery

My tech stack: HTML5, CSS3, JavaScript, React, Node.js, WordPress, Webflow, Shopify

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

I'm available to start immediately. Let me know if you'd like to discuss your project!

Best regards,
CR7 SASUKE CR7""",
    "wordpress": """Hi,

I am a WordPress expert with years of experience building custom themes, plugins, WooCommerce stores, and optimized sites.

I can help you with:
Custom WordPress theme development
WooCommerce e-commerce setup
Elementor/divi page building
Performance optimization and caching
Security hardening
SEO optimization

Every site I build is mobile-responsive, fast-loading, and SEO-ready.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

Available now. Let's discuss your project!

Best regards,
CR7 SASUKE CR7""",
    "shopify": """Hi,

I am a Shopify developer experienced in building high-converting e-commerce stores from scratch and optimizing existing ones.

My Shopify services:
Custom theme development
Store setup and configuration
App integration and automation
Product page optimization
Speed optimization
Conversion rate optimization

I'll help you create a store that looks premium and converts visitors into customers.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

Let's build your e-commerce success story!

Best regards,
CR7 SASUKE CR7""",
    "react": """Hi,

I am a front-end developer specialized in React.js and Next.js with experience building modern web applications.

I excel at:
React/Next.js web applications
Responsive UI with modern frameworks
API integration
State management
Performance optimization
Progressive web apps

I write clean, well-documented code and deliver on time.

Portfolio: https://github.com/sasukecrc
Email: sasukecrcr@gmail.com

I'd love to work on your project!

Best regards,
CR7 SASUKE CR7""",
}

APPLIED_CACHE = set()


def classify_job(title):
    t = (title or "").lower()
    if any(kw in t for kw in ["wordpress", "woocommerce", "elementor"]):
        return "wordpress"
    elif any(kw in t for kw in ["shopify", "e-commerce", "ecommerce"]):
        return "shopify"
    elif any(kw in t for kw in ["react", "nextjs", "next.js", "frontend"]):
        return "react"
    else:
        return "webdev"


def search_for_jobs():
    logger.info("  Searching for high-paying jobs...")
    all_jobs = []
    queries = HIGH_PAYING_JOB_QUERIES + PLATFORM_QUERIES
    for query in queries:
        try:
            jobs = search_jobs(query)
            if jobs:
                for job in jobs:
                    job["search_query"] = query
                all_jobs.extend(jobs)
                logger.info(f"     Found {len(jobs)} from: {query[:50]}")
            time.sleep(0.3)
        except Exception as e:
            logger.warning(f"     Search error: {e}")
    logger.info(f"  Total jobs found: {len(all_jobs)}")
    return all_jobs


def apply_to_job(job):
    title = job.get("title", "Web Development Project") or "Web Development Project"
    url = job.get("url", "")
    if url in APPLIED_CACHE:
        return {"status": "skipped", "reason": "already_applied"}
    job_type = classify_job(title)
    template = APPLICATION_TEMPLATES.get(job_type, APPLICATION_TEMPLATES["webdev"])
    subject = f"Professional Web Developer: {title[:70]}"
    logger.info(f"     Applying to: {title[:50]}...")
    try:
        result = send_application_email("sasukecrcr@gmail.com", subject, template)
        if result.get("success"):
            APPLIED_CACHE.add(url)
            logger.info(f"     Sent!")
            return {"job_title": title, "job_url": url, "status": "sent", "template_used": job_type}
        else:
            logger.warning(f"     Failed: {result.get('error')}")
            return {"job_title": title, "status": "failed", "error": result.get("error")}
    except Exception as e:
        logger.error(f"     Error: {e}")
        return {"job_title": title, "status": "error", "error": str(e)}


def run_acquisition_cycle():
    logger.info("  Client Acquisition Division: Starting...")
    results = {"jobs_found": 0, "applications_sent": 0, "applications_failed": 0, "errors": []}
    try:
        jobs = search_for_jobs()
        results["jobs_found"] = len(jobs)
    except Exception as e:
        logger.error(f"  Search phase failed: {e}")
        results["errors"].append(f"Search error: {e}")
        return results
    if not jobs:
        logger.info("  No new jobs found")
        return results
    try:
        jobs_to_apply = jobs[:APPLICATIONS_PER_CYCLE]
        sent, failed = 0, 0
        for job in jobs_to_apply:
            result = apply_to_job(job)
            if result.get("status") == "sent":
                sent += 1
            elif result.get("status") in ("failed", "error"):
                failed += 1
            time.sleep(1.5)
        results["applications_sent"] = sent
        results["applications_failed"] = failed
    except Exception as e:
        logger.error(f"  Apply phase failed: {e}")
        results["errors"].append(f"Apply error: {e}")
    return results
