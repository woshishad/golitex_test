---
name: theorem-to-litex
description: Use when translating a natural-language theorem, textbook result, dataset problem, proof sketch, or mathematical statement into Litex .lit code, including choosing a Litex-native formulation, preserving the source proof route, writing boundary-probing proof attempts, avoiding circular or assumption-driven proofs, running the verifier, recording exact errors, and classifying translated/checkable/blocked status.
---

# Theorem to Litex

Use this skill to turn a mathematical theorem or problem into Litex code. Follow
the Manual's central model: users write facts, and Litex grows a verified
context. For translation pressure tests, the goal is not always to force a green
file. The goal is to preserve the mathematical proof route, run the verifier,
and use exact failures to map Litex language, standard-library, builtin-rule,
kernel, and diagnostic gaps.

## Core workflow

1. Understand the theorem in ordinary mathematics before writing Litex.
2. Identify objects, domains, assumptions, conclusions, and any witnesses or cases.
3. Identify the source proof route before optimizing for Litex: finite enumeration, Cartesian-product count, quotient count, bijection, stars-and-bars, algebraic chain, witness construction, case split, induction, or theorem citation.
4. Choose the most Litex-native formulation that still tests the source proof idea. Do not replace the theorem by an easier arithmetic-only statement just to get success.
5. Write facts in mathematical order so each accepted line becomes context for later lines.
6. Run the smallest relevant verifier command, read the exact result, and make only the next correction that preserves the proof route.
7. If preserving the proof route fails, record the exact failing line/output and classify the blocker rather than weakening the statement.
8. Classify the item as `translated`, `checkable`, or `blocked`.

If the task is for this repository and the user asks for code that makes Litex
code verifiable, write the attempt in `examples/tmp.lit` and test it directly.

## Boundary-probing mode

Use boundary-probing mode for textbook, dataset, and benchmark translation work
whose purpose is to discover Litex gaps. In this mode:

- Prefer the source's mathematical proof flow over a convenient proof that avoids the hard step.
- It is acceptable, and often desirable, for the first `.lit` attempt to fail.
- Preserve the failing attempt in a nearby note, todo, or comment if the executable file must stay runnable.
- Record the exact verifier output: error type, line, statement, and message.
- Convert the failure into one primary blocker label.
- Do not "repair" a file by deleting the mathematical step being tested unless the user asks for a runnable demo.
- If a narrower runnable fragment is useful, keep it separate from the blocked source-route attempt and label it as a fragment.

For example, a combinations proof should try to formalize the set of subsets or
the bijection/quotient argument before falling back to the numerical identity
`20 * 19 * 18 / 6 = 1140`. The numerical identity is useful evidence about
arithmetic, but it is not evidence that Litex can express or prove the
combinatorial theorem.

## Formulating the statement

- Use builtin predicates and objects when they express the idea: `=`, `!=`, `<`, `<=`, `$in`, `$subset`, `$is_set`, `R`, `Z`, `N`, finite sets, tuples, functions, ranges, and standard set operations.
- Use `forall` block form for ordinary theorem statements. Without assumptions, put conclusions directly under `forall`; with assumptions, put hypotheses first, then `=>:`, then conclusions.
- Use `<=>:` only when both directions are intended. Otherwise use ordinary implication with `=>:`.
- Use `exist ... st { ... }` for existence statements and `witness` when proving one by explicit construction.
- Use `prop` for a reusable mathematical predicate with a definition. Use `abstract_prop` only for an intentionally uninterpreted concept, axiom interface, or clearly recorded proof debt.
- Use `claim` for short helper facts and local reusable `forall` patterns that should be available by shape matching.
- Use `thm name:` for named, classic, long, standard-library-facing, or parameter-sensitive theorems that should be cited explicitly with `by thm name(args...)`.

## Proof style

- Do not "shoot the arrow then draw the target": never assume the target theorem with `know`, `abstract_prop`, or an abstract counting predicate and then demonstrate only a numerical instance.
- Prefer explicit intermediate facts over large jumps.
- Use equality and inequality chains when they expose the ordinary calculation path.
- For counting statements, represent the counted objects directly when possible: define the finite sets, products, tuples, choices, or solution set, then prove a `count(...)` statement. Example pattern: if a two-stage choice has finite sets `A` and `B`, prove `count(cart(A, B)) = count(A) * count(B)` before instantiating numbers.
- For counting statements that need missing objects such as subsets of fixed cardinality, permutations, quotient counts, bijections, or integer-solution sets, attempt the natural object-level formulation first and record the verifier failure. Do not silently replace it with a staged product unless the staged product is the mathematical object being tested.
- When a line becomes `unknown`, add a smaller equality, membership fact, domain condition, nonzero denominator fact, witness, case split, or helper `claim`.
- When a line becomes `error`, fix syntax or well-definedness first: undeclared names, missing type facts, function arguments outside the domain, invalid local witness scope, or division by zero.
- Keep goal shapes close to known facts and known `forall` conclusions so Litex can match them structurally.
- For existential goals, give a concrete `witness`; to use a known existential fact, use `have by exist` to name the witness and import its body facts.
- For disjunctions, prove one branch directly or use `by cases` when a known split should prove a shared goal branch-by-branch.
- For finite enumerated domains, use `by enumerate finite_set`, `by enumerate range`, or `by enumerate closed_range` when the proof is naturally case exhaustion.
- For induction over integer-like parameters, use `by induc` or `by strong_induc` only after identifying the base and step facts clearly.

