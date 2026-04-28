from __future__ import annotations

import math
import re
from collections import Counter

from app.matcher import SKILLS, normalize_text


TOKEN_PATTERN = re.compile(r"[a-z0-9+#./-]+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(normalize_text(text))


def build_embedding(text: str) -> dict[str, float]:
    tokens = tokenize(text)
    counts = Counter(tokens)

    normalized = normalize_text(text)
    for skill in SKILLS:
        if skill in normalized:
            counts[skill] += 3

    return {token: float(count) for token, count in counts.items()}


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0

    shared_tokens = set(left) & set(right)
    dot_product = sum(left[token] * right[token] for token in shared_tokens)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))

    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot_product / (left_norm * right_norm)
