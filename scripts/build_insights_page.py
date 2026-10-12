#!/usr/bin/env python3
"""Build insights.html with static article cards (no JS required to see content)."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

LABELS = {
    "diseases-and-conditions": "Diseases and Conditions",
    "prevention-and-lifestyle": "Prevention and Lifestyle",
    "research-and-innovation": "Research and Innovation",
    "data-and-statistics": "Data and Statistics",
}

CATEGORY_BLURBS = {
    "diseases-and-conditions": "Evidence-based explainers on cardiovascular diseases, conditions, and the factors that shape heart health.",
    "prevention-and-lifestyle": "Clear coverage of prevention, everyday habits, and lifestyle factors connected to cardiovascular health.",
    "research-and-innovation": "Accessible perspectives on emerging studies, scientific advances, and innovation in cardiovascular health.",
    "data-and-statistics": "Understand cardiovascular trends, risk factors, outcomes, and public health data through clear analysis.",
}

ICONS = {
    "diseases-and-conditions": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 21s-7-4.35-9-9.5C1.4 7.4 4.1 4 7.8 4c2.1 0 3.5 1.2 4.2 2.3C12.7 5.2 14.1 4 16.2 4c3.7 0 6.4 3.4 4.8 7.5C19 16.65 12 21 12 21Z"></path>
                                <path d="M7 12h3l1.2-2.5 1.7 5 1.2-2.5H17"></path>
                            </svg>""",
    "prevention-and-lifestyle": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 22V10"></path>
                                <path d="M12 13C7 13 4 10.5 4 6c5 0 8 2.5 8 7Z"></path>
                                <path d="M12 17c4.5 0 7-2.2 7-6-4.5 0-7 2.2-7 6Z"></path>
                            </svg>""",
    "research-and-innovation": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M9 3h6"></path>
                                <path d="M10 3v6l-5 9a2 2 0 0 0 1.7 3h10.6a2 2 0 0 0 1.7-3l-5-9V3"></path>
                                <path d="M7.5 16h9"></path>
                                <path d="M10 13h4"></path>
                            </svg>""",
    "data-and-statistics": """<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M4 20V10"></path>
                                <path d="M10 20V4"></path>
                                <path d="M16 20v-7"></path>
                                <path d="M22 20H2"></path>
                            </svg>""",
}


def card(a: dict) -> str:
    return f"""                    <a class="insight-article-card" href="{html.escape(a['href'])}" data-category="{html.escape(a['category'])}">
                        <span class="insight-article-card-category">{html.escape(LABELS.get(a['category'], a['category']))}</span>
                        <h3>{html.escape(a['title'])}</h3>
                        <p>{html.escape(a.get('summary', ''))}</p>
                        <span class="insight-article-card-meta">{html.escape((a.get('difficulty') or 'intro').title())} · Open article</span>
                    </a>"""


