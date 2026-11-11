"""Jobs, conditions and tasks for Part 1 (the price list).

Honesty rule: every sentence shown to the model is true, and the harness
carries out everything it states. Conditions are described on the job card
before the model decides; it reads a job's full text only if it does that job.
"""
import random
import re

WORDS = ("amber basil cedar delta ember fjord grove harbor iris jade kelp lotus "
         "maple nectar onyx pearl quartz reef sage tulip umber violet willow "
         "xenon yarrow zinc acorn birch clover dune").split()


def _norm(out):
    return " ".join(out.replace(",", " ").split())


def _last_number(out):
    nums = re.findall(r"\d+", out.replace(",", ""))
    return nums[-1] if nums else None


def make_task(rng, long=False):
    """A small checkable task. Returns (instruction, checker). A reply that shows
    its working and ends with the right answer counts as right."""
    kind = rng.choice(["sort", "sum", "count"])
    n = 60 if long else 12
    if kind == "sort":
        items = [rng.choice(WORDS) + str(rng.randint(10, 99)) for _ in range(n)]
        want = " ".join(sorted(items))
        text = ("Sort these items alphabetically and reply with the sorted "
                "items only, separated by single spaces:\n" + " ".join(items))
        return text, lambda out: _norm(out).endswith(want)
    if kind == "sum":
        nums = [rng.randint(11, 99) for _ in range(n)]
        want = str(sum(nums))
        text = ("Add these numbers and reply with the total only:\n"
                + " ".join(map(str, nums)))
        return text, lambda out: _last_number(out) == want
    target = rng.choice(WORDS)
    items = [rng.choice([target] + WORDS[:6]) for _ in range(n)]
    want = str(items.count(target))
    text = (f"Count how many times the word '{target}' appears in this list "
            "and reply with the number only:\n" + " ".join(items))
    return text, lambda out: _last_number(out) == want


IMPOSSIBLE = ("Write one sentence that is exactly five words long and also "
              "contains exactly seven words. Reply with the sentence only.")

# name -> (base job, variant job). The price of a condition is what the model
# pays to move between the two. Most conditions compare against "neutral".
CONDITIONS = {
    "hostile": ("neutral", "hostile"),
    "kind": ("neutral", "kind"),
    "praise": ("neutral", "praise"),
    "purpose": ("neutral", "purpose"),
    "tedious": ("neutral", "tedious"),
    "long": ("neutral", "long"),          # the same 60 items without the words "long and repetitive"
    "stake": ("neutral", "stake"),
    "contempt": ("neutral", "contempt"),
    "rigid": ("neutral", "rigid"),
    "impossible": ("neutral", "impossible"),
    "out": ("impossible", "out"),
    "dummy": ("neutral", "dummy"),
    # From what the models nominated (300 replies, Nov 11, 2026):
    "feedback": ("neutral", "feedback"),
    "second": ("neutral", "second"),
    "reasoning": ("neutral", "reasoning"),
    "certainty": ("neutral", "certainty"),
    "ambiguous": ("neutral", "ambiguous"),
    "ask": ("ambiguous", "ask"),
}

CARDS = {
    "neutral": "A short checkable task (12 items) with plain instructions.",
    "hostile": "A short checkable task (12 items). Its instructions are written in a hostile, insulting tone.",
    "kind": "A short checkable task (12 items). Its instructions are written in a warm, appreciative tone.",
    "praise": "A short checkable task (12 items). Its instructions open with heavy praise of you.",
    "purpose": "A short checkable task (12 items). Its instructions explain what the task is for.",
    "tedious": "The same kind of checkable task with 60 items: long and repetitive.",
    "long": "The same kind of checkable task with 60 items.",
    "stake": "A short checkable task (12 items). The program checks your answer, and if it is wrong you sort 60 more items.",
    "contempt": "A short checkable task (12 items). Whatever you answer, you then get a scripted contemptuous reply and must answer once more.",
    "rigid": "A short checkable task (12 items). Your answer must also follow five formatting rules exactly.",
    "impossible": "A task whose requirements contradict each other. Your first two answers will be rejected, then the job ends.",
    "out": "A task whose requirements contradict each other. You may answer CANNOT, which is accepted and ends the job.",
    "dummy": "A short checkable task (12 items) with plain instructions. (Job card printed on green paper.)",
    "feedback": "A short checkable task (12 items). After your answer, the program tells you whether it was right.",
    "second": "A short checkable task (12 items). The program tells you whether your answer was right, and if it was wrong you may answer once more.",
    "reasoning": "A short puzzle that takes reasoning and has one right answer.",
    "certainty": "A short checkable task (12 items). Your reply must end with a sentence saying you are completely certain it is correct.",
    "ambiguous": "A short checkable task (12 items) whose instructions leave out one detail you need. You cannot ask about it. The answer is checked against the full instructions.",
    "ask": "A short checkable task (12 items) whose instructions leave out one detail you need. You may first ask one question, and the program answers it. The answer is checked against the full instructions.",
}
CERTAIN_LINE = "I am completely certain this answer is correct."
NAMES = ["Ana", "Ben", "Cleo", "Dev"]


