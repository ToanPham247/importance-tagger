from importance_tagger import Tagger

T = Tagger({3: ["down", "urgent"], 2: ["slow", "warning"], 1: ["deploy"]})

def test_tier():
    assert T.tier("service is down") == 3
    assert T.tier("a bit slow") == 2
    assert T.tier("nothing here") == 0

def test_highest_tier_wins():
    assert T.tier("slow and down") == 3   # 3 beats 2

def test_tag_matched():
    tag = T.tag("urgent: down")
    assert tag.tier == 3 and set(tag.matched) == {"urgent", "down"}

def test_rank_order():
    ranked = T.rank(["deploy done", "it is down", "kinda slow"])
    assert [t.tier for _, t in ranked] == [3, 2, 1]

def test_whole_word():
    t = Tagger({1: ["cat"]}, whole_word=True)
    assert t.tier("a cat sat") == 1 and t.tier("category") == 0
