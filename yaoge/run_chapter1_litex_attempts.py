#!/usr/bin/env python3
"""
Run every Chapter 1 Litex attempt and write structured logs.

The verifier can return process exit code 0 even when the Litex result is an
error, so this script classifies by the JSON payload printed by `litex -f`.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_LITEX_DIR = Path("yaoge/第一章定理与例题")
DEFAULT_MARKDOWN_LOG = DEFAULT_LITEX_DIR / "run_results.md"
DEFAULT_JSON_LOG = DEFAULT_LITEX_DIR / "run_results.json"


@dataclass
class LitexRunResult:
    file: str
    status: str
    process_returncode: int
    elapsed_seconds: float
    top_result: str
    top_error_type: str
    top_line: int | None
    top_message: str
    deepest_error_type: str
    deepest_line: int | None
    deepest_message: str
    deepest_stmt: str
    stdout: str
    stderr: str
    parsed_output: dict[str, Any] | None


def parse_json_payload(stdout: str) -> dict[str, Any] | None:
    text = stdout.strip()
    if not text:
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def previous_error_chain(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not payload:
        return []

    chain: list[dict[str, Any]] = []
    current: Any = payload
    while isinstance(current, dict):
        if current.get("result") == "error" or current.get("error_type"):
            chain.append(current)
        current = current.get("previous_error")
    return chain


def compact_text(value: Any, max_len: int = 220) -> str:
    if value is None:
        return ""
    text = str(value).replace("\n", "\\n")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def classify_status(payload: dict[str, Any] | None, returncode: int) -> str:
    if payload is None:
        return "unparsed"
    if payload.get("result") == "success":
        return "success"
    if payload.get("result") == "error" or payload.get("error_type"):
        return "error"
    if returncode != 0:
        return "process_error"
    return "unknown"


def run_one_file(path: Path, litex_bin: str, timeout_seconds: float) -> LitexRunResult:
    started = datetime.now()
    try:
        completed = subprocess.run(
            [litex_bin, "-f", str(path)],
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        elapsed = (datetime.now() - started).total_seconds()
        payload = parse_json_payload(completed.stdout)
        chain = previous_error_chain(payload)
        deepest = chain[-1] if chain else {}
        status = classify_status(payload, completed.returncode)
        return LitexRunResult(
            file=str(path),
            status=status,
            process_returncode=completed.returncode,
            elapsed_seconds=elapsed,
            top_result=str(payload.get("result", "")) if payload else "",
            top_error_type=str(payload.get("error_type", "")) if payload else "",
            top_line=payload.get("line") if payload else None,
            top_message=str(payload.get("message", "")) if payload else "",
            deepest_error_type=str(deepest.get("error_type", "")),
            deepest_line=deepest.get("line"),
            deepest_message=str(deepest.get("message", "")),
            deepest_stmt=str(deepest.get("stmt", "")),
            stdout=completed.stdout,
            stderr=completed.stderr,
            parsed_output=payload,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = (datetime.now() - started).total_seconds()
        return LitexRunResult(
            file=str(path),
            status="timeout",
            process_returncode=-1,
            elapsed_seconds=elapsed,
            top_result="",
            top_error_type="TimeoutExpired",
            top_line=None,
            top_message=f"Timed out after {timeout_seconds} seconds.",
            deepest_error_type="TimeoutExpired",
            deepest_line=None,
            deepest_message=f"Timed out after {timeout_seconds} seconds.",
            deepest_stmt="",
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            parsed_output=None,
        )


def collect_lit_files(litex_dir: Path) -> list[Path]:
    return sorted(path for path in litex_dir.glob("*.lit") if path.is_file())


def status_counts(results: list[LitexRunResult]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for result in results:
        counts[result.status] = counts.get(result.status, 0) + 1
    return counts


def render_markdown(results: list[LitexRunResult], litex_bin: str, litex_dir: Path) -> str:
    generated_at = datetime.now().isoformat(timespec="seconds")
    counts = status_counts(results)
    lines = [
        "# Chapter 1 Litex Run Results",
        "",
        f"- generated_at: `{generated_at}`",
        f"- litex_bin: `{litex_bin}`",
        f"- litex_dir: `{litex_dir}`",
        f"- total_files: `{len(results)}`",
        f"- success: `{counts.get('success', 0)}`",
        f"- error: `{counts.get('error', 0)}`",
        f"- timeout: `{counts.get('timeout', 0)}`",
        f"- unparsed: `{counts.get('unparsed', 0)}`",
        "",
        "| # | file | status | top error | deepest error | line | message |",
        "|---:|---|---|---|---|---:|---|",
    ]
    for index, result in enumerate(results, start=1):
        path = Path(result.file)
        display = path.name
        top_error = result.top_error_type or result.top_result
        deepest_error = result.deepest_error_type
        line = result.deepest_line if result.deepest_line is not None else result.top_line
        message = result.deepest_message or result.top_message or result.stderr
        lines.append(
            "| "
            + " | ".join(
                [
                    str(index),
                    f"`{display}`",
                    f"`{result.status}`",
                    f"`{compact_text(top_error, 80)}`",
                    f"`{compact_text(deepest_error, 80)}`",
                    str(line or ""),
                    compact_text(message),
                ]
            )
            + " |"
        )
    lines.append("")
    lines.append("## Raw Output")
    lines.append("")
    lines.append("Full stdout/stderr and parsed JSON are stored in `run_results.json`.")
    lines.append("")
    return "\n".join(lines)


def write_logs(results: list[LitexRunResult], markdown_log: Path, json_log: Path, litex_bin: str, litex_dir: Path) -> None:
    markdown_log.parent.mkdir(parents=True, exist_ok=True)
    json_log.parent.mkdir(parents=True, exist_ok=True)
    markdown_log.write_text(render_markdown(results, litex_bin, litex_dir), encoding="utf-8")
    json_log.write_text(
        json.dumps([asdict(result) for result in results], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Chapter 1 .lit files and write logs.")
    parser.add_argument(
        "--litex-dir",
        type=Path,
        default=DEFAULT_LITEX_DIR,
        help="Directory containing Chapter 1 .lit files.",
    )
    parser.add_argument(
        "--litex-bin",
        default=shutil.which("litex") or "litex",
        help="Litex executable path.",
    )
    parser.add_argument(
        "--markdown-log",
        type=Path,
        default=DEFAULT_MARKDOWN_LOG,
        help="Markdown summary log path.",
    )
    parser.add_argument(
        "--json-log",
        type=Path,
        default=DEFAULT_JSON_LOG,
        help="JSON detailed log path.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="Per-file timeout in seconds.",
    )
    args = parser.parse_args()

    files = collect_lit_files(args.litex_dir)
    if not files:
        raise SystemExit(f"No .lit files found in {args.litex_dir}")

    results = [run_one_file(path, args.litex_bin, args.timeout) for path in files]
    write_logs(results, args.markdown_log, args.json_log, args.litex_bin, args.litex_dir)
    counts = status_counts(results)
    print(
        " ".join(
            [
                f"total={len(results)}",
                f"success={counts.get('success', 0)}",
                f"error={counts.get('error', 0)}",
                f"timeout={counts.get('timeout', 0)}",
                f"unparsed={counts.get('unparsed', 0)}",
                f"markdown_log={args.markdown_log}",
                f"json_log={args.json_log}",
            ]
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
