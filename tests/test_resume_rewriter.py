from app.matcher import analyze_match
from app.resume_rewriter import build_rewrite_guidance, estimate_years_experience


def test_estimate_years_experience_detects_years() -> None:
    assert estimate_years_experience("Data Engineer with 5 years of experience.") == 5


def test_rewrite_guidance_contains_guardrails() -> None:
    result = analyze_match("Python SQL", "Python SQL LLM RAG")
    guidance = build_rewrite_guidance("Python SQL", "Python SQL LLM RAG", result)

    assert "Do not invent" in guidance
    assert "Skill gaps" in guidance
    assert "llm" in guidance
