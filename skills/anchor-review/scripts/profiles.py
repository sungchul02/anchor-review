"""Save a calibrated setup once (a "profile"), then reuse it for every later review.

A profile is one venue × field combination, e.g. "ARR × RAG". It holds:
- the anchors (blind texts and the confidential key)
- the reviewer prompt that was validated on them
- the calibration result (reliability AUC and score distribution per class)

Profiles live in ~/.claude/anchor-review/profiles/<name>/. They are local only; never publish them,
because they contain other people's paper texts.

Usage:
    # 1) after the first calibration run, save the profile
    python profiles.py save <name> --venue "ACL/EMNLP/NAACL (ARR)" --field "RAG, context compression"
        --subs <anchor_subs_dir> --key <key.md> --reviews <calibration_reviews_dir> [--prompt <reviewer_prompt.md>]

    # 2) list saved profiles
    python profiles.py list

    # 3) for a new review: copy a sample of anchors plus the target(s) into a fresh submissions folder
    python profiles.py sample <name> <run_subs_dir> --targets paper_ABCD.md[,paper_EFGH.md] [--mix "MAIN=3,FINDINGS=2,COLING=2,ARXIV-ONLY=2"] [--seed 1]
    # default bundle: 9 anchors + the target = 10 papers, which every tier reviewer reads in full

Then run assign.py on <run_subs_dir> and aggregate.py with the profile's key.md (see SKILL.md).
"""
import argparse
import json
import pathlib
import random
import shutil
import statistics as st
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import aggregate  # noqa: E402  (reuses the key reader, review parser and AUC)

ROOT = pathlib.Path.home() / ".claude" / "anchor-review" / "profiles"
DEFAULT_PROMPT = pathlib.Path(__file__).parent.parent / "reference" / "reviewer_prompt.md"


def save(args):
    dest = ROOT / args.name
    if dest.exists() and not args.overwrite:
        sys.exit(f"profile {args.name} exists; pass --overwrite to replace it")
    cls = aggregate.read_key(args.key)
    overall, _, _, by_reviewer = aggregate.read_reviews(args.reviews, set(cls))
    means = {p: st.mean(v) for p, v in overall.items()}
    reliability = aggregate.auc(means, cls, aggregate.ACCEPTED, ("ARXIV-ONLY",))
    if reliability is None or reliability < 0.75:
        print(f"WARNING: reliability AUC {reliability} < 0.75; the profile will be marked unreliable")

    if dest.exists():
        shutil.rmtree(dest)
    (dest / "subs").mkdir(parents=True)
    for pid in cls:
        src = pathlib.Path(args.subs) / f"paper_{pid}.md"
        if src.exists():
            shutil.copy(src, dest / "subs" / src.name)
    shutil.copy(args.key, dest / "key.md")
    shutil.copy(args.prompt, dest / "reviewer_prompt.md")
    shutil.copytree(args.reviews, dest / "calibration_reviews")

    per_class = {}
    for c in aggregate.CLASSES:
        v = sorted(round(s, 3) for p, s in means.items() if cls.get(p) == c)
        if v:
            per_class[c] = dict(n=len(v), mean=round(st.mean(v), 3), median=round(st.median(v), 3), scores=v)
    per_reviewer = {name: dict(auc=aggregate.auc(s, cls, aggregate.ACCEPTED, ("ARXIV-ONLY",)),
                               class_means=aggregate.class_means(s, cls))
                    for name, s in sorted(by_reviewer.items())}
    info = dict(name=args.name, venue=args.venue, field=args.field, created=time.strftime("%Y-%m-%d"),
                anchors=len(cls), reliability_auc=reliability, reliable=bool(reliability and reliability >= 0.75),
                per_class=per_class, per_reviewer=per_reviewer)
    (dest / "profile.json").write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"saved profile {args.name} at {dest} (anchors {len(cls)}, reliability AUC {reliability})")


def list_profiles(_args):
    if not ROOT.exists() or not any(ROOT.iterdir()):
        print("no profiles yet")
        return
    for d in sorted(ROOT.iterdir()):
        p = d / "profile.json"
        if p.exists():
            info = json.loads(p.read_text(encoding="utf-8"))
            print(f"{info['name']}: {info['venue']} × {info['field']} | anchors {info['anchors']} | "
                  f"AUC {info['reliability_auc']} | created {info['created']}")


def sample(args):
    prof = ROOT / args.name
    cls = aggregate.read_key(prof / "key.md")
    rng = random.Random(args.seed)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    available = {c: sorted(p for p, k in cls.items() if k == c and (prof / "subs" / f"paper_{p}.md").exists())
                 for c in aggregate.CLASSES}
    if args.mix:
        mix = {c: int(n) for c, n in (kv.split("=") for kv in args.mix.split(","))}
    else:  # default bundle of 9 anchors: 3 MAIN, 2 FINDINGS, 2 COLING, 2 ARXIV-ONLY (3/3/3 without COLING anchors)
        mix = ({"MAIN": 3, "FINDINGS": 2, "COLING": 2, "ARXIV-ONLY": 2} if available.get("COLING")
               else {"MAIN": 3, "FINDINGS": 3, "ARXIV-ONLY": 3})
    chosen = []
    for c, n in mix.items():
        ids = available.get(c, [])
        if len(ids) < n:
            print(f"WARNING: only {len(ids)} {c} anchors available, wanted {n}")
        chosen += rng.sample(ids, min(n, len(ids)))
    for pid in chosen:
        shutil.copy(prof / "subs" / f"paper_{pid}.md", out / f"paper_{pid}.md")
    for t in args.targets.split(","):
        t = pathlib.Path(t)
        if t.stem[len("paper_"):] in cls:
            sys.exit(f"target ID {t.stem} collides with an anchor ID; rename the target")
        shutil.copy(t, out / t.name)
    print(f"{len(chosen)} anchors + {len(args.targets.split(','))} target(s) in {out}")
    print(f"key for aggregate.py: {prof / 'key.md'}   prompt for assign.py: {prof / 'reviewer_prompt.md'}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("save")
    s.add_argument("name"); s.add_argument("--venue", required=True); s.add_argument("--field", required=True)
    s.add_argument("--subs", required=True); s.add_argument("--key", required=True); s.add_argument("--reviews", required=True)
    s.add_argument("--prompt", default=str(DEFAULT_PROMPT)); s.add_argument("--overwrite", action="store_true")
    s.set_defaults(func=save)
    sub.add_parser("list").set_defaults(func=list_profiles)
    m = sub.add_parser("sample")
    m.add_argument("name"); m.add_argument("out"); m.add_argument("--targets", required=True)
    m.add_argument("--mix", help='anchors per class (default "MAIN=3,FINDINGS=2,COLING=2,ARXIV-ONLY=2")')
    m.add_argument("--seed", type=int, default=1)
    m.set_defaults(func=sample)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
