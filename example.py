"""Run: python example.py"""
from importance_tagger import Tagger

tagger = Tagger({
    3: ["down", "outage", "urgent"],
    2: ["slow", "warning"],
    1: ["deploy", "release"],
})
msgs = ["API is down right now", "response is slow", "scheduled release", "lunch time"]
for text, tag in tagger.rank(msgs):
    print(f"  tier {tag.tier} {tag.matched!s:22} :: {text}")
