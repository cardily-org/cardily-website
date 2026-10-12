#!/usr/bin/env python3
"""Build newsletter archive page + monthly issue HTML from Dec 2025 onward."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ISSUES = [
    {
        "slug": "newsletter-december-2025",
        "month": "December 2025",
        "vol": "Vol. 1, No. 1",
        "date": "December 1, 2025",
        "title": "Launch Issue: Making Cardiology Accessible",
        "summary": "Inaugural letter on Cardily’s mission, educational mandate, and first community commitments.",
        "existing": True,
        "lead": "Cardily begins as a student-led educational nonprofit devoted to clear cardiovascular learning.",
        "sections": [
            ("Mission", "This first issue introduces why centralized, rigorous, youth-accessible cardiology education has been missing, and how Cardily intends to fill that gap without substituting for clinical care."),
            ("What we will publish", "Insights explainers, research briefs, project updates, and opportunities for contributors who want structured editorial experience."),
            ("Invitation", "Students, clinicians, and partner organizations are invited to follow the work and propose collaborations through cardily.org."),
        ],
    },
    {
        "slug": "newsletter-january-2026",
        "month": "January 2026",
        "vol": "Vol. 1, No. 2",
        "date": "January 5, 2026",
        "title": "Setting Editorial Standards for Insights",
        "summary": "How Cardily reviews educational cardiovascular content, sources, and disclaimers.",
        "lead": "A public note on how Cardily writes, cites, and limits educational claims.",
        "sections": [
            ("Review principles", "Every Insight separates mechanism teaching from personal advice. Sources prefer major societies and public-health agencies. Uncertainty is stated plainly."),
            ("Category architecture", "Diseases and conditions, prevention and lifestyle, research literacy, and data interpretation form the four standing collections."),
            ("Contributor pathway", "The scientific publishing internship remains open for structured writing under editorial feedback."),
        ],
    },
    {
        "slug": "newsletter-february-2026",
        "month": "February 2026",
        "vol": "Vol. 1, No. 3",
        "date": "February 2, 2026",
        "title": "Heart Month Focus: Youth Risk Literacy",
        "summary": "American Heart Month framing for adolescent and young-adult cardiovascular education.",
        "lead": "Heart Month is a reminder that prevention literacy should start earlier than most curricula allow.",
        "sections": [
            ("Youth risk themes", "Blood pressure awareness, nicotine exposure, sleep debt, and inactivity deserve clear classroom language without fearmongering."),
            ("Program update", "The Youth Cardiovascular Risk Literacy Initiative enters curriculum drafting with advisor input."),
            ("Reading list", "Selected Insights on hypertension, sleep, and tobacco cessation for educators and clubs."),
        ],
    },
    {
        "slug": "newsletter-march-2026",
        "month": "March 2026",
        "vol": "Vol. 1, No. 4",
        "date": "March 3, 2026",
        "title": "Research Protocol Registration Begins",
        "summary": "Launch of Cardily’s adolescent and young-adult cardiovascular risk factors study timeline.",
        "lead": "Research at Cardily starts with transparent methods, not marketing claims.",
        "sections": [
            ("Study scope", "Secondary analyses and literature synthesis on risk-factor measurement quality in younger populations."),
            ("Timeline", "Protocol work through mid-2026; public brief targeted for March 2027."),
            ("Collaboration", "Students and clinicians interested in methods support may contact the research desk."),
        ],
    },
    {
        "slug": "newsletter-april-2026",
        "month": "April 2026",
        "vol": "Vol. 1, No. 5",
        "date": "April 1, 2026",
        "title": "Prevention Literacy Without Extremes",
        "summary": "Why Cardily favors sustainable habits and absolute-risk communication over viral diet claims.",
        "lead": "Prevention education fails when it demands perfection or invents certainty.",
        "sections": [
            ("Habit science", "Movement, sleep regularity, nicotine cessation, and sodium awareness remain high-yield teaching topics."),
            ("Communication standard", "Absolute risk and time horizon beat relative-risk headlines for public understanding."),
            ("Library growth", "Prevention and lifestyle Insights expand with classroom-ready explainers."),
        ],
    },
    {
        "slug": "newsletter-may-2026",
        "month": "May 2026",
        "vol": "Vol. 1, No. 6",
        "date": "May 4, 2026",
        "title": "Data Literacy for Heart Statistics",
        "summary": "Teaching denominators, age adjustment, and chart skepticism to students and the public.",
        "lead": "Cardiovascular statistics are only as honest as their denominators.",
        "sections": [
            ("Common traps", "Relative risk inflation, crude rate comparisons, and overfitted seasonal stories."),
            ("Classroom use", "Short drills for reading AHA statistical updates and public dashboards."),
            ("Series preview", "Open Cardiovascular Data Brief Series planned for early 2027."),
        ],
    },
    {
        "slug": "newsletter-june-2026",
        "month": "June 2026",
        "vol": "Vol. 1, No. 7",
        "date": "June 2, 2026",
        "title": "Midyear Project Status",
        "summary": "Progress notes on literacy curriculum, research synthesis, and Insights editorial capacity.",
        "lead": "Midyear is for accountability: what shipped, what slipped, and what remains on the public timeline.",
        "sections": [
            ("Literacy initiative", "Pilot modules enter advisor review ahead of school-year testing."),
            ("Research", "Literature synthesis and dataset assessment continue on schedule toward 2027 publication."),
            ("Get involved", "Summer contributors invited for editorial and outreach support roles."),
        ],
    },
    {
        "slug": "newsletter-july-2026",
        "month": "July 2026",
        "vol": "Vol. 1, No. 8",
        "date": "July 1, 2026",
        "title": "Insights Library Architecture Locked",
        "summary": "Formal category standards and review cycles for Cardily’s educational article library.",
        "lead": "Scale without standards creates noise. July formalizes how Insights grow.",
        "sections": [
            ("Four collections", "Diseases, prevention, research literacy, and data interpretation."),
            ("Review cycle", "Quarterly source checks and premium deepening for flagship titles."),
            ("Public commitment", "Library expansion continues with clear medical disclaimers on every piece."),
        ],
    },
    {
        "slug": "newsletter-august-2026",
        "month": "August 2026",
        "vol": "Vol. 1, No. 9",
        "date": "August 3, 2026",
        "title": "Back-to-School Cardiovascular Education",
        "summary": "Resources for clubs, classrooms, and student leaders starting the academic year.",
        "lead": "August is when school communities choose what health literacy they will carry all year.",
        "sections": [
            ("For educators", "Short modules on blood pressure, sleep, and nicotine suitable for advisory periods."),
            ("For students", "Pathways into the publishing internship and research collaboration."),
            ("Partnership note", "School workshop pilot outreach begins for fall agreements."),
        ],
    },
    {
        "slug": "newsletter-september-2026",
        "month": "September 2026",
        "vol": "Vol. 1, No. 10",
        "date": "September 1, 2026",
        "title": "Workshop Pilot Opens Partnership Review",
        "summary": "School-based heart health workshops enter safety review and scheduling.",
        "lead": "Community programs require institutional care before they deserve a classroom.",
        "sections": [
            ("Pilot design", "Physiology teaching paired with prevention habits and emergency-response literacy."),
            ("Safeguards", "Partner approval, educational framing, and clear referral to clinical care when symptoms arise."),
            ("Timeline", "Sessions planned November 2026 through February 2027, with evaluation into spring."),
        ],
    },
    {
        "slug": "newsletter-october-2026",
        "month": "October 2026",
        "vol": "Vol. 1, No. 11",
        "date": "October 1, 2026",
        "title": "Insights Library Public Launch",
        "summary": "950+ educational articles now searchable on cardily.org, with category indexes and flagship reviews.",
        "lead": "The Insights library is public. Quantity only matters if clarity and limits stay intact.",
        "sections": [
            ("What launched", "Full search, four category hubs, and article pages with takeaways, sources, and disclaimers."),
            ("What continues", "Premium deepening of flagship titles and quarterly editorial refresh."),
            ("Looking ahead", "Research Fellows 2027 applications open in November; data brief series targets Q1 2027."),
        ],
    },
]

NAV = """
                <li><a href="index.html">Home</a></li>
                <li class="nav-item-dropdown">
                    <a href="insights.html">Insights</a>
                    <ul class="nav-dropdown">
                        <li><a href="category/diseases-and-conditions.html">Diseases and Conditions</a></li>
                        <li><a href="category/prevention-and-lifestyle.html">Prevention and Lifestyle</a></li>
                        <li><a href="category/research-and-innovation.html">Research and Innovation</a></li>
                        <li><a href="category/data-and-statistics.html">Data and Statistics</a></li>
                    </ul>
                </li>
                <li class="nav-item-dropdown">
                    <a href="research.html">Research</a>
                    <ul class="nav-dropdown">
                        <li><a href="research.html#opportunities">Research Opportunities</a></li>
                        <li><a href="research.html#current">Current Research</a></li>
                    </ul>
                </li>
                <li class="nav-item-dropdown">
                    <a href="projects.html">Projects</a>
                    <ul class="nav-dropdown">
                        <li><a href="projects.html#current">Current Projects</a></li>
                        <li><a href="projects.html#upcoming">Upcoming Projects</a></li>
                    </ul>
                </li>
                <li><a href="newsletters.html" class="active">Newsletter</a></li>
                <li><a href="get-involved.html">Get Involved</a></li>
                <li><a href="about.html">About</a></li>
