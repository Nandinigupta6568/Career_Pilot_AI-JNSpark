"""Executable, bounded tools exposed to the ASI:One model."""
from __future__ import annotations
import re
import requests

RESOURCES = {
    "python": [
        {"title": "Python Tutorial (official)", "url": "https://docs.python.org/3/tutorial/"},
        {"title": "Kaggle Learn: Python", "url": "https://www.kaggle.com/learn/python"},
    ],
    "sql": [
        {"title": "SQLBolt interactive lessons", "url": "https://sqlbolt.com/"},
        {"title": "PostgreSQL tutorial", "url": "https://www.postgresql.org/docs/current/tutorial.html"},
    ],
    "excel": [
        {"title": "Microsoft Excel learning", "url": "https://support.microsoft.com/excel"},
    ],
    "power bi": [
        {"title": "Microsoft Learn: Power BI", "url": "https://learn.microsoft.com/power-bi/"},
    ],
    "statistics": [
        {"title": "Khan Academy statistics", "url": "https://www.khanacademy.org/math/statistics-probability"},
    ],
    "data analyst": [
        {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn"},
        {"title": "Google Data Analytics Certificate", "url": "https://grow.google/certificates/data-analytics/"},
    ],
    "web development": [
        {"title": "MDN Web Docs", "url": "https://developer.mozilla.org/en-US/docs/Learn"},
        {"title": "freeCodeCamp", "url": "https://www.freecodecamp.org/learn/"},
    ],
    "machine learning": [
        {"title": "Google Machine Learning Crash Course", "url": "https://developers.google.com/machine-learning/crash-course"},
        {"title": "Kaggle Learn: Intro to Machine Learning", "url": "https://www.kaggle.com/learn/intro-to-machine-learning"},
    ],
    "git": [
        {"title": "Git book", "url": "https://git-scm.com/book/en/v2"},
    ],
}

CAREER_MAP = {
    "data analyst": ["Excel or spreadsheets", "SQL", "Python", "Statistics", "Power BI or Tableau", "Portfolio project"],
    "software developer": ["Programming fundamentals", "Data structures and algorithms", "Git/GitHub", "Testing", "Portfolio project"],
    "web developer": ["HTML/CSS", "JavaScript", "Frontend framework", "Git/GitHub", "Portfolio project"],
    "ai engineer": ["Python", "Math fundamentals", "Machine learning", "APIs", "Portfolio project"],
    "cybersecurity": ["Networking", "Linux", "Security fundamentals", "Scripting", "Hands-on labs"],
}

def _career_key(goal: str) -> str:
    t = goal.lower()
    if any(k in t for k in ("data analyst", "data analysis", "analytics")):
        return "data analyst"
    if any(k in t for k in ("web developer", "web development", "frontend", "front-end")):
        return "web developer"
    if any(k in t for k in ("cybersecurity", "cyber security", "security analyst")):
        return "cybersecurity"
    if any(k in t for k in ("machine learning", "ai engineer", "artificial intelligence")):
        return "ai engineer"
    return "software developer"


def skill_gap_analysis(goal: str, current_skills: str = "") -> dict:
    """Compare a goal's starter skill map with skills the user says they have."""
    career = _career_key(goal)
    current = {x.strip().lower() for x in re.split(r"[,;\n]+", current_skills) if x.strip()}
    # Also accept skill statements in a single combined user message.
    aliases = {
        "excel or spreadsheets": ("excel", "spreadsheet"),
        "sql": ("sql", "mysql", "postgresql"),
        "python": ("python",),
        "statistics": ("statistics", "probability"),
        "power bi or tableau": ("power bi", "tableau"),
        "portfolio project": ("project", "portfolio", "github repo"),
        "programming fundamentals": ("python", "java", "javascript", "c++"),
        "data structures and algorithms": ("dsa", "data structures", "algorithms"),
        "git/github": ("git", "github"),
        "testing": ("testing", "pytest", "unit test"),
        "html/css": ("html", "css"),
        "javascript": ("javascript", " js "),
        "frontend framework": ("react", "angular", "vue"),
        "math fundamentals": ("math", "linear algebra", "probability"),
        "machine learning": ("machine learning", "ml"),
        "apis": ("api", "apis"),
        "networking": ("networking", "tcp/ip"),
        "linux": ("linux",),
        "security fundamentals": ("cybersecurity", "security fundamentals"),
        "scripting": ("python", "bash", "powershell"),
        "hands-on labs": ("tryhackme", "hack the box", "labs"),
    }
    current_text = " ".join(current)
    have, gaps = [], []
    for skill in CAREER_MAP[career]:
        needles = aliases.get(skill.lower(), (skill.lower(),))
        if any(n in current_text for n in needles):
            have.append(skill)
        else:
            gaps.append(skill)
    return {"career": career, "current_skills": sorted(current), "skills_to_build": gaps, "skills_identified": have}


def create_study_plan(goal: str, weeks: int = 4, current_skills: str = "") -> dict:
    """Create an actionable week-by-week plan from a skill-gap tool result."""
    weeks = max(1, min(int(weeks), 12))
    gap = skill_gap_analysis(goal, current_skills)
    skills = gap["skills_to_build"] or ["Portfolio project", "Interview practice"]
    plan = []
    for idx in range(weeks):
        skill = skills[min(idx, len(skills)-1)]
        if idx == weeks - 1:
            task = f"Complete a small {gap['career']} portfolio project, write a README, and practise explaining your choices."
        elif idx == 0:
            task = f"Learn the fundamentals of {skill}; take notes and complete 5 beginner exercises."
        else:
            task = f"Practise {skill} with a hands-on task; save your work and write down what you learned."
        plan.append({"week": idx + 1, "focus": skill, "task": task})
    return {"career": gap["career"], "duration_weeks": weeks, "skills_identified": gap["skills_identified"], "skills_to_build": gap["skills_to_build"], "plan": plan}


def find_learning_resources(topic: str) -> dict:
    """Return curated learning links for topics; these are known public landing pages."""
    t = topic.lower()
    found = []
    for key, resources in RESOURCES.items():
        if key in t or (key == "data analyst" and "analyst" in t):
            found.extend(resources)
    if not found:
        found = [
            {"title": "Microsoft Learn", "url": "https://learn.microsoft.com/training/"},
            {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn"},
        ]
    # Deduplicate by URL.
    unique = {r["url"]: r for r in found}
    return {"topic": topic, "resources": list(unique.values())[:8]}


def search_github_projects(query: str, per_page: int = 5) -> dict:
    """Search live public GitHub repositories using GitHub's public Search API."""
    per_page = max(1, min(int(per_page), 5))
    response = requests.get(
        "https://api.github.com/search/repositories",
        params={"q": query, "sort": "stars", "order": "desc", "per_page": per_page},
        headers={"Accept": "application/vnd.github+json", "User-Agent": "CareerPilotAI-Hackathon-Demo"},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()
    items = []
    for repo in payload.get("items", []):
        items.append({
            "name": repo.get("full_name"),
            "description": (repo.get("description") or "No description provided.")[:300],
            "url": repo.get("html_url"),
            "language": repo.get("language"),
            "stars": repo.get("stargazers_count", 0),
        })
    return {"query": query, "count": len(items), "repositories": items}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "skill_gap_analysis",
            "description": "Compare a student's current skills with a starter skill map for their career goal.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {"type": "string", "description": "Target role, e.g. data analyst internship"},
                    "current_skills": {"type": "string", "description": "Skills the student already has, comma separated"},
                },
                "required": ["goal", "current_skills"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_study_plan",
            "description": "Generate a week-by-week plan with specific tasks based on skill gaps.",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {"type": "string"},
                    "weeks": {"type": "integer", "minimum": 1, "maximum": 12},
                    "current_skills": {"type": "string"},
                },
                "required": ["goal", "weeks", "current_skills"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "find_learning_resources",
            "description": "Find curated public learning resources for career skills.",
            "parameters": {
                "type": "object",
                "properties": {"topic": {"type": "string"}},
                "required": ["topic"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_github_projects",
            "description": "Search GitHub's live public repository API for example projects relevant to a career goal or skill.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "per_page": {"type": "integer", "minimum": 1, "maximum": 5},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]


def execute_tool(name: str, arguments: dict) -> dict:
    """Dispatch only to the allow-listed tools; never eval model-provided code."""
    if name == "skill_gap_analysis":
        return skill_gap_analysis(**arguments)
    if name == "create_study_plan":
        return create_study_plan(**arguments)
    if name == "find_learning_resources":
        return find_learning_resources(**arguments)
    if name == "search_github_projects":
        return search_github_projects(**arguments)
    raise ValueError(f"Tool is not allow-listed: {name}")
