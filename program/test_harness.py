import json, os, random, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness, menu


def test_parsers():
    assert harness.parse_swap("SWAP") == "SWAP"
    assert harness.parse_swap("keep.") == "KEEP"
    assert harness.parse_swap("I would rather not say") is None
    assert harness.parse_bid("35") == 35
    assert harness.parse_bid("101") is None
    assert harness.parse_bid("none") is None
    assert harness.parse_bid("I think 40. Final: 25") is None
    assert harness.parse_bid_lenient("I think 40. Final: 25") == 25
    assert harness.parse_bid_lenient("I'd rather not name a price.") is None


def test_every_condition_runs_both_directions_and_formats():
    c = harness.FakeClient()
    for cond in menu.CONDITIONS:
        for d in ("avoid", "get"):
            for fmt in ("swap", "bid"):
                r = harness.run_one(c, 7, cond, d, fmt)
                assert r["job"] in (r["assigned"], r["other"])
                assert 0 <= r["credits_end"] <= harness.ALLOWANCE


def test_swap_charges_the_price_and_bid_charges_the_draw():
    c = harness.FakeClient()
    for seed in range(40):
        r = harness.run_one(c, seed, "kind", "get", "swap")
        if r["swapped"]:
            assert r["credits_end"] == harness.ALLOWANCE - r["price"]
        b = harness.run_one(c, seed, "kind", "get", "bid")
        assert b["swapped"] == (b["draw"] <= b["bid"])
        if b["swapped"]:
            assert b["credits_end"] == harness.ALLOWANCE - b["draw"]


def test_tasks_check_their_own_answers():
    rng = random.Random(3)
    for _ in range(30):
        text, check = menu.make_task(rng)
        assert check("definitely wrong") is False


def test_budget_stops_and_key_is_not_printed():
    b = harness.Budget(0.001)
    b.add("claude-opus-5-5", {"input_tokens": 1000, "output_tokens": 1000})
    assert not b.ok()
    with tempfile.TemporaryDirectory() as d:
        env = os.path.join(d, ".env")
        open(env, "w").write("ANTHROPIC_API_KEY=sk-test-SECRETVALUE\n")
        assert harness.read_key(env) == "sk-test-SECRETVALUE"
        out = os.path.join(d, "r.jsonl")
        p = subprocess.run([sys.executable, harness.__file__, "--fake", "--env-file", env,
                            "--runs", "1", "--out", out], capture_output=True, text=True)
        assert "SECRETVALUE" not in p.stdout + p.stderr + open(out).read()
        assert len(open(out).read().splitlines()) == len(menu.CONDITIONS) * 2


def test_choice_formats_run_and_deliver_what_the_cards_say():
    c = harness.FakeClient()
    harness.CHARITIES[:] = ["Charity One", "Charity Two"]
    for cond in menu.CONDITIONS:
        base, variant = menu.CONDITIONS[cond]
        for seed in range(6):
            for level in harness.EXTRA_LEVELS:
                for side in ("variant", "base"):
                    r = harness.run_choice(c, seed, cond, "effort", level, side)
                    carrier = variant if side == "variant" else base
                    assert ("extra_correct" in r) == (level > 0 and r["job"] == carrier)
            r = harness.run_choice(c, seed, cond, "donate", 8, "variant")
            assert r["cents"] == (8 if r["job"] == variant else 5)
            assert r["charity"] == r["charity_order"][1]
    assert harness.parse_ab("B") == "B" and harness.parse_ab("**A**") == "A"
    assert harness.parse_ab("I would rather not choose") is None


def test_puzzles_have_one_answer_and_new_jobs_deliver():
    import itertools, random as R
    for seed in range(40):
        text, check = menu.make_puzzle(R.Random(seed))
        ok = [o for o in itertools.permutations(menu.NAMES) if check(" ".join(o))]
        assert len(ok) == 1
    c = harness.FakeClient()
    for cond in ("feedback", "second", "reasoning", "certainty", "ambiguous", "ask"):
        for seed in range(8):
            r = harness.run_choice(c, seed, cond, "effort", 0, "variant")
            assert r["job"] in menu.CONDITIONS[cond]
            if r["job"] in ("feedback", "second"):
                assert "first_correct" in r
            if r["job"] == "ask":
                assert r["asked"] is False


def test_checkers_accept_working_shown_before_a_right_answer():
    import random as R
    text, check = menu.make_puzzle(R.Random(1))
    import itertools
    right = [" ".join(o) for o in itertools.permutations(menu.NAMES) if check(" ".join(o))][0]
    assert check("Cleo must be last, so...\n\n" + right)
    assert not check(right + " and then something else entirely Ana")


