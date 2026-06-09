#!/usr/bin/env python3
"""
Extract theorem-like results from a probability textbook PDF.

Default output is Markdown with:

定理内容:
证明链路:

The extraction is heuristic because textbook PDFs do not expose semantic theorem
boundaries. The script keeps page numbers and source snippets so failures can be
audited and improved.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


try:
    from pypdf import PdfReader
except ImportError:  # pragma: no cover - exercised by user environment
    PdfReader = None


DEFAULT_LABELS = ("Theorem", "Proposition", "Lemma", "Corollary")


@dataclass
class TheoremRecord:
    label: str
    number: str
    title: str
    page_start: int
    page_end: int
    theorem_content: str
    proof_chain: list[str]
    raw_proof: str
    extraction_notes: list[str]


@dataclass
class TextLine:
    page: int
    text: str


@dataclass
class Chapter1Record:
    id: str
    kind: str
    source_section: str
    page_start: int
    page_end: int
    content: str
    litex_proof_chain: list[str]
    litex_objects: list[str]
    status: str
    blocker: str
    notes: str


def normalize_text(text: str) -> str:
    replacements = {
        "\ufb01": "fi",
        "\ufb02": "fl",
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "Ú": ">=",
        "…": "<=",
    }
    normalized = text
    for source, target in replacements.items():
        normalized = normalized.replace(source, target)
    normalized = re.sub(r"[ \t]+", " ", normalized)
    return normalized.strip()


def extract_lines(pdf_path: Path) -> list[TextLine]:
    if PdfReader is None:
        raise RuntimeError(
            "Missing dependency: pypdf. Run with the bundled Python shown by "
            "`codex_app.load_workspace_dependencies`, or install pypdf."
        )

    reader = PdfReader(str(pdf_path))
    lines: list[TextLine] = []
    for page_index, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        for raw_line in page_text.splitlines():
            line = normalize_text(raw_line)
            if line:
                lines.append(TextLine(page=page_index, text=line))
    return lines


def heading_regex(labels: Iterable[str]) -> re.Pattern[str]:
    labels_pattern = "|".join(re.escape(label) for label in labels)
    return re.compile(
        rf"^(?P<label>{labels_pattern})\s+"
        rf"(?P<number>\d+(?:\.\d+)*)"
        rf"(?P<punct>[.]?)"
        rf"(?:\s+(?P<rest>.*))?$"
    )


def hard_stop_regex(labels: Iterable[str]) -> re.Pattern[str]:
    labels_pattern = "|".join(re.escape(label) for label in labels)
    return re.compile(
        rf"^((?P<label>{labels_pattern})\s+\d+(?:\.\d+)*[.]?\b|"
        rf"Example\s+\d+|"
        rf"Remarks?[.]|"
        rf"Summary$|"
        rf"Exercises$|"
        rf"Problems$|"
        rf"Self-Test Problems|"
        rf"Chapter\s+\d+|"
        rf"Section\s+\d+(?:\.\d+)*|"
        rf"\d+(?:\.\d+)+\s+[A-Z])"
        ,
        re.IGNORECASE,
    )


def looks_like_running_header(line: str) -> bool:
    return bool(
        re.match(r"^\d+\s+Chapter\s+\d+", line)
        or re.match(r"^Section\s+\d+(?:\.\d+)*\s+", line)
        or re.match(r"^\d+\s*$", line)
    )


def find_heading_indices(lines: list[TextLine], labels: Iterable[str]) -> list[int]:
    heading_pattern = heading_regex(labels)
    indices: list[int] = []
    for index, text_line in enumerate(lines):
        if looks_like_running_header(text_line.text):
            continue
        match = heading_pattern.match(text_line.text)
        if not match:
            continue
        rest = match.group("rest") or ""
        rest_lower = rest.lower()
        if rest_lower.startswith(
            (
                "in chapter",
                "in words",
                "is proved",
                "is as follows",
                "could",
                "tells",
                "states",
                "is useful",
                "will",
                "may",
                "and ",
                "by ",
                "from ",
            )
        ):
            continue
        indices.append(index)
    return indices


def collect_block(
    lines: list[TextLine],
    start_index: int,
    next_heading_index: int | None,
    labels: Iterable[str],
) -> list[TextLine]:
    stop_pattern = hard_stop_regex(labels)
    end_index = next_heading_index if next_heading_index is not None else len(lines)
    block = [lines[start_index]]

    for line in lines[start_index + 1 : end_index]:
        if looks_like_running_header(line.text):
            continue
        if stop_pattern.match(line.text):
            break
        block.append(line)

    return block


def join_lines(block: list[TextLine]) -> str:
    text = " ".join(line.text for line in block)
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return text.strip()


def split_statement_and_proof(full_text: str, heading_text: str) -> tuple[str, str, list[str]]:
    notes: list[str] = []
    body = full_text[len(heading_text) :].strip()
    proof_patterns = [
        r"\bProof of [^:]{1,120}:",
        r"\bProof\.",
        r"\bProof:",
    ]

    proof_match: re.Match[str] | None = None
    for pattern in proof_patterns:
        proof_match = re.search(pattern, body)
        if proof_match:
            break

    if proof_match:
        theorem_content = body[: proof_match.start()].strip()
        raw_proof = body[proof_match.end() :].strip()
    else:
        theorem_content = body.strip()
        raw_proof = ""
        notes.append("No explicit proof marker found in extracted block.")

    if not theorem_content:
        theorem_content = heading_text
        notes.append("Statement may be split across formulas or lost by PDF extraction.")

    if not raw_proof:
        notes.append("Proof chain is empty or appears outside the detected block.")

    return theorem_content, raw_proof, notes


def split_proof_chain(raw_proof: str, max_steps: int | None) -> list[str]:
    if not raw_proof:
        return []

    cleaned = re.sub(r"\s+", " ", raw_proof).strip()
    cleaned = re.sub(r"\b(QED|q\.e\.d\.)\b", "", cleaned, flags=re.IGNORECASE)
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(])", cleaned)
    steps: list[str] = []

    for sentence in sentences:
        step = sentence.strip(" ;")
        if not step:
            continue
        step = re.sub(r"^(Hence|Thus|Therefore|Consequently),?\s+", r"\1, ", step)
        steps.append(step)
        if max_steps is not None and len(steps) >= max_steps:
            break

    if max_steps is not None and len(sentences) > max_steps:
        steps.append(f"... truncated; {len(sentences) - max_steps} more extracted proof sentence(s).")

    return steps


def parse_records(
    lines: list[TextLine],
    labels: Iterable[str],
    max_proof_steps: int | None,
) -> list[TheoremRecord]:
    heading_pattern = heading_regex(labels)
    heading_indices = find_heading_indices(lines, labels)
    records: list[TheoremRecord] = []

    for position, start_index in enumerate(heading_indices):
        next_heading_index = (
            heading_indices[position + 1] if position + 1 < len(heading_indices) else None
        )
        block = collect_block(lines, start_index, next_heading_index, labels)
        heading_line = block[0].text
        heading_match = heading_pattern.match(heading_line)
        if heading_match is None:
            continue

        label = heading_match.group("label")
        number = heading_match.group("number")
        title = (heading_match.group("rest") or "").strip()
        full_text = join_lines(block)
        theorem_content, raw_proof, notes = split_statement_and_proof(full_text, heading_line)
        proof_chain = split_proof_chain(raw_proof, max_proof_steps)

        records.append(
            TheoremRecord(
                label=label,
                number=number,
                title=title,
                page_start=block[0].page,
                page_end=block[-1].page,
                theorem_content=theorem_content,
                proof_chain=proof_chain,
                raw_proof=raw_proof,
                extraction_notes=notes,
            )
        )

    return deduplicate_records(records)


def record_score(record: TheoremRecord) -> int:
    return len(record.title) + len(record.theorem_content) + len(record.raw_proof)


def deduplicate_records(records: list[TheoremRecord]) -> list[TheoremRecord]:
    deduplicated: list[TheoremRecord] = []
    for record in records:
        if (
            deduplicated
            and deduplicated[-1].label == record.label
            and deduplicated[-1].number == record.number
            and deduplicated[-1].page_start == record.page_start
        ):
            if record_score(record) > record_score(deduplicated[-1]):
                deduplicated[-1] = record
            continue
        deduplicated.append(record)
    return deduplicated


def chapter_page_lines(lines: list[TextLine], chapter_number: int) -> list[TextLine]:
    chapter_pattern = re.compile(rf"^CHAPTER\s+{chapter_number}$", re.IGNORECASE)
    next_chapter_pattern = re.compile(rf"^CHAPTER\s+{chapter_number + 1}$", re.IGNORECASE)

    start_page: int | None = None
    end_page: int | None = None
    for line in lines:
        if start_page is None and chapter_pattern.match(line.text):
            start_page = line.page
            continue
        if start_page is not None and next_chapter_pattern.match(line.text):
            end_page = line.page
            break

    if start_page is None:
        raise RuntimeError(f"Could not find CHAPTER {chapter_number} in PDF text.")
    return [
        line
        for line in lines
        if line.page >= start_page and (end_page is None or line.page < end_page)
    ]


def chapter1_theorem_records() -> list[Chapter1Record]:
    return [
        Chapter1Record(
            id="ch1_theorem_01_basic_counting",
            kind="theorem",
            source_section="1.2 The Basic Principle of Counting",
            page_start=17,
            page_end=17,
            content=(
                "If experiment 1 has m possible outcomes and, for each outcome of "
                "experiment 1, experiment 2 has n possible outcomes, then the two "
                "experiments together have mn possible outcomes."
            ),
            litex_proof_chain=[
                "Introduce finite sets A and B for the possible outcomes of the first and second experiments.",
                "Represent a two-stage outcome as an ordered pair in cart(A, B).",
                "Use Litex finite-set support to prove count(cart(A, B)) = count(A) * count(B).",
                "Use count(A)=m and count(B)=n to rewrite the final count as m*n.",
            ],
            litex_objects=["A finite_set", "B finite_set", "cart(A, B)", "count(cart(A, B))"],
            status="translated",
            blocker="",
            notes=(
                "Candidate route for direct verification. Keep as translated until a concrete "
                ".lit file is generated and run."
            ),
        ),
        Chapter1Record(
            id="ch1_theorem_02_generalized_counting",
            kind="theorem",
            source_section="1.2 The Basic Principle of Counting",
            page_start=17,
            page_end=17,
            content=(
                "For r staged experiments with n1, n2, ..., nr possible outcomes at "
                "successive stages, the total number of outcomes is n1*n2*...*nr."
            ),
            litex_proof_chain=[
                "For a fixed finite number of stages, introduce finite sets A1, ..., Ar.",
                "Represent a complete experimental outcome as a tuple in cart(A1, ..., Ar).",
                "Use count(cart(A1, ..., Ar)) = count(A1)*...*count(Ar).",
                "For arbitrary r, a recursive finite product interface would be needed.",
            ],
            litex_objects=["cart(A1, ..., Ar)", "count(cart(...))", "finite product over stage counts"],
            status="translated",
            blocker="blocked_by_stdlib",
            notes="Fixed arity is checkable; arbitrary r needs a finite-list/product theorem.",
        ),
        Chapter1Record(
            id="ch1_theorem_03_permutations",
            kind="theorem",
            source_section="1.3 Permutations",
            page_start=19,
            page_end=19,
            content="There are n! = n(n-1)...3*2*1 possible linear orderings of n distinct items.",
            litex_proof_chain=[
                "Define the set of no-repeat sequences of length n drawn from an n-element finite set.",
                "Expose the staged proof route: n choices for the first position, n-1 for the second, and so on.",
                "Prove a bijection between no-repeat sequences and staged choice records.",
                "Use the generalized counting principle to obtain n!.",
            ],
            litex_objects=["permutations(S)", "no-repeat tuple", "factorial(count(S))"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Needs a permutation/no-repeat sequence object and factorial theorem.",
        ),
        Chapter1Record(
            id="ch1_theorem_04_repeated_permutations",
            kind="theorem",
            source_section="1.3 Permutations",
            page_start=20,
            page_end=20,
            content=(
                "If n objects are divided into repeated classes of sizes n1, ..., nr, "
                "the number of distinguishable linear arrangements is n!/(n1!...nr!)."
            ),
            litex_proof_chain=[
                "Start from labeled permutations of n distinct copies.",
                "Define an equivalence relation that swaps objects inside each repeated class.",
                "Show every visible arrangement has n1!*...*nr! labeled representatives.",
                "Divide n! by the internal class permutation count.",
            ],
            litex_objects=["finite quotient", "equivalence classes", "factorial"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Needs quotient counting for indistinguishable objects.",
        ),
        Chapter1Record(
            id="ch1_theorem_05_combination_formula",
            kind="theorem",
            source_section="1.4 Combinations",
            page_start=21,
            page_end=22,
            content="The number of r-element subgroups of an n-element set is C(n,r)=n!/((n-r)!r!).",
            litex_proof_chain=[
                "Define the set of r-element subsets of an n-element finite set.",
                "Relate ordered r-tuples without repetition to unordered r-subsets.",
                "Show each subset has r! ordered listings.",
                "Divide n(n-1)...(n-r+1) by r!.",
            ],
            litex_objects=["{s power_set(S): count(s)=r}", "no-repeat tuple", "choose(n,r)"],
            status="blocked",
            blocker="blocked_by_infer_rule",
            notes="Current blocker: from s in power_set(S) and S finite, Litex does not infer s is finite for count(s).",
        ),
        Chapter1Record(
            id="ch1_theorem_06_pascal_identity",
            kind="theorem",
            source_section="1.4 Combinations",
            page_start=22,
            page_end=22,
            content="C(n,r)=C(n-1,r-1)+C(n-1,r).",
            litex_proof_chain=[
                "Fix one distinguished element of an n-element set.",
                "Partition r-subsets by whether they contain that element.",
                "Subsets containing it correspond to (r-1)-subsets of the remaining n-1 elements.",
                "Subsets not containing it correspond to r-subsets of the remaining n-1 elements.",
                "Use disjoint union count to add the two counts.",
            ],
            litex_objects=["fixed-cardinality subsets", "disjoint union", "count(union(A,B))"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Needs fixed-cardinality subset count and disjoint partition machinery.",
        ),
        Chapter1Record(
            id="ch1_theorem_07_binomial_theorem",
            kind="theorem",
            source_section="1.4 Combinations",
            page_start=23,
            page_end=24,
            content="(x+y)^n = sum_{k=0}^n C(n,k) x^k y^{n-k}.",
            litex_proof_chain=[
                "Induction route: prove base n=1.",
                "Assume the expansion for n-1.",
                "Multiply by (x+y) and split into two finite sums.",
                "Reindex the two sums.",
                "Use Pascal identity to combine coefficients.",
                "Combinatorial route: each term chooses which k of n factors contribute x.",
            ],
            litex_objects=["finite sum over k", "choose(n,k)", "polynomial equality", "induction on n"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Concrete polynomial identities are checkable; the general finite-sum theorem needs more support.",
        ),
        Chapter1Record(
            id="ch1_theorem_08_multinomial_coefficient",
            kind="theorem",
            source_section="1.5 Multinomial Coefficients",
            page_start=25,
            page_end=25,
            content=(
                "The number of divisions of n distinct items into r labeled groups of "
                "sizes n1,...,nr is n!/(n1!...nr!)."
            ),
            litex_proof_chain=[
                "Choose n1 items for group 1.",
                "Choose n2 items from the remaining items for group 2.",
                "Continue until all labeled groups are filled.",
                "Multiply the successive combination counts and simplify to n!/(n1!...nr!).",
            ],
            litex_objects=["labeled group tuple", "fixed-cardinality subsets", "multinomial coefficient"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Depends on combination formula and labeled finite partitions.",
        ),
        Chapter1Record(
            id="ch1_theorem_09_multinomial_theorem",
            kind="theorem",
            source_section="1.5 Multinomial Coefficients",
            page_start=26,
            page_end=27,
            content="The expansion of (x1+...+xr)^n is indexed by nonnegative n1+...+nr=n with multinomial coefficients.",
            litex_proof_chain=[
                "Expand the product as n choices of one variable among x1,...,xr.",
                "Group terms by how many times each variable is selected.",
                "Use the multinomial coefficient to count selections with fixed exponents.",
                "Sum over all nonnegative exponent vectors whose entries add to n.",
            ],
            litex_objects=["finite multi-index sum", "nonnegative exponent vectors", "multinomial coefficient"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Needs finite multi-index sums and multinomial coefficient interfaces.",
        ),
        Chapter1Record(
            id="ch1_theorem_10_positive_integer_solutions",
            kind="proposition",
            source_section="1.6 Integer Solutions",
            page_start=28,
            page_end=28,
            content="The number of positive integer vectors x1+...+xr=n is C(n-1,r-1).",
            litex_proof_chain=[
                "Line up n indistinguishable objects.",
                "Choose r-1 of the n-1 gaps as dividers.",
                "Map each divider choice to group sizes x1,...,xr.",
                "Map each positive solution back to its divider positions.",
                "Use the bijection to get C(n-1,r-1).",
            ],
            litex_objects=["positive solution set", "gap set with n-1 elements", "fixed-cardinality subsets", "bijection"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Needs integer-solution set counting and fixed-cardinality subset count.",
        ),
        Chapter1Record(
            id="ch1_theorem_11_nonnegative_integer_solutions",
            kind="proposition",
            source_section="1.6 Integer Solutions",
            page_start=28,
            page_end=28,
            content="The number of nonnegative integer vectors x1+...+xr=n is C(n+r-1,r-1).",
            litex_proof_chain=[
                "Transform a nonnegative solution x_i into a positive solution y_i=x_i+1.",
                "Then y1+...+yr=n+r.",
                "Use Proposition 6.1 on positive solutions of sum n+r.",
                "Translate back to obtain C(n+r-1,r-1).",
            ],
            litex_objects=["nonnegative solution set", "positive solution set", "bijection y_i=x_i+1"],
            status="blocked",
            blocker="blocked_by_stdlib",
            notes="Needs function/bijection between solution sets and stars-and-bars theorem.",
        ),
    ]


def classify_chapter1_problem(statement: str) -> tuple[list[str], list[str], str, str, str]:
    text = statement.lower()
    objects: list[str] = []
    chain: list[str] = []
    status = "translated"
    blocker = ""
    notes = "Heuristic route inferred from Chapter 1 methods; verify against the problem manually."

    def set_result(route: list[str], litex_objects: list[str], item_status: str, item_blocker: str, item_notes: str) -> None:
        nonlocal chain, objects, status, blocker, notes
        chain = route
        objects = litex_objects
        status = item_status
        blocker = item_blocker
        notes = item_notes

    if any(key in text for key in ["license plate", "area code", "die is rolled", "outcome sequence", "telephone"]):
        if any(key in text for key in ["no letter", "no number", "no digit", "without repetition", "not repeated", "no repetitions"]):
            set_result(
                [
                    "Identify each position of the sequence.",
                    "Use the book's staged no-repetition count: each later position has fewer available symbols.",
                    "Try to represent the actual outcomes as no-repeat tuples.",
                    "If no-repeat tuple support is missing, record the staged product as a proof fragment and mark the tuple bijection blocked.",
                ],
                ["no-repeat tuple", "finite symbol sets", "staged product"],
                "blocked",
                "blocked_by_stdlib",
                "Needs no-repeat finite sequence support to prove the outcome set itself.",
            )
        else:
            set_result(
                [
                    "Represent each independent position as a finite set.",
                    "Represent the full outcome as a tuple in cart(S1,...,Sk).",
                    "Use count(cart(...)) = product of the position counts.",
                    "Evaluate the resulting product.",
                ],
                ["finite sets for positions", "cart(S1,...,Sk)", "count(cart(...))"],
                "translated",
                "",
                (
                    "Candidate route for direct verification. Do not mark checkable until a "
                    "concrete .lit file is generated and run."
                ),
            )
    elif any(key in text for key in ["committee", "subcommittee", "hand", "poker", "chosen from", "choose", "subsets"]):
        set_result(
            [
                "Identify the underlying finite population set.",
                "Represent the choice as a fixed-cardinality subset.",
                "If there are restrictions, partition the subset family or subtract forbidden subset families.",
                "Apply the combination formula or inclusion-exclusion.",
            ],
            ["{s power_set(S): count(s)=k}", "fixed-cardinality subset count", "set partition"],
            "blocked",
            "blocked_by_infer_rule",
            "Known blocker: Litex currently needs better finite-subset/count inference for set-builder subsets.",
        )
    elif any(key in text for key in ["arrangement", "seated", "assigned", "assign", "ranking", "row", "linear", "order", "awards", "officers"]):
        if any(key in text for key in ["identical", "same nationality", "nationality", "letters", "blocks"]):
            set_result(
                [
                    "Start from labeled permutations.",
                    "Identify the internal swaps that do not change the visible outcome.",
                    "Use quotient counting by repeated classes.",
                    "Evaluate n! divided by the product of repeated-class factorials.",
                ],
                ["labeled permutation", "finite quotient", "repeated-class factorials"],
                "blocked",
                "blocked_by_stdlib",
                "Needs quotient counting for repeated/indistinguishable objects.",
            )
        else:
            set_result(
                [
                    "Represent the outcome as a no-repeat sequence or assignment.",
                    "Use staged choices: n choices, then n-1, and so on.",
                    "Prove a bijection between staged records and the source outcome object.",
                    "Evaluate the product.",
                ],
                ["no-repeat tuple", "permutation(S)", "staged product"],
                "blocked",
                "blocked_by_stdlib",
                "Needs permutation/no-repeat sequence support.",
            )
    elif any(key in text for key in ["expand", "binomial", "multinomial"]):
        set_result(
            [
                "Identify the polynomial expression to expand.",
                "For a concrete exponent, use algebraic normalization/equality chains.",
                "For a general exponent, use binomial or multinomial coefficient theorem.",
            ],
            ["polynomial expression", "coefficient formula", "finite sums"],
            "translated",
            "blocked_by_stdlib",
            "Concrete polynomial identities are often checkable; general finite-sum formulas need stdlib support.",
        )
    elif any(key in text for key in ["distributed", "distribute", "invest", "blackboards", "urns", "vectors", "integer"]):
        set_result(
            [
                "Represent the allocation or vector as integer variables x1,...,xr.",
                "Translate constraints into a sum equation and lower bounds.",
                "Shift variables if lower bounds are positive.",
                "Apply positive or nonnegative stars-and-bars.",
            ],
            ["integer solution set", "variable shift", "stars-and-bars bijection"],
            "blocked",
            "blocked_by_stdlib",
            "Needs integer-solution set counting and stars-and-bars theorem.",
        )
    elif any(key in text for key in ["path", "grid", "lattice"]):
        set_result(
            [
                "Represent each path as a word in moves R and U.",
                "Fix the number of R and U moves required.",
                "Count words with a fixed number of one move type using combinations.",
            ],
            ["binary word", "fixed-cardinality subset of move positions", "choose(n,k)"],
            "blocked",
            "blocked_by_stdlib",
            "Needs fixed-cardinality subset or fixed-weight word counting.",
        )
    else:
        set_result(
            [
                "Identify the finite outcome object described by the problem.",
                "Choose the relevant Chapter 1 counting principle: product, permutation, combination, multinomial coefficient, or stars-and-bars.",
                "Write the counted object before evaluating arithmetic.",
                "Run Litex on the object-level formulation and classify the first failure.",
            ],
            ["finite outcome set", "count(...)"],
            "translated",
            "blocked_by_formulation",
            "Manual classification needed.",
        )

    return chain, objects, status, blocker, notes


def extract_problem_records(chapter_lines: list[TextLine]) -> list[Chapter1Record]:
    section_titles = {
        "PROBLEMS": "problems",
        "THEORETICAL EXERCISES": "theoretical_exercises",
        "SELF-TEST PROBLEMS AND EXERCISES": "self_test",
    }
    section_indices: list[tuple[int, str]] = []
    for index, line in enumerate(chapter_lines):
        title = line.text.upper()
        if title in section_titles:
            section_indices.append((index, section_titles[title]))

    records: list[Chapter1Record] = []
    for section_position, (start_index, section_key) in enumerate(section_indices):
        end_index = (
            section_indices[section_position + 1][0]
            if section_position + 1 < len(section_indices)
            else len(chapter_lines)
        )
        section_lines = chapter_lines[start_index + 1 : end_index]
        item_starts: list[int] = []
        for index, line in enumerate(section_lines):
            if re.match(r"^[∗*]?\d+[.]\s+", line.text):
                item_starts.append(index)

        for item_position, item_start in enumerate(item_starts):
            item_end = item_starts[item_position + 1] if item_position + 1 < len(item_starts) else len(section_lines)
            item_lines = section_lines[item_start:item_end]
            if not item_lines:
                continue
            first_text = item_lines[0].text
            item_match = re.match(r"^(?P<star>[∗*]?)(?P<number>\d+)[.]\s+(?P<body>.*)", first_text)
            if item_match is None:
                continue
            number = item_match.group("number")
            body_lines = [item_match.group("body")] + [line.text for line in item_lines[1:]]
            content = normalize_problem_text(" ".join(body_lines))
            chain, objects, status, blocker, notes = classify_chapter1_problem(content)
            records.append(
                Chapter1Record(
                    id=f"ch1_{section_key}_{number.zfill(2)}",
                    kind="problem",
                    source_section=section_key,
                    page_start=item_lines[0].page,
                    page_end=item_lines[-1].page,
                    content=content,
                    litex_proof_chain=chain,
                    litex_objects=objects,
                    status=status,
                    blocker=blocker,
                    notes=notes,
                )
            )

    return records


def normalize_problem_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:?])", r"\1", text)
    return text.strip()


def chapter1_litex_records(lines: list[TextLine]) -> list[Chapter1Record]:
    chapter_lines = chapter_page_lines(lines, 1)
    return chapter1_theorem_records() + extract_problem_records(chapter_lines)


def render_chapter1_litex_markdown(records: list[Chapter1Record]) -> str:
    chunks = [
        "# Chapter 1 Theorems and Problems: Litex Proof Routes",
        "",
        "This output follows the theorem-to-litex boundary-probing workflow: preserve the book's proof route, name the counted object first, and mark missing Litex support as a blocker instead of replacing it with arithmetic only.",
        "",
    ]
    for record in records:
        chunks.extend(
            [
                f"## {record.id}",
                "",
                f"- kind: {record.kind}",
                f"- source_section: {record.source_section}",
                f"- pages: {record.page_start}-{record.page_end}",
                f"- status: {record.status}",
                f"- blocker: {record.blocker}",
                "",
                "定理/问题内容:",
                "",
                record.content,
                "",
                "可被 Litex 理解的证明链路:",
                "",
            ]
        )
        for index, step in enumerate(record.litex_proof_chain, start=1):
            chunks.append(f"{index}. {step}")
        chunks.extend(["", "Litex 对象/谓词候选:", ""])
        for obj in record.litex_objects:
            chunks.append(f"- `{obj}`")
        chunks.extend(["", "备注:", "", record.notes, ""])
    return "\n".join(chunks).rstrip() + "\n"


def render_markdown(records: list[TheoremRecord]) -> str:
    chunks = ["# Extracted Theorem-Like Results", ""]
    for record in records:
        heading = f"{record.label} {record.number}"
        if record.title:
            heading += f" {record.title}"
        chunks.extend(
            [
                f"## {heading}",
                "",
                f"- pages: {record.page_start}-{record.page_end}",
                "",
                "定理内容:",
                "",
                record.theorem_content or "(empty)",
                "",
                "证明链路:",
                "",
            ]
        )
        if record.proof_chain:
            for step_index, step in enumerate(record.proof_chain, start=1):
                chunks.append(f"{step_index}. {step}")
        else:
            chunks.append("- (未在自动提取块中找到显式 proof；请人工核对 PDF 附近页面。)")

        if record.extraction_notes:
            chunks.extend(["", "提取备注:", ""])
            for note in record.extraction_notes:
                chunks.append(f"- {note}")
        chunks.append("")

    return "\n".join(chunks).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract theorem/proposition/lemma/corollary content and proof chains from a PDF."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        default="A-First-Course-in-Probability (1).pdf",
        help="Path to the probability textbook PDF.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Write output to this file. Defaults to stdout.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--chapter1-litex",
        action="store_true",
        help=(
            "Extract Chapter 1 theorem/problem records and attach Litex-oriented "
            "proof routes based on the theorem-to-litex skill."
        ),
    )
    parser.add_argument(
        "--labels",
        default=",".join(DEFAULT_LABELS),
        help="Comma-separated heading labels to extract.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Only output the first N records, useful for quick checks.",
    )
    parser.add_argument(
        "--max-proof-steps",
        type=int,
        default=12,
        help="Maximum proof-chain sentences per result. Use 0 for all extracted steps.",
    )
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    lines = extract_lines(pdf_path)
    labels = tuple(label.strip() for label in args.labels.split(",") if label.strip())
    max_proof_steps = None if args.max_proof_steps == 0 else args.max_proof_steps

    if args.chapter1_litex:
        records = chapter1_litex_records(lines)
    else:
        records = parse_records(lines, labels, max_proof_steps)

    if args.limit is not None:
        records = records[: args.limit]

    if args.format == "json":
        output = json.dumps([asdict(record) for record in records], ensure_ascii=False, indent=2)
        output += "\n"
    elif args.chapter1_litex:
        output = render_chapter1_litex_markdown(records)
    else:
        output = render_markdown(records)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