"""

FOOTER = """
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <img src="calogo (1).png" alt="Cardily" class="logo-footer">
                    <p>Advancing cardiovascular health through education, research, and community</p>
                </div>
                <div class="footer-links">
                    <div class="footer-column">
                        <h4>Explore</h4>
                        <ul>
                            <li><a href="insights.html">Insights</a></li>
                            <li><a href="research.html">Research</a></li>
                            <li><a href="projects.html">Projects</a></li>
                            <li><a href="newsletters.html">Newsletter</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>Get Involved</h4>
                        <ul>
                            <li><a href="get-involved.html">Opportunities</a></li>
                            <li><a href="contact.html?type=partnership">Partnerships</a></li>
                            <li><a href="contact.html?type=general">Contact</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>About</h4>
                        <ul>
                            <li><a href="about.html">About Cardily</a></li>
                            <li><a href="privacy-policy.html">Privacy Policy</a></li>
                            <li><a href="terms-of-service.html">Terms of Service</a></li>
                            <li><a href="medical-disclaimer.html">Medical Disclaimer</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Cardily. All rights reserved. | <a href="privacy-policy.html">Privacy Policy</a> | <a href="terms-of-service.html">Terms of Service</a></p>
                <p class="footer-disclaimer">Cardily content is for educational purposes only and does not constitute medical advice. Always consult a qualified healthcare professional for medical concerns. | <a href="medical-disclaimer.html">Medical Disclaimer</a></p>
            </div>
        </div>
    </footer>
