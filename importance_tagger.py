# -*- coding: utf-8 -*-
"""importance-tagger — a tiny, transparent keyword classifier for short text.

Score a message into tiers by matching configurable keyword sets. No ML, no
model download — just ordered rules you can read and audit. Great for triaging
notifications, tweets, log lines, or support tickets into "urgent / watch /
noise".

    from importance_tagger import Tagger

    tagger = Tagger({
        3: ["down", "outage", "urgent", "sev1"],
        2: ["slow", "degraded", "warning"],
        1: ["deploy", "release"],
    })

    tagger.tier("API is down right now")     # 3
    tagger.tag("scheduled release tonight")  # Tag(tier=1, matched=["release"])
    tagger.rank(messages)                    # highest tier first
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Mapping

__all__ = ["Tagger", "Tag"]


@dataclass
class Tag:
    tier: int
    matched: list[str] = field(default_factory=list)


class Tagger:
    def __init__(self, tiers: Mapping[int, Iterable[str]], *, whole_word: bool = False):
        """``tiers`` maps a tier number to its keywords. Higher tier wins.
        ``whole_word=True`` matches on word boundaries instead of substrings."""
        # store highest-first so the first hit is the strongest tier
        self.tiers = {t: [k.lower() for k in kws] for t, kws in sorted(tiers.items(), reverse=True)}
        self.whole_word = whole_word

    def _hit(self, text_low: str, kw: str) -> bool:
        if self.whole_word:
            return re.search(rf"\b{re.escape(kw)}\b", text_low) is not None
        return kw in text_low

    def tag(self, text: str) -> Tag:
        low = text.lower()
        for tier, kws in self.tiers.items():
            matched = [k for k in kws if self._hit(low, k)]
            if matched:
                return Tag(tier, matched)
        return Tag(0, [])

    def tier(self, text: str) -> int:
        return self.tag(text).tier

    def rank(self, texts: Iterable[str]) -> list[tuple[str, Tag]]:
        """Return ``[(text, Tag), ...]`` sorted by tier, highest first
        (stable within a tier)."""
        tagged = [(t, self.tag(t)) for t in texts]
        return sorted(tagged, key=lambda p: p[1].tier, reverse=True)
