You are analyzing papers whose publication outcome is known, in order to write review criteria from real examples.

All {N} papers in `{DIR}` share the same outcome: **{CLASS_DESC}**. Topic area: {FIELD}.

Rules:
- Read only the files in `{DIR}`. Do not search the web. Make no changes other than writing `{OUT}`.
- Read the papers one at a time. After each paper, append your notes for it to `{OUT}` under `## paper_<ID>` before you open the next one.
- Describe properties of the paper as submitted. Do not guess authors or venues, and do not copy long passages.

For each paper, note in Korean, with short evidence pointers (section or table):
1. Contribution type: new task or problem, characterized phenomenon, method, resource or benchmark, analysis, or system.
2. What is new, in one or two sentences, and how big the step is (new framing, a strong advance, or an incremental variant).
3. Evidence breadth:
   - the datasets
   - the models and their sizes
   - the baselines, and whether they are strong and run under the same settings
   - ablations
   - statistics or variance
4. Whether the central claims are supported, partly supported or not supported, and why.
5. Visible flaws, each marked major (it threatens a central claim) or minor.
6. Scope and realism: a toy or controlled setup, standard benchmarks, or realistic or harder settings.
7. Writing of the claims: precise, slightly overstated, or overclaimed.

After the last paper, append a section `## Common pattern` that summarizes what these papers have in common. For each item, give how many of the {N} papers show it. Be concrete, and also note the exceptions:
- the typical contribution type and size of step
- the typical evidence breadth
- the typical flaws, including the ones that coexisted with this outcome
- what seems to be the minimum that papers with this outcome had
