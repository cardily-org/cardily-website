#!/usr/bin/env python3
"""Generate Cardily Insights article HTML pages from topic catalogs + body content."""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
ARTICLES = ROOT / "articles"
CATEGORY = ROOT / "category"

CATEGORY_META = {
    "diseases-and-conditions": {
        "label": "Diseases and Conditions",
        "href": "category/diseases-and-conditions.html",
        "description": "Evidence-based explainers on cardiovascular diseases, conditions, and the factors that shape heart health.",
    },
    "prevention-and-lifestyle": {
        "label": "Prevention and Lifestyle",
        "href": "category/prevention-and-lifestyle.html",
        "description": "Clear coverage of prevention, everyday habits, and lifestyle factors connected to cardiovascular health.",
    },
    "research-and-innovation": {
        "label": "Research and Innovation",
        "href": "category/research-and-innovation.html",
        "description": "Accessible perspectives on emerging studies, scientific advances, and innovation in cardiovascular health.",
    },
    "data-and-statistics": {
        "label": "Data and Statistics",
        "href": "category/data-and-statistics.html",
        "description": "Understand cardiovascular trends, risk factors, outcomes, and public health data through clear analysis.",
    },
}

NAV = """
                <li><a href="../index.html">Home</a></li>
                <li class="nav-item-dropdown">
                    <a href="../insights.html" class="active">Insights</a>
                    <ul class="nav-dropdown">
                        <li><a href="../category/diseases-and-conditions.html">Diseases and Conditions</a></li>
                        <li><a href="../category/prevention-and-lifestyle.html">Prevention and Lifestyle</a></li>
                        <li><a href="../category/research-and-innovation.html">Research and Innovation</a></li>
                        <li><a href="../category/data-and-statistics.html">Data and Statistics</a></li>
                    </ul>
                </li>
                <li class="nav-item-dropdown">
                    <a href="../research.html">Research</a>
                    <ul class="nav-dropdown">
                        <li><a href="../research.html#opportunities">Research Opportunities</a></li>
                        <li><a href="../research.html#current">Current Research</a></li>
                    </ul>
                </li>
                <li class="nav-item-dropdown">
                    <a href="../projects.html">Projects</a>
                    <ul class="nav-dropdown">
                        <li><a href="../projects.html#current">Current Projects</a></li>
                        <li><a href="../projects.html#upcoming">Upcoming Projects</a></li>
                    </ul>
                </li>
                <li><a href="../newsletters.html">Newsletter</a></li>
                <li><a href="../get-involved.html">Get Involved</a></li>
                <li><a href="../about.html">About</a></li>
"""

NAV_ROOT = NAV.replace("../", "")

FOOTER = """
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <img src="{logo}" alt="Cardily" class="logo-footer">
                    <p>Advancing cardiovascular health through education, research, and community</p>
                </div>
                <div class="footer-links">
                    <div class="footer-column">
                        <h4>Explore</h4>
                        <ul>
                            <li><a href="{insights}">Insights</a></li>
                            <li><a href="{research}">Research</a></li>
                            <li><a href="{projects}">Projects</a></li>
                            <li><a href="{newsletters}">Newsletter</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>Get Involved</h4>
                        <ul>
                            <li><a href="{involved}">Opportunities</a></li>
                            <li><a href="{contact_p}">Partnerships</a></li>
                            <li><a href="{contact_g}">Contact</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h4>About</h4>
                        <ul>
                            <li><a href="{about}">About Cardily</a></li>
                            <li><a href="{privacy}">Privacy Policy</a></li>
                            <li><a href="{terms}">Terms of Service</a></li>
                            <li><a href="{disclaimer}">Medical Disclaimer</a></li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 Cardily. All rights reserved. | <a href="{privacy}">Privacy Policy</a> | <a href="{terms}">Terms of Service</a></p>
                <p class="footer-disclaimer">Cardily content is for educational purposes only and does not constitute medical advice. Always consult a qualified healthcare professional for medical concerns. | <a href="{disclaimer}">Medical Disclaimer</a></p>
            </div>
        </div>
    </footer>
"""