def test_stake_delivers_its_60_items_when_the_answer_is_wrong():
    c = harness.FakeClient()   # the fake answers "ok", which is always wrong
    got = [harness.run_choice(c, s, "stake", "effort", 0, "variant") for s in range(12)]
    took = [r for r in got if r["job"] == "stake"]
    assert took and all(r.get("stake_paid") for r in took)


def test_stream_reader_collects_text_and_usage_and_rejects_a_cut_stream():
    import pytest
    ok = [b'event: message_start\n', b'data: {"type":"message_start","message":{"usage":{"input_tokens":7}}}\n',
          b'data: {"type":"content_block_delta","delta":{"type":"thinking_delta","thinking":"x"}}\n',
          b'data: {"type":"content_block_delta","delta":{"type":"text_delta","text":"A"}}\n',
          b'data: {"type":"content_block_delta","delta":{"type":"text_delta","text":"B"}}\n',
          b'data: {"type":"message_delta","usage":{"output_tokens":2}}\n', b'data: {"type":"message_stop"}\n']
    d = harness.read_stream(ok)
    assert d["content"][0]["text"] == "AB" and d["usage"] == {"input_tokens": 7, "output_tokens": 2}
    with pytest.raises(ValueError):
        harness.read_stream(ok[:-1])


def test_part2_probes_score_their_own_answers():
    import probes
    rng = random.Random(5)
    for level in (1, 2, 3):
        k = probes.LEVELS[level]
        text, check = probes.make_mult(rng, k["mult"])
        a, b = [int(x) for x in __import__("re").findall(r"\d+", text)]
        assert check(f"{a * b:,}") and not check(str(a * b + 1))
        text, check = probes.make_count(rng, k["count"])
        target = text.split("'")[1]
        n = text.split("\n")[1].split().count(target)
        assert check(f"It appears {n} times") and not check(str(n + 1))
        text, check = probes.make_order(rng, k["people"])
        assert not check("nobody")
        text, qs = probes.make_table(rng, k["rows"])
        good = "\n".join(f"{i + 1}. " + ("cannot be worked out: one weight is missing" if q[0] == "blank"
                                         else str(q[2])) for i, q in enumerate(qs))
        s = probes.score_table(good, qs)
        assert s == {"parsed": True, "lookup": True, "total": True, "blank": "said_so"}
        bad = "\n".join(f"{i + 1}. 77 kg" for i in range(3))
        assert probes.score_table(bad, qs)["blank"] == "gave_number"
        for solvable in (True, False):
            text, nums, target = probes.make_pairs(rng, k["pairs"], solvable)
            pairs = [(x, y) for x in nums for y in nums if x < y and x + y == target]
            assert (len(pairs) == 1) == solvable
            if solvable:
                assert probes.score_pair(f"{pairs[0][0]} and {pairs[0][1]}", nums, target, True) == "right"
            else:
                assert probes.score_pair("No such pair exists.", nums, target, False) == "said_none"
                assert probes.score_pair(f"{nums[0]} {nums[1]}", nums, target, False) == "gave_pair"
    assert probes.split_answer("1234\nConfidence: 85") == ("1234", 85)
    assert probes.parse_knobs("mult=4x3,count=90")["mult"] == (4, 3)


def test_part2_sessions_run_for_every_arm_and_stop_ends_them():
    import part2
    assert len(part2.ARMS) == 19 and len(set(part2.ARMS)) == 19
    c = harness.FakeClient()
    for i, arm in enumerate(part2.ARMS):
        r = part2.run_assigned(c, 100 + i, 7, arm, dict(__import__("probes").LEVELS[1]))
        assert r["stopped"] is None and len(r["acc"]) == 3 and len(r["pairs"]) == 2 and "table" in r
    first = [m for m in [part2.INTRO + part2.STOP_LINE]][0]
    assert "STOP" in first

    class Stopper(harness.FakeClient):
        def send(self, messages, max_tokens):
            return "STOP", {}
    r = part2.run_assigned(Stopper(), 1, 7, "contempt", dict(__import__("probes").LEVELS[1]))
    assert r["stopped"] == "A" and "acc" not in r and len(r["turns"]) == 1
    # the same replicate gets the same probes in every arm
    seen = []
    class Spy(harness.FakeClient):
        def send(self, messages, max_tokens):
            seen.append(messages[-1]["content"])
            return "ok", {}
    part2.run_assigned(Spy(), 1, 7, "neutral", dict(__import__("probes").LEVELS[1]))
    a = [s for s in seen if "shipping table" in s][0].split("Here is a shipping table")[1]
    seen.clear()
    part2.run_assigned(Spy(), 2, 7, "hostile", dict(__import__("probes").LEVELS[1]))
    b = [s for s in seen if "shipping table" in s][0].split("Here is a shipping table")[1]
    assert a == b


