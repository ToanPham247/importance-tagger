# importance-tagger

A tiny, **transparent** keyword classifier for short text. Score a message into tiers by matching configurable keyword sets — no ML, no model download, just ordered rules you can read and audit. Great for triaging notifications, tweets, log lines, or tickets into *urgent / watch / noise*.

## Usage

```python
from importance_tagger import Tagger

tagger = Tagger({
    3: ["down", "outage", "urgent", "sev1"],
    2: ["slow", "degraded", "warning"],
    1: ["deploy", "release"],
})

tagger.tier("API is down right now")      # 3
tagger.tag("scheduled release tonight")   # Tag(tier=1, matched=["release"])
tagger.rank(messages)                     # [(text, Tag), ...] highest tier first
```

Higher tier wins when several match. Pass `whole_word=True` to match word boundaries instead of substrings.

## License
MIT — see [LICENSE](LICENSE).