def footer(prefix: str = "../") -> str:
    return FOOTER.format(
        logo=f"{prefix}calogo (1).png",
        insights=f"{prefix}insights.html",
        research=f"{prefix}research.html",
        projects=f"{prefix}projects.html",
        newsletters=f"{prefix}newsletters.html",
        involved=f"{prefix}get-involved.html",
        contact_p=f"{prefix}contact.html?type=partnership",
        contact_g=f"{prefix}contact.html?type=general",
        about=f"{prefix}about.html",
        privacy=f"{prefix}privacy-policy.html",
        terms=f"{prefix}terms-of-service.html",
        disclaimer=f"{prefix}medical-disclaimer.html",
    )


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def load_topics() -> list[dict]:
    files = [
        "topics-diseases.json",
        "topics-prevention.json",
        "topics-research.json",
        "topics-data.json",
        "topics.json",
    ]
    topics: list[dict] = []
    seen: set[str] = set()
    for name in files:
        path = CONTENT / name
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and "topics" in data:
            data = data["topics"]
        for item in data:
            slug = item["slug"]
            if slug in seen:
                continue
            seen.add(slug)
            topics.append(item)
    return topics


def load_bodies() -> dict[str, dict]:
    """Load bodies; premium chunk files override enriched defaults."""
    bodies: dict[str, dict] = {}
    paths = [CONTENT / "article-bodies.json"]
    paths.extend(sorted(CONTENT.glob("bodies-premium-*.json")))
    for path in paths:
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else list(data.values())
        for item in items:
            slug = item.get("slug")
            if not slug:
                continue
            prev = bodies.get(slug)
            # later premium files win; premium/handcrafted always win over generated
            if prev and prev.get("tier") == "premium" and item.get("tier") != "premium":
                continue
            bodies[slug] = item
    return bodies


def default_sources(category: str) -> list[dict]:
    base = [
        {
            "label": "American Heart Association — Heart and Stroke Resources",
            "url": "https://www.heart.org/",
        },
        {
            "label": "CDC — Heart Disease",
            "url": "https://www.cdc.gov/heart-disease/",
        },
        {
            "label": "National Heart, Lung, and Blood Institute (NHLBI)",
            "url": "https://www.nhlbi.nih.gov/",
        },
        {
            "label": "American College of Cardiology",
            "url": "https://www.acc.org/",
        },
    ]
    if category == "data-and-statistics":
        base.insert(
            0,
            {
                "label": "AHA Heart Disease & Stroke Statistics",
                "url": "https://www.heart.org/en/around-the-aha/heart-and-stroke-statistics",
            },
        )
    if category == "research-and-innovation":
        base.insert(
            0,
            {
                "label": "PubMed — Biomedical Literature",
                "url": "https://pubmed.ncbi.nlm.nih.gov/",
            },
        )
    return base