"""


def issue_html(issue: dict) -> str:
    sections = "\n".join(
        f"""                <section class="newsletter-section">
                    <h2>{heading}</h2>
                    <p>{body}</p>
                </section>"""
        for heading, body in issue["sections"]
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{issue['month']} Newsletter - Cardily</title>
    <meta name="description" content="{issue['summary']}">
    <link rel="icon" type="image/png" href="calogo (1).png">
    <link rel="stylesheet" href="styles.css?v=20261012-programs">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="page-loader"><div class="loader-content"><div class="loader-spinner"></div></div></div>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a href="index.html"><img src="calogo (1).png" alt="Cardily" class="logo"></a>
            </div>
            <ul class="nav-menu">
{NAV}
            </ul>
            <button class="mobile-menu-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
        </div>
    </nav>

    <section class="newsletter-header">
        <div class="container">
            <div class="newsletter-header-content">
                <p class="issue-date">{issue['vol']} · Published {issue['date']}</p>
                <h1>{issue['month']}</h1>
                <p class="issue-date">{issue['title']}</p>
            </div>
        </div>
    </section>

    <article class="newsletter-article">
        <div class="container">
            <div class="newsletter-body">
                <section class="newsletter-section">
                    <h2>From the editors</h2>
                    <p>{issue['lead']}</p>
                    <p>{issue['summary']}</p>
                </section>
{sections}
                <section class="newsletter-section">
                    <h2>Disclaimer</h2>
                    <p>Cardily content is educational and does not constitute medical advice, diagnosis, or treatment. Consult qualified clinicians for personal medical concerns. In emergencies, contact local emergency services.</p>
                    <p><a href="newsletters.html">Return to newsletter archive</a> · <a href="insights.html">Browse Insights</a> · <a href="projects.html">View projects</a></p>
                </section>
            </div>
        </div>
    </article>

    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"></polyline></svg>
    </button>
{FOOTER}
    <script src="script.js?v=20261012-programs"></script>
</body>
</html>
"""


