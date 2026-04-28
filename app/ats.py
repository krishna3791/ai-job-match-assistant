from __future__ import annotations

import re
from dataclasses import dataclass

from app.matcher import find_skills


SECTION_KEYWORDS = {
    "summary": ["summary", "professional summary", "profile"],
    "skills": ["skills", "technical skills", "core competencies"],
    "experience": ["experience", "professional experience", "work experience"],
    "education": ["education"],
}

ACTION_VERBS = [
    "built",
    "designed",
    "developed",
    "implemented",
    "created",
    "improved",
    "optimized",
    "automated",
    "migrated",
    "managed",
    "led",
    "delivered",
]


@dataclass(frozen=True)
class ATSReport:
    score: int
    strengths: list[str]
    issues: list[str]
    recommendations: list[str]


def has_email(text: str) -> bool:
    return bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))


def has_phone(text: str) -> bool:
    return bool(re.search(r"(\+?\d[\d\s().-]{8,}\d)", text))


def has_metric(text: str) -> bool:
    return bool(re.search(r"\d+%|\$\d+|\d+\s*(years?|hrs?|hours?|tb|gb|million|k)\b", text.lower()))


def detect_sections(text: str) -> set[str]:
    lowered = text.lower()
    found = set()
    for section, keywords in SECTION_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            found.add(section)
    return found


def calculate_ats_report(resume_text: str, job_description_text: str) -> ATSReport:
    score = 0
    strengths = []
    issues = []
    recommendations = []

    sections = detect_sections(resume_text)
    section_score = len(sections) * 10
    score += min(section_score, 40)
    if sections:
        strengths.append(f"Detected resume sections: {', '.join(sorted(sections))}.")
    missing_sections = sorted(set(SECTION_KEYWORDS) - sections)
    if missing_sections:
        issues.append(f"Missing common ATS sections: {', '.join(missing_sections)}.")
        recommendations.append("Add clear section headings such as Summary, Skills, Experience, and Education.")

    contact_score = 0
    if has_email(resume_text):
        contact_score += 10
    else:
        issues.append("Email address was not detected.")
    if has_phone(resume_text):
        contact_score += 10
    else:
        issues.append("Phone number was not detected.")
    score += contact_score

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description_text)
    if job_skills:
        skill_score = round((len(resume_skills & job_skills) / len(job_skills)) * 25)
        score += skill_score
        strengths.append(f"Matched {len(resume_skills & job_skills)} of {len(job_skills)} detected job skills.")
    else:
        recommendations.append("Paste a detailed job description to calculate stronger skill alignment.")

    action_verb_count = sum(1 for verb in ACTION_VERBS if verb in resume_text.lower())
    if action_verb_count >= 4:
        score += 15
        strengths.append("Resume uses several action verbs.")
    else:
        score += action_verb_count * 3
        recommendations.append("Start more bullets with action verbs like built, improved, automated, or optimized.")

    if has_metric(resume_text):
        score += 10
        strengths.append("Resume includes measurable impact or numeric detail.")
    else:
        issues.append("Measurable impact was not detected.")
        recommendations.append("Add metrics such as volume, latency, cost reduction, SLA, or processing scale where truthful.")

    word_count = len(resume_text.split())
    if 350 <= word_count <= 900:
        strengths.append("Resume length looks reasonable for ATS parsing.")
    elif word_count < 350:
        issues.append("Resume text looks short.")
        recommendations.append("Add more project impact, tools, and business outcomes if they are truthful.")
    else:
        issues.append("Resume text may be long.")
        recommendations.append("Trim repeated details and prioritize role-relevant skills.")

    return ATSReport(
        score=min(score, 100),
        strengths=strengths,
        issues=issues,
        recommendations=recommendations,
    )
