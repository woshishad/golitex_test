---
name: contribute-to-litex
description: Use when helping users contribute to Litex: documentation feedback, contribution task triage, dataset or textbook translation work, blocker records, demo/readability improvements, or preparing a contribution PR.
---

# Contribute to Litex

Use this skill for Litex contribution work. The default contribution path is
documentation clarity, dataset or textbook translation, blocker reporting, and
public understanding. Do not start by changing verifier, parser, builtin-rule,
or soundness-critical logic unless the user explicitly asks for that work and
the local code context supports it.

## First classify the contribution

Before acting, identify the contribution type:

- **Documentation feedback**: README, Manual, Mechanics notes, examples, website docs, setup docs, or confusing verifier output.
- **Datasets or textbooks**: horizontal dataset work or vertical textbook/chapter translation.
- **Understanding improvements**: README sections, demo notes, benchmark pages, contribution guides, or external-facing explanations.
- **Kernel engineering**: verifier, parser, builtin rules, inference rules, runtime, or soundness-sensitive behavior.

For new contributors, prefer the first three categories. Treat kernel
engineering as an advanced path.

## Documentation feedback

Good documentation feedback is small and exact. Record:

- The page, section, example, or file that was read.
- The first sentence, concept, code block, output, or error message that caused confusion.
- What the reader expected it to mean.
- What it actually appeared to mean.
- What would make it easier to follow.

One precise confusion point is better than a broad statement such as "the docs
are hard to read."

## Dataset and textbook work

For datasets, work horizontally: improve or expand problem collections such as
MATH500, miniF2F-style problems, high-school math, contests, or exams.

For textbooks, work vertically: translate a book or chapter in source order,
preserve the mathematical structure, and record what Litex can or cannot
express yet.

Prefer a first slice of 20-50 representative items before attempting broad
coverage. Useful contribution tasks include:

- Fixing statements, cleaning Litex code, updating statuses, removing bad records, or making proof attempts clearer.
- Adding missing sources, selecting an initial slice, or adding missing translated items.
- Recording blockers with the smallest useful reproduction or note.
- Adding license notes when source text cannot be redistributed.

For each translated item, keep this record shape:

```yaml
id:
source:
topic:
difficulty:
natural_language_idea:
litex_code:
proof_attempt:
status: translated/checkable/blocked
blocker:
notes:
```

Status rules:

- Use `checkable` only after the relevant `.lit` code has been run and verified.
- Use `translated` when the statement is natural in Litex but the proof is unfinished.
- Use `blocked` when the reason is understood and recorded.
- If source text cannot be redistributed, put the license caveat in `notes` and keep a reusable mathematical reformulation.

## Understanding improvements

When improving public-facing material, make at least one important question
clearer:

- What can Litex already run?
- How is Litex different from Lean or ordinary LLM problem solving?
- What is the strongest current demo?
- Which mathematical examples are already checkable?
- Which parts are blocked, and what do those blockers teach us?
- How can another person get involved?

Good targets include README sections, demo notes, benchmark pages, dataset
gallery pages, and contribution guidance.

## Validation

For contribution changes, validate the smallest relevant surface first:

- For `.lit` examples, run the specific file or the smallest relevant example test before broader tests.
- For examples or docs snippets, run `cargo test run_examples -- --nocapture` when appropriate.
- For Mechanics markdown snippets, run `cargo test run_the_mechanics_markdown_files -- --nocapture`.
- For dataset records, verify that statuses match the recorded evidence and that `checkable` items were actually run.

Report exact verifier failures, file names, snippet labels, or confusing output
when a contribution reveals a blocker or diagnostic issue.
