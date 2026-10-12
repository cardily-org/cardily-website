#!/usr/bin/env python3
"""Build richer, topic-specific article bodies for the full Cardily catalog."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

SOURCES = {
    "diseases-and-conditions": [
        {"label": "American Heart Association", "url": "https://www.heart.org/"},
        {"label": "CDC, Heart Disease", "url": "https://www.cdc.gov/heart-disease/"},
        {"label": "NHLBI", "url": "https://www.nhlbi.nih.gov/"},
        {"label": "American College of Cardiology", "url": "https://www.acc.org/"},
    ],
    "prevention-and-lifestyle": [
        {"label": "AHA Life's Essential 8", "url": "https://www.heart.org/en/healthy-living/healthy-lifestyle/lifes-essential-8"},
        {"label": "CDC, Heart Disease Prevention", "url": "https://www.cdc.gov/heart-disease/prevention/"},
        {"label": "NHLBI, Healthy Lifestyle", "url": "https://www.nhlbi.nih.gov/health/heart-healthy-living"},
        {"label": "Dietary Guidelines for Americans", "url": "https://www.dietaryguidelines.gov/"},
    ],
    "research-and-innovation": [
        {"label": "PubMed", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
        {"label": "ClinicalTrials.gov", "url": "https://clinicaltrials.gov/"},
        {"label": "ACC/AHA Guidelines Hub", "url": "https://www.acc.org/guidelines"},
        {"label": "AHA Journals", "url": "https://www.ahajournals.org/"},
    ],
    "data-and-statistics": [
        {"label": "AHA Heart Disease & Stroke Statistics", "url": "https://www.heart.org/en/around-the-aha/heart-and-stroke-statistics"},
        {"label": "CDC Wonder / NCHS", "url": "https://wonder.cdc.gov/"},
        {"label": "Global Burden of Disease", "url": "https://www.healthdata.org/research-analysis/gbd"},
        {"label": "NHANES", "url": "https://www.cdc.gov/nchs/nhanes/index.htm"},
    ],
}

MECHANISM_BANK = {
    "coronary": "Coronary arteries supply oxygen-rich blood to myocardium. When atherosclerotic plaque narrows a lumen-or when plaque ruptures and thrombosis suddenly occludes flow-myocytes face ischemia. Duration and severity of mismatch determine whether tissue recovers, stuns, or infarcts.",
    "atherosclerosis": "Atherosclerosis begins with endothelial injury and lipid retention in the arterial intima. Macrophages become foam cells; fibrous caps form over necrotic cores. Inflammation and mechanical stress influence whether plaques remain stable or become thrombosis-prone.",
    "infarction": "Infarction means irreversible myocyte death from prolonged ischemia. Clinically, injury is often tracked with troponin rise and fall plus ischemic symptoms or ECG changes. Not every troponin elevation equals a classic type 1 plaque-rupture myocardial infarction.",
    "heart-failure": "Heart failure is a clinical syndrome of congestion and/or inadequate cardiac output. It can occur with reduced ejection fraction (pumping weakness) or preserved ejection fraction (often stiff filling). Neurohormonal activation (sympathetic, RAAS) initially compensates, then worsens remodeling.",
    "ejection": "Ejection fraction estimates the fraction of end-diastolic volume ejected each beat. It is useful-but incomplete. Diastolic function, valves, pulmonary pressures, and filling pressures can be abnormal even when EF looks “normal.”",
    "atrial-fibrillation": "In atrial fibrillation, organized atrial contraction is replaced by rapid disorganized activity. Ventricular rate becomes irregularly irregular. Stroke risk relates partly to left-atrial appendage stasis and thrombus formation, which is why anticoagulation discussions are central.",
    "arrhythmia": "Arrhythmias arise from abnormal automaticity, triggered activity, or reentry circuits. Scar, stretch, ischemia, electrolytes, and channelopathies change conduction and refractoriness, creating the substrate for tachycardias or bradyarrhythmias.",
    "hypertension": "Chronically elevated arterial pressure increases afterload and damages vessel walls. Over years this promotes left-ventricular hypertrophy, arterial stiffness, atherosclerosis acceleration, and higher risk of stroke, heart failure, and kidney disease.",
    "stroke": "Ischemic stroke reflects focal brain ischemia from thrombosis or embolism; hemorrhagic stroke reflects vessel rupture. Cardioembolic pathways (for example from atrial fibrillation) connect heart rhythm disorders to brain injury.",
    "valve": "Valves maintain one-way flow. Stenosis obstructs forward flow and raises upstream pressure; regurgitation allows backward volume overload. Severity, acuity, and ventricular compensation determine symptoms and risk.",
    "aortic": "The aorta faces high pressure continuously. Aneurysm means pathologic dilation; dissection means an intimal tear creating a false lumen. Genetics, hypertension, and bicuspid aortopathy are recurring risk themes in educational discussions.",
    "lipid": "ApoB-containing lipoproteins, especially LDL particles, drive atherosclerotic plaque growth. Lifetime exposure matters: earlier and longer elevations generally mean more cumulative plaque burden.",
    "diabetes": "Insulin resistance and hyperglycemia amplify vascular injury through endothelial dysfunction, dyslipidemia patterns, and inflammation. Cardiometabolic risk is therefore shared across glucose, blood pressure, weight, and lipids.",
    "obesity": "Excess adiposity-especially visceral fat-links to hypertension, dyslipidemia, sleep apnea, and inflammation. Risk is not only scale weight; distribution and metabolic context matter.",
    "sleep": "Short or fragmented sleep raises sympathetic tone, impairs glucose handling, and associates with higher blood pressure. Obstructive sleep apnea adds nocturnal hypoxia and hemodynamic swings.",
    "exercise": "Regular aerobic activity improves endothelial function, insulin sensitivity, and blood-pressure profiles. Resistance training adds metabolic and musculoskeletal benefits. Dose, progression, and safety screening matter for individuals with known disease.",
    "sodium": "High sodium intake can expand plasma volume and elevate blood pressure in salt-sensitive people. Population sodium reduction is a classic public-health lever; individual counseling still depends on context (for example heart-failure care plans).",
    "tobacco": "Tobacco smoke injures endothelium, promotes thrombosis, and accelerates atherosclerosis. Cessation reduces risk on a meaningful timeline; dual use with vaping is not a free pass.",
    "statin": "Statins inhibit HMG-CoA reductase, lower LDL-C, and have plaque-stabilizing effects beyond the lab number alone. They are foundational in atherosclerotic risk reduction discussions when indicated.",
    "sglt2": "SGLT2 inhibitors began as glucose-lowering drugs and later showed heart-failure and kidney outcome benefits in major trials. They illustrate how cardiometabolic pathways overlap across specialties.",
    "trial": "A randomized trial assigns interventions by chance to reduce confounding. Readers should still inspect endpoints, blinding, follow-up, adherence, and whether the enrolled population matches the people they care about.",
    "risk": "Risk tools estimate average probabilities in populations with similar profiles. They support conversations; they do not dictate destiny. Absolute risk and time horizon usually communicate better than relative percentages alone.",
    "absolute": "Absolute risk answers “how many events per 100 (or 1000) people over a period.” Relative risk can look large while absolute benefit remains small-especially in low-baseline-risk groups.",
    "prevalence": "Prevalence is existing cases at a time point; incidence is new cases over time. Mixing them produces nonsense comparisons in headlines and student essays alike.",
}

MISCONCEPTIONS = [
    "A normal ECG never rules out all heart disease.",
    "“Relative risk cut by 50%” can still mean a tiny absolute benefit.",
    "Ejection fraction is not a complete report card for the heart.",
    "Young age lowers average risk; it does not make ischemia impossible.",
    "Wearable alerts are screening signals, not automatic diagnoses.",
    "Lifestyle change and medications are often partners, not rivals.",
    "Chest pain has many causes; cardiac causes are not the only dangerous ones-and not every cardiac problem announces itself as classic pain.",
    "One viral study rarely overturns a body of guideline-level evidence overnight.",
]

CLINICAL_FRAMES = [
    "History → focused exam → selective testing → shared interpretation.",
    "Separate mechanism questions from treatment questions from prognosis questions.",
    "Ask what would change management before chasing every abnormal number.",
    "Match urgency to red-flag features, not to anxiety alone or reassurance alone.",
    "Document definitions: what syndrome label is being used, and what evidence supports it.",
]


def slug_tokens(slug: str, title: str, keywords: list[str]) -> list[str]:
    blob = " ".join([slug.replace("-", " "), title.lower(), " ".join(keywords).lower()])
    return re.findall(r"[a-z0-9]+", blob)


def pick_mechanisms(tokens: list[str], n: int = 3) -> list[str]:
    hits = []
    joined = " ".join(tokens)
    for key, text in MECHANISM_BANK.items():
        key_parts = key.split("-")
        if any(p in tokens for p in key_parts) or key.replace("-", " ") in joined:
            hits.append(text)
    # stable fill from hash if few hits
    if len(hits) < n:
        keys = list(MECHANISM_BANK.keys())
        h = int(hashlib.md5(joined.encode()).hexdigest(), 16)
        for i in range(12):
            k = keys[(h + i * 7) % len(keys)]
            if MECHANISM_BANK[k] not in hits:
                hits.append(MECHANISM_BANK[k])
            if len(hits) >= n:
                break
    return hits[:n]


def pick_misc(seed: str, n: int = 2) -> list[str]:
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    out = []
    for i in range(n):
        out.append(MISCONCEPTIONS[(h + i * 3) % len(MISCONCEPTIONS)])
    return out


def pick_frame(seed: str) -> str:
    h = int(hashlib.md5(seed.encode()).hexdigest(), 16)
    return CLINICAL_FRAMES[h % len(CLINICAL_FRAMES)]


def enrich_topic(topic: dict) -> dict:
    title = topic["title"]
    summary = topic.get("summary", "")
    angle = topic.get("angle", "mechanism-first teaching")
    outline = topic.get("outline") or [
        "Why this topic matters",
        "Core concepts to understand",
        "How clinicians and researchers think about it",
        "What learners should notice",
        "Questions for clinical conversations",
    ]
    keywords = topic.get("keywords") or []
    category = topic["category"]
    tokens = slug_tokens(topic["slug"], title, keywords)
    mechanisms = pick_mechanisms(tokens, 3)
    misc = pick_misc(topic["slug"], 2)
    frame = pick_frame(topic["slug"])
    kw = ", ".join(keywords[:6]) if keywords else title.lower()

    takeaways = [
        f"{title} is an educational deep dive-not a personal diagnosis or treatment plan.",
        f"Hold this angle: {angle}.",
        f"Key vocabulary cluster: {kw}.",
        misc[0],
        "Urgent warning symptoms need emergency evaluation, not article self-triage.",
    ]

    sections = []
    for i, heading in enumerate(outline[:5]):
        if i == 0:
            paras = [
                summary,
                f"Cardily’s goal with “{title}” is durable understanding: definitions you can reuse, mechanisms you can sketch, and evidence habits that resist hype.",
                f"Working angle for this Insight: {angle}. If a paragraph becomes trivia, return to that spine.",
                mechanisms[0],
                "Educational content can sharpen questions for clinicians. It cannot replace history-taking, examination, or individualized recommendations.",
            ]
        elif i == 1:
            paras = [
                f"In “{heading}”, start by naming the system under discussion and the failure mode it faces.",
                mechanisms[1],
                f"Related terms around this topic include {kw}. Sort each term into mechanism, syndrome label, test finding, or treatment class-those buckets prevent category errors.",
                "Build a three-layer note: (1) one-sentence definition, (2) one-sentence mechanism, (3) one common public misconception. If any layer is missing, keep studying before debating nuances.",
                mechanisms[2],
            ]
        elif i == 2:
            paras = [
                f"“{heading}” is where clinical reasoning patterns matter. A useful default sequence is: {frame}",
                "Researchers evaluating the same topic will ask about endpoints, bias, generalizability, and absolute effect sizes. Readers should borrow that skepticism even when skimming news summaries.",
                f"For {title.lower()}, distinguish pathophysiology claims from prognostic claims from therapeutic claims. A strong mechanism story does not automatically prove a treatment benefit.",
                "Guideline language often encodes certainty levels. “Is recommended” is not identical to “may be reasonable,” and both differ from early-phase excitement.",
                "When imaging or labs enter the conversation, ask what decision they change. Tests are tools, not trophies.",
            ]
        elif i == 3:
            paras = [
                f"Use “{heading}” as a mastery checkpoint. Explain the topic to a peer in plain language, then reintroduce two precise terms correctly.",
                f"Misconception to retire: {misc[0]}",
                f"Second misconception filter: {misc[1]}",
                "Compare at least two high-quality sources (for example a major society page and a public-health explainer). Note where they agree on definitions and where they emphasize different uncertainties.",
                f"Because this article lives in the {category.replace('-', ' ')} collection, connect outward: disease mechanisms inform prevention; prevention data raise research questions; research methods discipline how we read statistics.",
            ]
        else:
            paras = [
                f"Turn “{heading}” into better care conversations. Sample prompts: What does this mean for my absolute risk over the next 5-10 years? Which evaluation steps fit my age and history? Which choices are preference-sensitive?",
                "If you are a student, convert the article into a one-page concept map: triggers → mechanisms → findings → decision forks → open questions.",
                "If you support a family member, focus on warning symptoms, follow-up timing, and medication purposes at a high level-leaving prescribing and diagnosis to the care team.",
                "Cardily publishes educational clarity for the next generation of cardiovascular learners and the public. Emergency symptoms require emergency services.",
                f"Suggested next read: another Insight sharing keywords among {kw}, then one research-literacy or data-literacy piece so methods stay attached to facts.",
            ]
        sections.append({"heading": heading, "paragraphs": paras})

    sections.append(
        {
            "heading": "Synthesis and responsible next steps",
            "paragraphs": [
                f"“{title}” rewards slow reading. The lasting skill is recognizing precise claims, overextended claims, and personal questions that need a clinician.",
                f"Re-anchor: {angle}. Retrieval cue: {kw}. Number habit: prefer absolute risk and clear denominators whenever statistics appear.",
                mechanisms[0],
                "Continue learning across Cardily Insights, and treat medical decisions as collaborative clinical work-not a DIY project from a webpage.",
            ],
        }
    )

    difficulty = topic.get("difficulty", "intro")
    minutes = 10 if difficulty == "intro" else 12 if difficulty == "intermediate" else 14

    return {
        "slug": topic["slug"],
        "takeaways": takeaways,
        "sections": sections,
        "sources": SOURCES.get(category, SOURCES["diseases-and-conditions"]),
        "reading_minutes": minutes,
        "reviewed": False,
        "generated": True,
        "tier": "enriched-v2",
    }


def main() -> None:
    topics = json.loads((CONTENT / "topics.json").read_text(encoding="utf-8"))
    # keep any premium handcrafted bodies
    existing_path = CONTENT / "article-bodies.json"
    premium: dict[str, dict] = {}
    if existing_path.exists():
        raw = json.loads(existing_path.read_text(encoding="utf-8"))
        items = raw if isinstance(raw, list) else list(raw.values())
        for item in items:
            if item.get("tier") == "premium" or item.get("handcrafted"):
                premium[item["slug"]] = item

    bodies = []
    for topic in topics:
        if topic["slug"] in premium:
            bodies.append(premium[topic["slug"]])
        else:
            bodies.append(enrich_topic(topic))

    existing_path.write_text(json.dumps(bodies, indent=2), encoding="utf-8")
    print(f"Wrote {len(bodies)} bodies ({len(premium)} premium preserved)")


if __name__ == "__main__":
    main()
