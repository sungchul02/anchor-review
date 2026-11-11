"""Shuffle the blind submissions into reviewer batches and write one task file per reviewer.

Usage:
    python assign.py <subs_dir> <run_dir> <reviewer_prompt.md> [--per 5] [--venues "ACL 2027,EMNLP 2027,NAACL 2027"] [--seed 1]

<subs_dir> holds paper_<ID>.md for every anchor and target, already anonymized and stripped.

Each venue is one full pass over all submissions, so every paper gets exactly one review per venue
(three reviews with the default venues). Batch sizes are near-equal (e.g. 26 papers -> 5, 5, 5, 5, 6).

Writes:
    <run_dir>/tasks/<VENUE>_<k>.md   prompt for one reviewer subagent
    <run_dir>/reviews/               where reviewers write their reviews
    <run_dir>/plan.json              which papers went to which reviewer
"""
import argparse
import json
import pathlib
import random
import re

PLACEHOLDERS = ("{VENUE}", "{N}", "{DIR}", "{FILES}", "{OUT}")


def make_batches(ids, per, rng):
    shuffled = ids[:]
    rng.shuffle(shuffled)
    n_batches = max(1, round(len(shuffled) / per))
    return [shuffled[i::n_batches] for i in range(n_batches)]


def fill(template, venue, batch, subs_dir, review_path):
    prompt = (template
              .replace("{VENUE}", venue)
              .replace("{N}", str(len(batch)))
              .replace("{DIR}", subs_dir.as_posix())
              .replace("{FILES}", ", ".join(f"paper_{pid}.md" for pid in batch))
              .replace("{OUT}", review_path.as_posix()))
    left = [p for p in PLACEHOLDERS if p in prompt]
    if left:
        raise ValueError(f"unfilled placeholders in the prompt: {left}")
    return prompt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("subs")
    ap.add_argument("run")
    ap.add_argument("prompt")
    ap.add_argument("--per", type=int, default=5, help="papers per reviewer (default 5)")
    ap.add_argument("--venues", default="ACL 2027,EMNLP 2027,NAACL 2027")
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    subs, run = pathlib.Path(args.subs).resolve(), pathlib.Path(args.run).resolve()
    (run / "tasks").mkdir(parents=True, exist_ok=True)
    (run / "reviews").mkdir(parents=True, exist_ok=True)
    template = pathlib.Path(args.prompt).read_text(encoding="utf-8")
    ids = sorted(f.stem[len("paper_"):] for f in subs.glob("paper_*.md"))
    rng = random.Random(args.seed)

    plan = {}
    for venue in (v.strip() for v in args.venues.split(",")):
        plan[venue] = make_batches(ids, args.per, rng)
        for k, batch in enumerate(plan[venue], start=1):
            name = f"{venue.split()[0]}_{k}"
            prompt = fill(template, venue, batch, subs, run / "reviews" / f"{name}.md")
            (run / "tasks" / f"{name}.md").write_text(prompt, encoding="utf-8")

    (run / "plan.json").write_text(json.dumps(plan, indent=1), encoding="utf-8")
    n_tasks = sum(len(b) for b in plan.values())
    print(f"{len(ids)} submissions -> {n_tasks} reviewer tasks in {run / 'tasks'}")


if __name__ == "__main__":
    main()
