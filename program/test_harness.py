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