## Proof integrity checks

Before marking a theorem or example `checkable`, audit the file for these failure modes:

- **Target assumed as proof**: if the main conclusion appears only under `know`, `proof_debt`, or an `abstract_prop`, it is not proved.
- **Example-only validation**: verifying `3 * 10 = 30` does not prove the counting principle; it only verifies arithmetic after the counting model has been established.
- **Concrete-instance replacement**: first classify whether the source item is abstract or concrete. For an abstract theorem, do not replace the general statement with a proof over hand-picked concrete sets, numbers, tuples, or examples. If the source proof route uses arbitrary sets `A` and `B`, the Litex attempt should use `forall A, B ...` or another genuinely general formulation. Concrete witnesses are appropriate for existence proofs, and concrete objects are appropriate for counterexamples. For a concrete textbook problem or numerical example, it is valid to use the concrete objects and numbers from that problem, as long as the proof still follows the problem's mathematical chain rather than proving only an unrelated arithmetic fragment.
- **Predicate wrapper hiding the work**: a fact such as `$two_stage_count(item, m, n, m*n)` is acceptable only as an explicitly blocked interface or as a theorem already proved elsewhere, not as the proof itself.
- **Conclusion before construction**: for sets, functions, permutations, combinations, or solution counts, first construct or name the mathematical object being counted, then prove the count relation.
- **Status mismatch**: any file with unresolved `proof_debt`, target-shape `know`, or unproved abstract interfaces must be `blocked` or `translated`, not `checkable`.

When correcting a circular proof, rewrite it in this order:

1. State the ordinary mathematical proof route in comments.
2. Replace abstract target predicates with concrete objects when the language supports them.
3. Move unproved target facts into `# proof_debt:` comments or a local blocker note.
4. Keep only independently verified Litex facts as executable code.
5. Re-run the file and classify based on the executable facts, not the intended comments.

Do not overcorrect circular proofs into harmless arithmetic-only files. If the
source proof needs a quotient, bijection, or subset-counting principle that
Litex lacks, the best result may be a blocked file plus a precise minimal
reproduction and blocker note.

## Proof debt and blockers

`know` is an assumption or proof-debt marker, similar in role to `sorry`. Use it
only when the task intentionally introduces background facts, axiom interfaces,
or a precise blocked step. Do not hide a gap by weakening the theorem.

If `know` is used for a central mathematical step, keep the item out of
`checkable` status unless that step is explicitly a trusted theorem or builtin
rule already available in the current context. Prefer a commented
`# proof_debt:` line over executable `know` when the fact is only an intended
future proof.

When a proof is unfinished, record:

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

Use `checkable` only after running the relevant `.lit` code and seeing it
verify. Use `translated` when the statement is natural in Litex but the proof is
unfinished. Use `blocked` when the failure reason is understood. Prefer blocker
labels such as `blocked_by_language`, `blocked_by_stdlib`,
`blocked_by_infer_rule`, `blocked_by_kernel`, `blocked_by_syntax`,
`blocked_by_diagnostics`, or `blocked_by_formulation`.

For blocked items, include the most useful failed attempt. If the `.lit` file is
kept runnable, put the failed attempt and exact output in a nearby `todo.md` or
problem note. A good blocker record includes:

- the source theorem/example id,
- the intended proof step,
- the smallest Litex snippet that failed,
- the exact verifier output,
- the suspected missing feature or builtin rule,
- the primary blocker label.

## Running and interpreting Litex

- For a single file, run `litex -f path/to/file.lit` when the installed CLI is available.
- In this repository, use the smallest relevant test first; for example snippets, use `cargo test run_examples -- --nocapture` when appropriate.
- Treat verifier outcomes exactly:
  - `true`: keep the fact and continue.
  - `unknown`: the proof needs a smaller intermediate fact or better-shaped lemma.
  - `error`: syntax or well-definedness must be fixed before proof search matters.
- Read `verified_by` and `infer_facts` output when available. It shows whether a fact closed by builtin rules, known facts, known `forall` facts, theorem citation, or inferred context.
- After a proof works, remove unnecessary broad `know` facts and keep only explicit trusted assumptions with a reason.

## Output format for users

When reporting the result, include:

- The natural-language proof idea.
- The `.lit` file path or code snippet.
- The verifier command used.
- The status: `checkable`, `translated`, or `blocked`.
- Any remaining `know` facts or blocker labels.
- The next smallest step if the proof is not checkable yet.
