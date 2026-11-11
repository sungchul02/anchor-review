"""Write one task file per reviewer for a blind review run.

Default (tiered, full bundle):
    python assign.py <subs_dir> <run_dir> <reviewer_prompt.md> --tiers presets/tiers.json --target-venue ACL [--seed 1]

    One reviewer per venue tier (target venue, a peer venue of the same level, a slightly easier venue).
    Every reviewer reads the WHOLE bundle (all papers in <subs_dir>), each in its own random order,
    and scores every paper. With a 15-paper bundle that is 3 reviewers x 15 papers.

Split mode (older calibration runs; only when --tiers is not given):
    python assign.py <subs_dir> <run_dir> <reviewer_prompt.md> --per 5 [--venues "ACL 2027,EMNLP 2027,NAACL 2027"]

    Each venue is one pass over all papers, split into batches of about --per papers.

<subs_dir> holds paper_<ID>.md for every anchor and target, already anonymized and stripped.

Writes:
    <run_dir>/tasks/<NAME>.md   prompt for one reviewer subagent
    <run_dir>/reviews/          where reviewers write their reviews
    <run_dir>/plan.json         which papers went to which reviewer, in which order
"""
import argparse
import json
import pathlib
import random

PLACEHOLDERS = ("{VENUE}", "{VENUE_NOTE}", "{VENUE_CRITERIA}", "{N}", "{DIR}", "{FILES}", "{OUT}")


def make_batches(ids, per, rng):
    shuffled = ids[:]
    rng.shuffle(shuffled)
    n_batches = max(1, round(len(shuffled) / per))
    return [shuffled[i::n_batches] for i in range(n_batches)]


def fill(template, venue, note, batch, subs_dir, review_path, criteria=""):
    prompt = (template
              .replace("{VENUE_CRITERIA}", criteria or "(no venue criteria file; use the official scales only)")
              .replace("{VENUE_NOTE}", note)
              .replace("{VENUE}", venue)
              .replace("{N}", str(len(batch)))
              .replace("{DIR}", subs_dir.as_posix())
              .replace("{FILES}", ", ".join(f"paper_{pid}.md" for pid in batch))
              .replace("{OUT}", review_path.as_posix()))
    left = [p for p in PLACEHOLDERS if p in prompt]
    if left:
        raise ValueError(f"unfilled placeholders in the prompt: {left}")
    return prompt


def tiered_tasks(ids, tiers, rng, criteria_dir=None):
    """One reviewer per tier, each reading every paper in its own random order.
    If criteria_dir holds tier_<tier>_<venue>.md (written in phase 1), it is inserted into that tier's prompt."""
    tasks = []
    for t in tiers:
        order = ids[:]
        rng.shuffle(order)
        name = f"{t['tier']}_{t['venue'].split()[0]}"
        crit_file = pathlib.Path(criteria_dir).expanduser() / f"tier_{name}.md" if criteria_dir else None
        criteria = crit_file.read_text(encoding="utf-8") if crit_file and crit_file.exists() else ""
        if criteria_dir and not criteria:
            print(f"WARNING: no criteria file {crit_file}")
        tasks.append((name, t["venue"], t["note"], order, criteria))
    return tasks


def split_tasks(ids, venues, per, rng):
    tasks = []
    for venue in venues:
        for k, batch in enumerate(make_batches(ids, per, rng), start=1):
            tasks.append((f"{venue.split()[0]}_{k}", venue, "", batch, ""))
    return tasks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subs")
    ap.add_argument("run")
    ap.add_argument("prompt")
    ap.add_argument("--tiers", help="tiers JSON (presets/tiers.json); enables the tiered full-bundle mode")
    ap.add_argument("--target-venue", default="ACL", help="key in the tiers JSON (default ACL)")
    ap.add_argument("--criteria-dir", help="folder with tier_<tier>_<venue>.md criteria from phase 1 (optional)")
    ap.add_argument("--per", type=int, default=5, help="split mode only: papers per reviewer")
    ap.add_argument("--venues", default="ACL 2027,EMNLP 2027,NAACL 2027", help="split mode only")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    subs, run = pathlib.Path(args.subs).resolve(), pathlib.Path(args.run).resolve()
    (run / "tasks").mkdir(parents=True, exist_ok=True)
    (run / "reviews").mkdir(parents=True, exist_ok=True)
    template = pathlib.Path(args.prompt).read_text(encoding="utf-8")
    ids = sorted(f.stem[len("paper_"):] for f in subs.glob("paper_*.md"))
    rng = random.Random(args.seed)

    if args.tiers:
        tiers = json.loads(pathlib.Path(args.tiers).read_text(encoding="utf-8"))[args.target_venue]
        tasks = tiered_tasks(ids, tiers, rng, args.criteria_dir)
    else:
        tasks = split_tasks(ids, [v.strip() for v in args.venues.split(",")], args.per, rng)

    plan = {}
    for name, venue, note, batch, criteria in tasks:
        prompt = fill(template, venue, note, batch, subs, run / "reviews" / f"{name}.md", criteria)
        (run / "tasks" / f"{name}.md").write_text(prompt, encoding="utf-8")
        plan[name] = dict(venue=venue, papers=batch)
    (run / "plan.json").write_text(json.dumps(plan, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(ids)} submissions -> {len(tasks)} reviewer tasks in {run / 'tasks'}: "
          + ", ".join(f"{n} ({len(b)} papers)" for n, _, _, b, _ in tasks))


if __name__ == "__main__":
    main()