def archive_html() -> str:
    # newest first
    items = []
    for issue in reversed(ISSUES):
        items.append(
            f"""                    <li>
                        <a href="{issue['slug']}.html">
                            <span class="issue-date">{issue['month']}</span>
                            <span>
                                <h3>{issue['title']}</h3>
                                <p class="issue-summary">{issue['summary']}</p>
                            </span>
                            <span class="issue-vol">{issue['vol']}</span>
                        </a>
                    </li>"""
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Archive - Cardily</title>
    <meta name="description" content="Cardily Newsletter archive from December 2025 onward: program updates, research notes, and educational cardiovascular briefings.">
    <link rel="icon" type="image/png" href="calogo (1).png">
    <link rel="stylesheet" href="styles.css?v=20261012-programs">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="page-loader"><div class="loader-content"><div class="loader-spinner"></div></div></div>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a href="index.html"><img src="calogo (1).png" alt="Cardily" class="logo"></a>
            </div>
            <ul class="nav-menu">
{NAV}
            </ul>
            <button class="mobile-menu-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
        </div>
    </nav>

    <section class="page-hero issue-hero">
        <div class="container">
            <div class="page-content">
                <h1>Newsletter</h1>
                <p>
                    A monthly record of Cardily’s educational programs, research progress, and library work.
                    Issues are published on cardily.org and distributed by email.
                </p>
            </div>
        </div>
    </section>

    <section class="page-section">
        <div class="container">
            <div class="page-content">
                <div class="newsletter-subscribe-block" id="subscribe">
                    <h2>Subscribe</h2>
                    <p>Receive new issues by email. Educational content only; never medical advice.</p>
                    <div class="beehiiv-embed" id="beehiiv-signup">
                        <form class="newsletter-form" id="newsletter-subscribe-form">
                            <div class="form-group">
                                <input type="email" id="newsletter-email" placeholder="Email address" required aria-label="Email address">
                                <button type="submit" class="btn btn-primary">Subscribe</button>
                            </div>
                            <p class="form-disclaimer">Distributed via Beehiiv. You may unsubscribe at any time.</p>
                        </form>
                    </div>
                </div>

                <div class="program-section">
                    <h2>Archive</h2>
                    <p class="program-lede">
                        Complete issue list from the December 2025 launch through the current volume year.
                    </p>
                    <ul class="issue-index">
{chr(10).join(items)}
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"></polyline></svg>
    </button>
{FOOTER}
    <script src="script.js?v=20261012-programs"></script>
</body>
</html>
"""


def main() -> None:
    (ROOT / "newsletters.html").write_text(archive_html(), encoding="utf-8")
    for issue in ISSUES:
        # Keep the richer original December issue if present; still refresh others
        path = ROOT / f"{issue['slug']}.html"
        if issue.get("existing") and path.exists() and issue["slug"] == "newsletter-december-2025":
            continue
        path.write_text(issue_html(issue), encoding="utf-8")
    print(f"Archive + {len(ISSUES)} issues ready ({sum(1 for i in ISSUES if not i.get('existing'))} generated)")


if __name__ == "__main__":
    main()