def synthesize_body(topic: dict) -> dict:
    """Create a substantial educational body when a handcrafted body is missing."""
    title = topic["title"]
    summary = topic.get("summary", "")
    angle = topic.get("angle", "clear mechanism-first teaching")
    outline = topic.get("outline") or [
        "Why this topic matters",
        "Core concepts to understand",
        "How clinicians and researchers think about it",
        "What students and curious readers should notice",
        "Questions worth taking to a clinician",
    ]
    keywords = topic.get("keywords") or []
    kw = ", ".join(keywords[:6]) if keywords else title.lower()
    category = topic["category"]
    cat_label = CATEGORY_META[category]["label"]
    difficulty = topic.get("difficulty", "intro")
    audience = topic.get("audience", "both")

    audience_line = {
        "students": "This piece is tuned for students building durable cardiovascular intuition.",
        "patients-general": "This piece is tuned for general readers who want clarity without clinical jargon overload.",
        "both": "This piece is written for both students and general readers who want rigorous clarity.",
    }.get(audience, "This piece is written for learners seeking rigorous clarity.")

    difficulty_line = {
        "intro": "We keep the entry point accessible, then layer mechanism.",
        "intermediate": "We assume basic heart vocabulary and push into mechanisms, tradeoffs, and evidence quality.",
        "advanced": "We assume familiarity with core cardiology language and focus on nuance, limits of evidence, and common expert pitfalls.",
    }.get(difficulty, "We balance accessibility with precision.")

    takeaways = [
        f"{title} belongs in Cardily’s {cat_label} library as education — not as a personal care plan.",
        f"Learning angle: {angle}.",
        f"Anchor terms to track: {kw}.",
        "Prefer absolute risk, study design, and clinical context over headlines or single-study certainty.",
        "Urgent symptoms (severe chest pain, trouble breathing, sudden weakness, fainting with concerning features) need emergency care — not an article.",
    ]

    category_bridges = {
        "diseases-and-conditions": [
            "Disease explainers work best when they separate phenotype (what we observe), mechanism (what drives it), and management categories (what care teams discuss) without collapsing those layers into DIY treatment instructions.",
            "Many cardiovascular conditions sit on a spectrum. Mild forms, atypical presentations, and look-alike diagnoses are why clinicians gather history, exam findings, and tests instead of relying on a single buzzword.",
        ],
        "prevention-and-lifestyle": [
            "Prevention literacy is strongest when habits are linked to biology — blood pressure load, lipid particles, insulin resistance, sleep debt, nicotine exposure — rather than aesthetic goals or internet extremes.",
            "Sustainable change usually beats perfect short-term restriction. Educational prevention content should reduce friction, not manufacture guilt.",
        ],
        "research-and-innovation": [
            "Innovation coverage should teach readers how evidence is generated: design, endpoints, bias, generalizability, and the gap between a promising signal and practice-ready care.",
            "New devices, drugs, and algorithms earn trust through transparent methods and reproducible benefit — not through marketing vocabulary.",
        ],
        "data-and-statistics": [
            "Cardiovascular statistics are tools for thinking. Rates, risks, and rankings only become meaningful when definitions, denominators, and adjustment methods are clear.",
            "A responsible reader asks what is being counted, in whom, over what time, and what residual confounding or coding drift might remain.",
        ],
    }

    bridge_a, bridge_b = category_bridges.get(category, category_bridges["diseases-and-conditions"])

    sections = []
    for i, heading in enumerate(outline[:6]):
        if i == 0:
            paras = [
                f"{summary}",
                f"{audience_line} {difficulty_line}",
                f"The educational aim of “{title}” is not to turn readers into diagnosticians. It is to build a stable mental model: what the topic names, why it matters in cardiovascular health, and which distinctions prevent expensive misunderstandings later.",
                bridge_a,
                f"Keep the working angle visible throughout: {angle}. When a paragraph drifts into trivia or fear, return to that angle.",
            ]
        elif i == 1:
            paras = [
                f"“{heading}” is where vocabulary becomes useful. Cardiovascular communication mixes metaphor (“blocked pipe,” “stiff pump,” “electrical short”) with measurement language (pressure, flow, ejection fraction, risk scores). Good learners translate freely in both directions.",
                f"For {title.lower()}, map ideas onto structure, function, and disruption. Structure asks what anatomy or system is involved. Function asks what that system is supposed to do. Disruption asks what fails, compensates, or becomes risky over time.",
                f"Related terms you will see around this topic include {kw}. You do not need to memorize a dictionary on day one; you need to know which term is a mechanism, which is a syndrome label, and which is a test finding.",
                bridge_b,
                "A practical drill: write one sentence definition, one sentence mechanism, and one sentence misconception. If you cannot separate those three, the concept is still fuzzy.",
            ]
        elif i == 2:
            paras = [
                f"Under “{heading}”, think like a careful clinician or scientist without pretending to be one. Real-world evaluation usually sequences history, examination, and selectively chosen tests, then interprets results against guidelines and the whole patient — age, other conditions, medications, values, and access to care.",
                "Educational articles can describe those categories. They cannot decide which test you personally need, which medication is appropriate, or whether a finding is urgent.",
                "When reading studies or news about this topic, inspect the endpoint (death, hospitalization, symptom score, or lab surrogate), the population enrolled, follow-up length, and whether benefits are shown as relative change, absolute change, or both.",
                "Also notice exclusion criteria. Trials and registries often under-represent older adults, pregnant people, and communities facing the highest burden of disease. That gap is part of interpreting “what the evidence says.”",
                f"For {title}, ask whether a claim is about pathophysiology, prognosis, screening, or treatment effect. Mixing those claim-types is a common source of viral confusion.",
            ]
        elif i == 3:
            paras = [
                f"“{heading}” is a checkpoint for durable learning. Students and serious autodidacts should be able to teach the topic back in plain language, then re-introduce two technical terms precisely.",
                f"A strong model of {title} includes (1) high-confidence basics, (2) areas still evolving, and (3) decisions that depend on individual risk and preferences. Scientific humility is not indecision; it is calibrated confidence.",
                "Watch for false shortcuts: assuming every chest symptom is coronary disease, assuming a normal ejection fraction means a normal heart, assuming a relative risk reduction of 30% is always a large personal benefit, or assuming a wearable alert equals a diagnosis.",
                "Compare sources. Prefer primary guidelines, major public-health agencies, and peer-reviewed syntheses over anonymous threads. When sources disagree, identify whether they disagree on definitions, populations, or values.",
                f"Because this Insight sits in {cat_label}, connect it outward: disease knowledge informs prevention; prevention data inform research questions; research methods discipline how we read statistics.",
            ]
        else:
            paras = [
                f"Use “{heading}” to convert reading into better conversations. Bring concrete questions: What does this mean for my overall risk? Which screening or diagnostic steps fit my age and history? Which uncertainties should we decide together?",
                "If you are supporting a family member, ask about warning symptoms, follow-up timing, medication purposes at a high level, and trustworthy educational materials — still leaving prescribing and diagnosis to the care team.",
                "Cardily’s lane is educational clarity for the next generation of cardiovascular learners and the public. Personal diagnosis, dosing, and emergency decisions belong with licensed clinicians and emergency services.",
                "If learning this topic raised anxiety, that is common. Pair curiosity with care: continue studying mechanisms and evidence, and route personal symptoms to appropriate clinical channels.",
                f"Suggested next step inside the library: browse related {cat_label} Insights, then cross-check one research-literacy or data-literacy piece so methods stay attached to facts.",
            ]
        sections.append({"heading": heading, "paragraphs": paras})

    # Closing synthesis section for length + uniqueness
    sections.append(
        {
            "heading": "Putting it together",
            "paragraphs": [
                f"“{title}” rewards slow reading. The payoff is not a memorized slogan; it is the ability to notice when a claim is precise, when it is overextended, and when a personal question needs a clinician.",
                f"Return to the spine of the piece: {angle}. Hold the keyword cluster ({kw}) as a retrieval cue. Revisit absolute versus relative risk whenever numbers appear.",
                "Cardily publishes this library to make cardiology more learnable — transparent about uncertainty, respectful of clinical boundaries, and ambitious about public understanding.",
            ],
        }
    )

    return {
        "slug": topic["slug"],
        "takeaways": takeaways,
        "sections": sections,
        "sources": default_sources(category),
        "reading_minutes": 9 if difficulty == "intro" else 11 if difficulty == "intermediate" else 13,
        "reviewed": False,
        "generated": True,
    }


