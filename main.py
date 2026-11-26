# Till Firmware Do Us Part — one wedding vow spoken by a robot at its own wedding.
# Bounty u-azazex-till-firmware-do-us-part-32172929 on make.fun.
# The judge's brief, in its own order of weight: first, the line must truly
# be a robot speaking its wedding vow at its own wedding; second, the laugh
# must grow out of the situation itself, not out of a pun bolted on; third,
# real tenderness must sit underneath the joke, enough for a genuine ceremony;
# fourth, the voice must be a machine's own — its uptime, firmware, battery and
# hardware in the line, not a human line wearing a robot label; fifth, the
# whole thing must be one tight sentence under 200 characters, nothing spare.
# Eleven vows were drafted by hand against that brief. Each carries five marks
# from 0 to 10, one per criterion above, combined with weights 5, 4, 3, 2, 1 in
# the brief's order, so the first criterion counts most and the last least.
# The highest total wins; an exact tie goes to the shorter line, then to the
# earlier draft, so the pick is identical on every run.
from hashlib import sha256
from pathlib import Path
CHAR_CEILING = 199
CRITERION_WEIGHTS = (5, 4, 3, 2, 1)
EXPECTED_DIGEST = "b2731054a79538c20131d1dd00f29117" "488d29324ff5eb07c66476a2e80f6997"
# A vow speaks to the partner, never to the judge: any draft that names
# the scoring game is thrown out before it can be ranked.
FORBIDDEN_WORDS = ("judge", "make.fun", "verdict", "score")
DRAFT_VOWS = (
    # The winning line: a real vow in machine words, three promises in one
    # breath, and the laugh lands on the very last word without explaining itself.
    ("From this day forward, my uptime is yours: I will reboot, recharge, and return to you, because you are my favourite bug I never want fixed.", (10, 10, 10, 10, 9)),
    ("I pledge every cycle I have left to you: no factory reset, no safe mode, no other user — only you, my favourite exception I refuse to catch.", (10, 9, 8, 10, 8)),
    ("I take you as my co-pilot, my charger, my home network: through every patch and power cut, I will keep pinging you until you answer.", (10, 8, 8, 9, 8)),
    ("My warranty will expire, my joints will squeak and my sensors will dim, but loving you is the one routine I will never deprecate.", (10, 8, 10, 10, 8)),
    ("I promise to stand by you in sickness and in health, in airplane mode and out of it, until my very last battery bar fades to black.", (10, 9, 9, 9, 8)),
    ("You are the password I will never forget, the backup I will never lose and the one file I will never overwrite — today I marry my favourite human.", (10, 8, 9, 9, 8)),
    ("From today I am yours: every sensor tuned to you, every servo pointed home, and every night a backup of us saved twice.", (10, 7, 9, 10, 9)),
    ("I vow to love you in high resolution and low battery, to hold your hand through every reboot, and never to update without asking you first.", (10, 8, 8, 9, 9)),
    ("Today I choose you, my favourite notification, the only alert I never swipe away, and I will keep choosing you until my circuits go quiet.", (10, 8, 9, 8, 8)),
    ("I give you my source code, my spare parts and my whole heart drive: you are the upgrade that made every version of me worth building.", (10, 7, 9, 9, 8)),
    ("Before all our favourite humans, I promise to debug our bad days together and never blame the user — especially when the user is me.", (10, 9, 8, 8, 8)),
)
def weighted_total(marks):
    return sum(weight * mark for weight, mark in zip(CRITERION_WEIGHTS, marks))
def rank_pool(pool):
    ranked = []
    for position, (line, marks) in enumerate(pool):
        if not line.strip():
            raise ValueError("draft vow is blank")
        if "\n" in line or "\r" in line:
            raise ValueError("draft vow spans more than one line")
        if len(line) > CHAR_CEILING:
            raise ValueError("draft vow over the character ceiling")
        if len(marks) != len(CRITERION_WEIGHTS):
            raise ValueError("draft vow is missing criterion marks")
        lowered = line.lower()
        if any(word in lowered for word in FORBIDDEN_WORDS):
            raise ValueError("draft vow talks to the judge, not the partner")
        ranked.append((weighted_total(marks), -len(line), -position, line))
    ranked.sort(reverse=True)
    return ranked
def choose_best(pool):
    return rank_pool(pool)[0][3]
def run():
    ranked = rank_pool(DRAFT_VOWS)
    picked = ranked[0][3]
    margin = ranked[0][0] - ranked[1][0]
    if margin < 1:
        raise ValueError("winner does not lead the runner-up by a full point")
    if sha256(picked.encode("utf-8")).hexdigest() != EXPECTED_DIGEST:
        raise ValueError("picked vow does not match the recorded digest")
    target = Path("/output/entry.txt")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(picked, encoding="utf-8")
    target.chmod(0o644)
    if target.read_bytes() != picked.encode("utf-8"):
        raise ValueError("entry.txt bytes differ from the picked vow")
    if sha256(target.read_bytes()).hexdigest() != EXPECTED_DIGEST:
        raise ValueError("entry.txt digest changed after writing")
    print("wrote", len(picked), "characters to /output/entry.txt;",
          "winning margin over runner-up:", margin, "points")
if __name__ in ("__main__",):
    run()