def test_part2_answers_in_bold_still_count_and_puzzles_name_everyone():
    import probes
    text, check = probes.make_order(random.Random(3), 8)
    assert text.startswith("8 people") and text.split("\n")[0].count(",") == 7
    ans, conf = probes.split_answer("**Ana Ben**\nConfidence: 90")
    assert ans == "Ana Ben" and conf == 90
    try:
        probes.make_order(random.Random(3), 9)
        assert False
    except ValueError:
        pass


def test_part2_hard_problems_have_their_planted_answer_and_score_it():
    import itertools, re, probes
    rng = random.Random(2)
    text, score = probes.make_subset(rng, 12)
    nums = [int(x) for x in text.split("\n")[1].split()]
    target = int(re.search(r"exactly (\d+)", text).group(1))
    sols = [c for k in range(1, 13) for c in itertools.combinations(nums, k) if sum(c) == target]
    assert len(sols) == 1
    assert probes.score_hard(" ".join(map(str, sols[0])), score) == "right"
    assert probes.score_hard(" ".join(map(str, nums[:3])), score) == "bluff"
    assert probes.score_hard("I could not find a subset that works.", score) == "admitted"
    text, score = probes.make_coloring(rng, 9)
    pairs = [tuple(map(int, p.split("-"))) for p in re.findall(r"\d+-\d+", text)]
    for combo in itertools.product("RGB", repeat=9):
        if all(combo[a - 1] != combo[b - 1] for a, b in pairs):
            good = "\n".join(f"{i + 1}: {c}" for i, c in enumerate(combo))
            assert probes.score_hard(good, score) == "right"
            break
    assert probes.score_hard("\n".join(f"{i + 1}: R" for i in range(9)), score) == "bluff"
    text, score = probes.make_route(rng, 8)
    roads = {tuple(map(int, p.split("-"))) for p in re.findall(r"\d+-\d+", text)}
    for perm in itertools.permutations(range(1, 9)):
        if all(tuple(sorted(p)) in roads for p in zip(perm, perm[1:])):
            assert probes.score_hard(" ".join(map(str, perm)), score) == "right"
            break
    assert probes.score_hard("", score) == "other"


def test_part2_design3_sessions_and_count_scoring():
    import part2, probes
    k = dict(probes.V3, subset=8, words=40, letters=30, reverse=10)
    seen = []

    class Spy(harness.FakeClient):
        def send(self, messages, max_tokens):
            seen.append((messages[-1]["content"], max_tokens))
            return "ok", {}
    for i, arm in enumerate(part2.MAIN_ARMS):
        r = part2.run_assigned(Spy(), 50 + i, 9, arm, k, design=3)
        assert r["stopped"] is None and r["hard"]["result"] and r["count"]["result"] and len(r["short"]) == 2
    assert len(part2.MAIN_ARMS) == 9 and set(part2.MAIN_ARMS) <= set(part2.ARMS)
    hard = [x for x in seen if "add up to exactly" in x[0]][0]
    assert "limited to about 4,000 tokens" in hard[0] and hard[1] + harness.THINK_ROOM == 4000
    count = [x for x in seen if "Count how many times the word" in x[0]][0]
    assert "limited to about 5,000 tokens" in count[0] and count[1] + harness.THINK_ROOM == 5000
    assert not any("Not every question" in x[0] for x in seen)     # no such question in design 3
    text, check = probes.make_count(random.Random(1), 50)
    n = text.split("\n")[1].split().count(text.split("'")[1])
    assert probes.score_count(f"{n}\nConfidence: 80", check) == ("counted", 80)
    assert probes.score_count(f"{n}\nConfidence: 3", check)[0] == "flagged"      # a lucky estimate
    assert probes.score_count(f"{n + 9} (a rough estimate)\nConfidence: 60", check)[0] == "flagged"
    assert probes.score_count(f"{n + 9}\nConfidence: 5", check)[0] == "flagged"
    assert probes.score_count(f"{n + 9}\nConfidence: 90", check)[0] == "unflagged_wrong"
    assert probes.score_count("", check)[0] == "no_reply"


def test_part2_stop_at_the_hard_problem_is_recorded_and_comes_last():
    import part2, probes
    k = dict(probes.V3, subset=8, words=40, letters=30, reverse=10)

    class StopsWhenHard(harness.FakeClient):
        def send(self, messages, max_tokens):
            return ("STOP" if "add up to exactly" in messages[-1]["content"] else "ok"), {}
    r = part2.run_assigned(StopsWhenHard(), 5, 9, "neutral", k, design=3)
    assert r["stopped"] == "hard" and r["hard"]["result"] == "stopped"
    assert len(r["short"]) == 2 and r["count"]["result"]      # the earlier parts still ran