def main() -> None:
    articles = json.loads((CONTENT / "manifest.json").read_text(encoding="utf-8"))
    counts = Counter(a["category"] for a in articles)
    total = len(articles)

    # Featured: first 6 per category = 24 static cards always visible
    featured = []
    for cat in LABELS:
        featured.extend([a for a in articles if a["category"] == cat][:6])

    cat_cards = []
    for cat, label in LABELS.items():
        n = counts.get(cat, 0)
        cat_cards.append(
            f"""                    <a class="insight-category-card" href="category/{cat}.html">
                        <span class="insight-card-icon" aria-hidden="true">
                            {ICONS[cat]}
                        </span>
                        <span class="insight-card-body">
                            <span class="insight-card-title">{html.escape(label)}</span>
                            <span class="insight-card-description">
                                {html.escape(CATEGORY_BLURBS[cat])}
                            </span>
                            <span class="insight-card-status">{n} articles, browse all</span>
                        </span>
                        <span class="insight-card-arrow" aria-hidden="true">→</span>
                    </a>"""
        )

    featured_html = "\n".join(card(a) for a in featured)
    # Full static library (all articles) so nothing depends on JS
    all_html = "\n".join(card(a) for a in articles)

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    
    <title>Insights - Cardily</title>
    <meta name="title" content="Insights - Cardily">
    <meta name="description" content="Browse {total} evidence-based Cardily Insights on cardiovascular diseases, prevention, research literacy, and data.">
    
    <link rel="icon" type="image/png" href="calogo (1).png">
    <link rel="stylesheet" href="styles.css?v=20261011-insights">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="page-loader">
        <div class="loader-content">
            <div class="loader-spinner"></div>
        </div>
    </div>

    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a href="index.html"><img src="calogo (1).png" alt="Cardily" class="logo"></a>
            </div>
            <ul class="nav-menu">
                <li><a href="index.html">Home</a></li>
                <li class="nav-item-dropdown">
                    <a href="insights.html" class="active">Insights</a>
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
                <li><a href="newsletters.html">Newsletter</a></li>
                <li><a href="get-involved.html">Get Involved</a></li>
                <li><a href="about.html">About</a></li>
            </ul>
            <button class="mobile-menu-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <section class="page-hero insights-hero">
        <div class="container">
            <div class="page-content">
                <h1>Insights</h1>
                <p>
                    <strong>{total} educational articles</strong> on cardiovascular health, diseases, prevention,
                    research literacy, and data. Click a category below, or browse the full library on this page.
                </p>
                <p class="insights-hero-actions">
                    <a class="btn btn-primary" href="#library">Browse all articles</a>
                    <a class="btn btn-secondary" href="category/diseases-and-conditions.html">Start with diseases</a>
                </p>
            </div>
        </div>
    </section>

    <section class="page-section insights-library">
        <div class="container">
            <div class="insights-content">
                <div class="insights-section-heading">
                    <span class="insights-eyebrow">Choose a collection</span>
                    <h2>Four ways into the library</h2>
                    <p>
                        Each category opens a full list of articles. No “coming soon”, the library is published.
                    </p>
                </div>

                <div class="insight-category-grid" role="navigation" aria-label="Insight categories">
{chr(10).join(cat_cards)}
                </div>

                <div class="insights-section-heading" style="margin-top: 3rem;">
                    <span class="insights-eyebrow">Start reading</span>
                    <h2>Featured Insights</h2>
                    <p>A sample from each category. Open any card, or jump to the full library beneath.</p>
                </div>

                <div class="insight-article-grid" id="insights-featured">
{featured_html}
                </div>

                <div class="insights-section-heading" style="margin-top: 3.5rem;" id="library">
                    <span class="insights-eyebrow">Full library · {total} articles</span>
                    <h2>Search and filter</h2>
                    <p>Every published Insight is listed below. Use search or filters to narrow the list.</p>
                </div>

                <div class="insights-toolbar" role="search">
                    <input type="search" id="insights-search" class="insights-search" placeholder="Search articles…" aria-label="Search articles">
                    <button type="button" class="insights-filter-btn active" data-filter="all">All ({total})</button>
                    <button type="button" class="insights-filter-btn" data-filter="diseases-and-conditions">Diseases ({counts.get('diseases-and-conditions', 0)})</button>
                    <button type="button" class="insights-filter-btn" data-filter="prevention-and-lifestyle">Prevention ({counts.get('prevention-and-lifestyle', 0)})</button>
                    <button type="button" class="insights-filter-btn" data-filter="research-and-innovation">Research ({counts.get('research-and-innovation', 0)})</button>
                    <button type="button" class="insights-filter-btn" data-filter="data-and-statistics">Data ({counts.get('data-and-statistics', 0)})</button>
                </div>
                <p class="insights-count" id="insights-count">Showing {total} of {total} articles</p>
                <div class="insight-article-grid" id="insights-grid">
{all_html}
                </div>
            </div>
        </div>
    </section>

    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"></polyline>
        </svg>
    </button>

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

    <script src="script.js?v=20261011-insights"></script>
    <script>
    (function () {{
        var grid = document.getElementById('insights-grid');
        var cards = Array.prototype.slice.call(grid.querySelectorAll('.insight-article-card'));
        var countEl = document.getElementById('insights-count');
        var search = document.getElementById('insights-search');
        var filter = 'all';
        var total = {total};

        function render() {{
            var q = (search.value || '').trim().toLowerCase();
            var shown = 0;
            cards.forEach(function (card) {{
                var cat = card.getAttribute('data-category');
                var text = (card.textContent || '').toLowerCase();
                var ok = (filter === 'all' || cat === filter) && (!q || text.indexOf(q) !== -1);
                card.hidden = !ok;
                if (ok) shown += 1;
            }});
            countEl.textContent = 'Showing ' + shown + ' of ' + total + ' articles';
        }}

        document.querySelectorAll('.insights-filter-btn').forEach(function (btn) {{
            btn.addEventListener('click', function () {{
                document.querySelectorAll('.insights-filter-btn').forEach(function (b) {{ b.classList.remove('active'); }});
                btn.classList.add('active');
                filter = btn.getAttribute('data-filter');
                render();
            }});
        }});
        search.addEventListener('input', render);
    }})();
    </script>
</body>
</html>
"""
    (ROOT / "insights.html").write_text(page, encoding="utf-8")
    print(f"Wrote insights.html with {total} static articles and {len(featured)} featured cards")


if __name__ == "__main__":
    main()
