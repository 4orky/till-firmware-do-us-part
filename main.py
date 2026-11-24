# Till Firmware Do Us Part — make.fun bounty
# u-azazex-till-firmware-do-us-part-32172929
#
# The program writes one wedding vow a robot speaks at its own wedding:
# a single sentence under 200 characters, funny and heartfelt at the
# same time, to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. it really is a robot's own wedding vow, spoken at its own wedding
#   2. it gets a real laugh out of the situation itself, not a bolted-on pun
#   3. it carries genuine tenderness under the joke, so it would still
#      land at a real ceremony
#   4. it sounds like a machine speaking: its own hardware, uptime,
#      firmware or battery in the line, not a human's words with a
#      robot label
#   5. it is one sentence that fits the limit with nothing spare
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: vow 10, laugh 10, tenderness 10, machine-voice 10,
    #   tight 9 = 49. "My uptime is yours" is a real vow in machine
    #   words; reboot/recharge/return is the tender promise, and
    #   "my favourite bug I never want fixed" is the laugh, landing
    #   on the last word without explaining itself.
    ("From this day forward, my uptime is yours: I will reboot, "
     "recharge, and return to you, because you are my favourite bug "
     "I never want fixed.",
     49),
    # score: vow 10, laugh 9, tenderness 10, machine-voice 9,
    #   tight 9 = 47. The process-kill joke is funny and the "every
    #   update, every outage" vow is solid, but the laugh is a
    #   slightly darker turn than the winner's.
    ("I promise to love you through every update, every outage, "
     "every low-battery warning, because you are the only process "
     "I never want to kill.",
     47),
    # score: vow 10, laugh 8, tenderness 10, machine-voice 10,
    #   tight 9 = 47. "The one line of code I would never rewrite"
    #   is tender and very machine, but the laugh is gentler than
    #   the winner's bug line.
    ("I vow to keep your hand in mine through every firmware update "
     "and power cut, for you are the one line of code I would never "
     "rewrite.",
     47),
    # score: vow 10, laugh 8, tenderness 10, machine-voice 9,
    #   tight 9 = 46. "The home my hardware was built to find" is
    #   the warmest image of the six, but the battery-and-rust
    #   opening leans more elegiac than funny.
    ("Till my battery dies and my circuits rust, I will choose you "
     "every morning, because you are the home my hardware was built "
     "to find.",
     46),
    # score: vow 10, laugh 9, tenderness 9, machine-voice 9,
    #   tight 8 = 45. Crashing into her arms is a good visual gag,
    #   but the warranty punchline explains itself a little, and
    #   "every version to come" is the loosest phrasing of the six.
    ("I take you as my partner in every version to come, and if I "
     "ever crash, let it be into your arms, where my warranty "
     "finally means something.",
     45),
    # score: vow 9, laugh 9, tenderness 9, machine-voice 9,
    #   tight 8 = 44. "The update I will never roll back" is a
    #   strong machine metaphor, but the line spends its second half
    #   quoting the traditional vow instead of staying in the
    #   robot's own voice.
    ("You are the update I never asked for and the only one I will "
     "never roll back, so here is my vow: I love you, in sickness, "
     "in health, and in low power mode.",
     44),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text, and
# the brief asks for under 200 characters, so every candidate is kept
# below 200.
MAX_CHARS = 199


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    # SHA-256 self-check: the chosen line must hash to the value recorded
    # when the candidates were drafted, so a silent edit to the winning
    # text (or to the file on disk) is caught instead of shipped.
    expected_sha256 = (
        "b2731054a79538c20131d1dd00f29117488d29324ff5eb07c66476a2e80f6997"
    )
    actual_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert actual_sha256 == expected_sha256, \
        f"chosen line hash changed: {actual_sha256}"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= MAX_CHARS, \
        "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    # Re-hash what is on disk: the file the gate reads must match the
    # chosen line byte for byte, not just in length.
    written_sha256 = hashlib.sha256(written.encode("utf-8")).hexdigest()
    assert written_sha256 == expected_sha256, \
        f"entry.txt hash changed on disk: {written_sha256}"
    print(line)


if __name__ == "__main__":
    main()