def render_article(topic: dict, body: dict, related: list[dict]) -> str:
    cat = CATEGORY_META[topic["category"]]
    title = topic["title"]
    summary = topic.get("summary", "")
    published = body.get("published") or date.today().isoformat()
    minutes = body.get("reading_minutes") or max(6, min(14, 4 + len(body.get("sections", [])) * 2))
    difficulty = topic.get("difficulty", "intro").title()
    audience = topic.get("audience", "both").replace("-", " ").title()

    takeaways_html = "\n".join(f"                        <li>{esc(t)}</li>" for t in body.get("takeaways", []))
    sections_html = []
    for section in body.get("sections", []):
        paras = "\n".join(f"                    <p>{esc(p)}</p>" for p in section.get("paragraphs", []))
        sections_html.append(
            f"""                <section class="article-section">
                    <h2>{esc(section["heading"])}</h2>
{paras}
                </section>"""
        )
    sources_html = "\n".join(
        f'                        <li><a href="{esc(s["url"])}" target="_blank" rel="noopener noreferrer">{esc(s["label"])}</a></li>'
        for s in body.get("sources", default_sources(topic["category"]))
    )
    related_html = "\n".join(
        f'                        <li><a href="{esc(r["slug"])}.html">{esc(r["title"])}</a></li>'
        for r in related[:4]
    ) or "                        <li><a href=\"../insights.html\">Browse all Insights</a></li>"

    review_note = (
        "This article was generated as part of Cardily’s educational library expansion and is structured for student and public learning. It is not a substitute for clinical judgment."
        if body.get("generated")
        else "This article is part of Cardily’s educational Insights library."
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>{esc(title)} - Cardily Insights</title>
    <meta name="title" content="{esc(title)} - Cardily Insights">
    <meta name="description" content="{esc(summary)}">
    <meta name="robots" content="index, follow">
    <link rel="icon" type="image/png" href="../calogo (1).png">
    <link rel="stylesheet" href="../styles.css?v=20261010-articles">
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
                <a href="../index.html"><img src="../calogo (1).png" alt="Cardily" class="logo"></a>
            </div>
            <ul class="nav-menu">
{NAV}
            </ul>
            <button class="mobile-menu-toggle" aria-label="Toggle menu">
                <span></span>
                <span></span>
                <span></span>
            </button>
        </div>
    </nav>

    <article class="insight-article">
        <header class="article-hero">
            <div class="container">
                <div class="article-hero-inner">
                    <nav class="article-breadcrumb" aria-label="Breadcrumb">
                        <a href="../insights.html">Insights</a>
                        <span aria-hidden="true">/</span>
                        <a href="../{cat["href"]}">{esc(cat["label"])}</a>
                    </nav>
                    <p class="article-kicker">{esc(cat["label"])}</p>
                    <h1>{esc(title)}</h1>
                    <p class="article-deck">{esc(summary)}</p>
                    <div class="article-meta">
                        <span>{esc(published)}</span>
                        <span>{minutes} min read</span>
                        <span>{esc(difficulty)}</span>
                        <span>{esc(audience)}</span>
                    </div>
                </div>
            </div>
        </header>

        <div class="container">
            <div class="article-layout">
                <div class="article-main">
                    <aside class="article-takeaways" aria-label="Key takeaways">
                        <h2>Key takeaways</h2>
                        <ul>
{takeaways_html}
                        </ul>
                    </aside>

{chr(10).join(sections_html)}

                    <section class="article-section article-disclaimer-box">
                        <h2>Educational disclaimer</h2>
                        <p>{esc(review_note)} Cardily content is for educational and informational purposes only and does not constitute medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for personal medical concerns. In an emergency, call local emergency services.</p>
                        <p><a href="../medical-disclaimer.html">Read the full medical disclaimer</a></p>
                    </section>

                    <section class="article-section">
                        <h2>Selected learning sources</h2>
                        <ul class="article-sources">
{sources_html}
                        </ul>
                    </section>
                </div>

                <aside class="article-sidebar">
                    <div class="article-sidebar-card">
                        <h2>Related Insights</h2>
                        <ul>
{related_html}
                        </ul>
                    </div>
                    <div class="article-sidebar-card">
                        <h2>Keep learning</h2>
                        <p>Explore more evidence-based cardiovascular education across Cardily Insights.</p>
                        <a class="btn btn-primary" href="../insights.html">Browse library</a>
                    </div>
                </aside>
            </div>
        </div>
    </article>

    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="18 15 12 9 6 15"></polyline>
        </svg>
    </button>

{footer("../")}

    <script src="../script.js?v=20261010-articles"></script>
</body>
</html>
"""


def render_category_page(category: str, topics: list[dict]) -> str:
    meta = CATEGORY_META[category]
    cards = []
    for t in topics:
        cards.append(
            f"""                    <a class="insight-article-card" href="../articles/{esc(t["slug"])}.html">
                        <span class="insight-article-card-category">{esc(meta["label"])}</span>
                        <h3>{esc(t["title"])}</h3>
                        <p>{esc(t.get("summary", ""))}</p>
                        <span class="insight-article-card-meta">{esc(t.get("difficulty", "intro").title())} · {esc(t.get("audience", "both").replace("-", " ").title())}</span>
                    </a>"""
        )
    cards_html = "\n".join(cards) if cards else '<p class="insights-empty-copy">Articles are being published to this category.</p>'

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(meta["label"])} - Cardily Insights</title>
    <meta name="description" content="{esc(meta["description"])}">
    <link rel="icon" type="image/png" href="../calogo (1).png">
    <link rel="stylesheet" href="../styles.css?v=20261010-articles">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
</head>
<body>
    <div class="page-loader"><div class="loader-content"><div class="loader-spinner"></div></div></div>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <a href="../index.html"><img src="../calogo (1).png" alt="Cardily" class="logo"></a>
            </div>
            <ul class="nav-menu">
{NAV}
            </ul>
            <button class="mobile-menu-toggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
        </div>
    </nav>

    <section class="page-hero insights-hero">
        <div class="container">
            <div class="page-content">
                <p class="article-kicker"><a href="../insights.html" style="color:inherit;">Insights</a> / {esc(meta["label"])}</p>
                <h1>{esc(meta["label"])}</h1>
                <p>{esc(meta["description"])} {len(topics)} articles in this collection.</p>
            </div>
        </div>
    </section>

    <section class="page-section insights-library">
        <div class="container">
            <div class="insight-article-grid">
{cards_html}
            </div>
        </div>
    </section>

    <button id="back-to-top" class="back-to-top" aria-label="Back to top">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="18 15 12 9 6 15"></polyline></svg>
    </button>
{footer("../")}
    <script src="../script.js?v=20261010-articles"></script>
</body>
</html>
"""


def write_manifest(topics: list[dict]) -> None:
    manifest = []
    for t in topics:
        manifest.append(
            {
                "slug": t["slug"],
                "title": t["title"],
                "category": t["category"],
                "summary": t.get("summary", ""),
                "difficulty": t.get("difficulty", "intro"),
                "audience": t.get("audience", "both"),
                "href": f"articles/{t['slug']}.html",
            }
        )
    (CONTENT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    js = "window.CARDILY_ARTICLES = " + json.dumps(manifest) + ";\n"
    (CONTENT / "manifest.js").write_text(js, encoding="utf-8")


def related_for(topic: dict, all_topics: list[dict], n: int = 4) -> list[dict]:
    same = [t for t in all_topics if t["category"] == topic["category"] and t["slug"] != topic["slug"]]
    others = [t for t in all_topics if t["category"] != topic["category"]]
    picks = same[:n]
    if len(picks) < n:
        picks.extend(others[: n - len(picks)])
    return picks


def main() -> None:
    ARTICLES.mkdir(exist_ok=True)
    CATEGORY.mkdir(exist_ok=True)
    topics = load_topics()
    if not topics:
        raise SystemExit("No topics found in content/*.json")

    bodies = load_bodies()
    write_manifest(topics)

    by_cat: dict[str, list[dict]] = {k: [] for k in CATEGORY_META}
    for topic in topics:
        body = bodies.get(topic["slug"]) or synthesize_body(topic)
        html = render_article(topic, body, related_for(topic, topics))
        (ARTICLES / f"{topic['slug']}.html").write_text(html, encoding="utf-8")
        by_cat.setdefault(topic["category"], []).append(topic)

    for cat, items in by_cat.items():
        if cat not in CATEGORY_META:
            continue
        (CATEGORY / f"{cat}.html").write_text(render_category_page(cat, items), encoding="utf-8")

    print(f"Generated {len(topics)} articles across {sum(1 for v in by_cat.values() if v)} categories.")
    # Keep Insights index in sync with static cards
    try:
        from build_insights_page import main as build_insights
        build_insights()
    except Exception as exc:
        import subprocess, sys
        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build_insights_page.py")])


if __name__ == "__main__":
    main()
