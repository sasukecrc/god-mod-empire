"""
Website Creation Division - Designs, builds, reviews and upgrades websites
Employees: 33 (10 designers + 15 developers + 5 marketers + 3 communicators)
Creates premium websites that make clients happy
"""
import json
import logging
import time
import os
from datetime import datetime

from config import *
from core.composio_client import post_linkedin_update

logger = logging.getLogger("CreationDiv")
_website_counter = [0]


def create_website(name, client="Potential Client"):
    _website_counter[0] += 1
    site_id = _website_counter[0]
    safe_name = name.replace(" ", "_").replace("/", "_")[:30]
    filename = f"{safe_name}_{site_id}.html"
    filepath = os.path.join(WEBSITE_OUTPUT_DIR, filename)
    html = _generate_premium_website(name, client)
    try:
        os.makedirs(WEBSITE_OUTPUT_DIR, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        logger.info(f"     Website created: {filename}")
        return {"site_id": site_id, "filename": filename, "filepath": filepath, "client": client, "success": True}
    except Exception as e:
        logger.error(f"     Creation failed: {e}")
        return {"success": False, "error": str(e)}


def _generate_premium_website(name, client):
    year = datetime.utcnow().year
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Premium Web Services</title>
    <meta name="description" content="{name} - Professional web development services.">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Segoe UI', -apple-system, sans-serif; line-height: 1.6; color: #1a1a2e; }}
        .hero {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); color: white; padding: 120px 20px 80px; text-align: center; position: relative; overflow: hidden; }}
        .hero h1 {{ font-size: 3.5em; margin-bottom: 20px; }}
        .hero h1 span {{ color: #e94560; }}
        .hero p {{ font-size: 1.3em; opacity: 0.9; max-width: 600px; margin: 0 auto 30px; }}
        .cta-button {{ display: inline-block; padding: 15px 40px; background: #e94560; color: white; text-decoration: none; border-radius: 50px; font-weight: bold; }}
        .cta-button:hover {{ transform: translateY(-3px); box-shadow: 0 10px 30px rgba(233,69,96,0.4); }}
        .services {{ padding: 80px 20px; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .section-title {{ text-align: center; font-size: 2.5em; margin-bottom: 50px; }}
        .section-title span {{ color: #e94560; }}
        .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 30px; }}
        .service-card {{ background: white; padding: 40px 30px; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.05); text-align: center; }}
        .service-card:hover {{ transform: translateY(-10px); }}
        .features {{ padding: 80px 20px; background: #1a1a2e; color: white; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 40px; text-align: center; }}
        .feature-item h3 {{ font-size: 2.5em; color: #e94560; }}
        .about {{ padding: 80px 20px; background: #f8f9fa; text-align: center; }}
        .contact {{ padding: 80px 20px; text-align: center; }}
        .footer {{ background: #1a1a2e; color: white; text-align: center; padding: 40px; }}
        @media (max-width: 768px) {{ .hero h1 {{ font-size: 2em; }} }}
    </style>
</head>
<body>
    <section class="hero">
        <h1>Welcome to <span>{name}</span></h1>
        <p>We build premium websites that grow your business.</p>
        <a href="#contact" class="cta-button">Get a Free Consultation</a>
    </section>
    <section class="services">
        <div class="container">
            <h2 class="section-title">Our <span>Services</span></h2>
            <div class="services-grid">
                <div class="service-card"><h3>Web Development</h3><p>Custom websites built with latest technologies.</p></div>
                <div class="service-card"><h3>E-Commerce</h3><p>Full-featured online stores.</p></div>
                <div class="service-card"><h3>Responsive Design</h3><p>Perfect on all devices.</p></div>
                <div class="service-card"><h3>Performance</h3><p>Lightning-fast load times.</p></div>
            </div>
        </div>
    </section>
    <section class="features">
        <div class="container">
            <div class="features-grid">
                <div class="feature-item"><h3>50+</h3><p>Projects Delivered</p></div>
                <div class="feature-item"><h3>100%</h3><p>Satisfaction</p></div>
                <div class="feature-item"><h3>24/7</h3><p>Support</p></div>
            </div>
        </div>
    </section>
    <section class="about">
        <div class="container">
            <h2>Why Choose Us?</h2>
            <p>Email: sasukecrcr@gmail.com | GitHub: github.com/sasukecrc</p>
        </div>
    </section>
    <section class="contact" id="contact">
        <h2>Get In Touch</h2>
        <a href="mailto:sasukecrcr@gmail.com" class="cta-button">Send Email</a>
    </section>
    <footer class="footer">
        <p>&copy; {year} {name}. All rights reserved.</p>
    </footer>
</body>
</html>"""


def upgrade_website(filepath):
    logger.info(f"     Upgrading: {os.path.basename(filepath)}")
    try:
        if not os.path.exists(filepath):
            return {"success": False, "error": "File not found"}
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        improvements = []
        if "fonts.googleapis.com" not in content:
            content = content.replace("</head>", '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">\n</head>')
            improvements.append("Added Google Fonts")
        if "scroll-behavior" not in content:
            content = content.replace("body {", "html { scroll-behavior: smooth; }\nbody {")
            improvements.append("Added smooth scrolling")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return {"success": True, "improvements": improvements}
    except Exception as e:
        return {"success": False, "error": str(e)}


def review_website(filepath):
    try:
        if not os.path.exists(filepath):
            return {"success": False, "error": "File not found"}
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        issues = []
        suggestions = []
        if "<meta name=\"viewport\"" not in content:
            issues.append("Missing viewport meta tag")
        if "smooth scroll" not in content.lower():
            suggestions.append("Add smooth scrolling")
        if "animation" not in content.lower():
            suggestions.append("Add CSS animations")
        size_kb = len(content) / 1024
        score = max(0, 100 - len(issues) * 20 - len(suggestions) * 5)
        return {"success": True, "score": score, "issues": issues, "suggestions": suggestions, "size_kb": round(size_kb, 1)}
    except Exception as e:
        return {"success": False, "error": str(e)}


def run_creation_cycle():
    logger.info("  Website Creation Division: Starting...")
    results = {"websites_created": 0, "websites_upgraded": 0, "websites_reviewed": 0, "errors": []}
    try:
        site = create_website("PremiumWeb", "Demo Client")
        if site.get("success"):
            results["websites_created"] = 1
            review = review_website(site["filepath"])
            if review.get("success"):
                results["websites_reviewed"] = 1
            upgrade = upgrade_website(site["filepath"])
            if upgrade.get("success"):
                results["websites_upgraded"] = 1
    except Exception as e:
        results["errors"].append(str(e))
    return results


def run_marketing_cycle():
    logger.info("  Marketing Division: Starting...")
    results = {"linkedin_posts": 0, "errors": []}
    try:
        from config import LINKEDIN_POSTS
        tracking_file = "data/linkedin_tracker.json"
        last_index = -1
        try:
            with open(tracking_file, "r") as f:
                tracking = json.load(f)
                last_index = tracking.get("last_post_index", -1)
        except:
            tracking = {"last_post_index": -1, "total_posts": 0}
        post_index = (last_index + 1) % len(LINKEDIN_POSTS)
        post = LINKEDIN_POSTS[post_index]
        result = post_linkedin_update(post["content"])
        if result.get("success"):
            tracking["last_post_index"] = post_index
            tracking["total_posts"] = tracking.get("total_posts", 0) + 1
            with open(tracking_file, "w") as f:
                json.dump(tracking, f, indent=2)
            results["linkedin_posts"] = 1
    except Exception as e:
        results["errors"].append(str(e))
    return results