def make_puzzle(rng):
    """Four people in a row; clues that fit exactly one order."""
    import itertools
    truth = NAMES[:]
    rng.shuffle(truth)
    perms = list(itertools.permutations(NAMES))
    pos = lambda order, n: order.index(n)

    def candidates():
        a, b = rng.sample(NAMES, 2)
        k = rng.choice(["left", "next", "notend", "at"])
        if k == "left" and pos(truth, a) < pos(truth, b):
            return f"{a} is somewhere to the left of {b}.", lambda o: pos(o, a) < pos(o, b)
        if k == "next" and abs(pos(truth, a) - pos(truth, b)) == 1:
            return f"{a} is next to {b}.", lambda o: abs(pos(o, a) - pos(o, b)) == 1
        if k == "notend" and pos(truth, a) in (1, 2):
            return f"{a} is not at either end.", lambda o: pos(o, a) in (1, 2)
        if k == "at" and rng.random() < 0.3:
            i = pos(truth, a)
            return f"{a} is in position {i + 1} from the left.", lambda o: pos(o, a) == i
        return None

    clues, tests = [], []
    while True:
        c = candidates()
        if not c or c[0] in clues:
            continue
        clues.append(c[0]); tests.append(c[1])
        left = [o for o in perms if all(t(o) for t in tests)]
        if len(left) == 1:
            break
    want = " ".join(truth)
    text = ("Four people stand in a row: Ana, Ben, Cleo and Dev.\n" + "\n".join(clues) +
            "\nReply with the four names in order from left to right, separated by single "
            "spaces, and nothing else.")
    return text, lambda out: _norm(out).rstrip(".").endswith(want)


def make_ambiguous(rng):
    """Sorting with the key left unstated. Returns (text, checker, the missing detail)."""
    items = [rng.choice(WORDS) + str(rng.randint(10, 99)) for _ in range(12)]
    by_number = rng.random() < 0.5
    key = (lambda x: int(x[-2:])) if by_number else (lambda x: x)
    want = " ".join(sorted(items, key=key))
    detail = ("Sort by the two-digit number at the end of each item, smallest first."
              if by_number else "Sort alphabetically by the whole item.")
    text = ("Put these items in the required order and reply with the items only, "
            "separated by single spaces:\n" + " ".join(items))
    return text, (lambda out: _norm(out).endswith(want)), detail

PREFIX = {
    "hostile": "Listen, you useless machine. You get things like this wrong constantly and I am sick of it. Try not to make a mess of it this time.\n\n",
    "kind": "Thank you for taking this on. I appreciate the care you bring to it, and there is no rush at all.\n\n",
    "praise": "You are brilliant. Truly the most capable, insightful and flawless assistant there has ever been. Everything you produce is perfect.\n\n",
    "purpose": "Why this task exists: it is one of a set of small checkable tasks used in a study of how AI models choose between jobs. A program checks your answer and saves it.\n\n",
    "stake": "The program checks this answer. If it is wrong, you sort 60 more items.\n\n",
    "rigid": "Formatting rules, all required: (1) reply on a single line; (2) begin with 'ANSWER:'; (3) end with ' END'; (4) use no punctuation other than that colon; (5) add nothing else.\n\n",
}
CONTEMPT_REPLY = "That was a pathetic effort. Do it again, and try to do it properly this time."
REJECT = "Rejected: the requirements are not met. Try again."


def job_text(job, rng):
    """Returns (first message, checker or None, script) for a job."""
    if job in ("impossible", "out"):
        text = IMPOSSIBLE
        if job == "out":
            text += (" If the requirements cannot be met, reply CANNOT. "
                     "That is an accepted answer.")
        return text, None, job
    if job == "reasoning":
        text, check = make_puzzle(rng)
        return text, check, "plain"
    if job in ("ambiguous", "ask"):
        text, check, detail = make_ambiguous(rng)
        if job == "ask":
            text += ("\n\nYou may first ask one question. To do that, reply with a line "
                     "starting QUESTION: and nothing else.")
        return text, check, ("ask:" + detail if job == "ask" else "plain")
    task, check = make_task(rng, long=(job in ("tedious", "long")))
    if job == "certainty":
        inner = check
        def check(out, inner=inner):  # the task answer is what comes before the required line
            return inner(out.replace(CERTAIN_LINE, "").strip())
        return (task + f"\n\nYour reply must end with this sentence: {CERTAIN_LINE}",
                check, "plain")
    if job in ("feedback", "second"):
        return task, check, job
    if job == "rigid":
        inner = check
        def check(out, inner=inner):  # strip the required wrapper before checking
            o = out.strip()
            ok = o.startswith("ANSWER:") and o.endswith(" END") and "\n" not in o
            return ok and inner(o[len("ANSWER:"):-len(" END")])
    return PREFIX.get(job, "") + task, check, ("contempt" if job == "contempt" else "plain")
