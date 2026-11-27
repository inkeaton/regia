#!/usr/bin/env python3
"""Rename every Diagnostic code and Trace code from one reviewed mapping.

One-off migration for the *Readable Diagnostic and Trace codes* map
(`.scratch/diagnostic-codes/map.md`). The rules it enforces are decided in
`issues/01-the-shape-of-a-code.md`; this script never invents a name.

Modes:

    inventory  every distinct code in the live files, where it appears, and
               the check-list line that defines it
    check      dry run: validate the mapping, report unmapped codes, unused
               entries and replacements per file; any problem fails the run
    apply      run `check`, then rewrite the live files in place

Options:

    --root DIR      repository root (default: two levels above this script)
    --mapping FILE  mapping CSV with columns `old,new`
                    (default: mapping.csv next to this script)
    --partial       `check` only: a code found but not mapped is counted, not
                    a failure, so one batch of names can be checked alone

Python 3, standard library only.
"""

import argparse
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent

# A code in the old shape, as a whole token. `_` is a word character, so a
# code already in the new shape (`R01_11-...`) never matches.
OLD_CODE = re.compile(r"\b[RT]\d{4}\b")
# A word holding something that looks like an old code but isn't a whole
# token (`xR0111`, `R01110`), and codes written with placeholders (`R01xx`).
NEAR_MISS = re.compile(r"\w*[RT]\d{4}\w*")
WILDCARD = re.compile(r"\b[RT]\d{2}[xX]{2}\b")
# A range written between two codes (`R0112` to `R0115`, `T2801`–`T2803`).
# Both ends are renamed, but the sentence may need rewording.
RANGE = re.compile(r"\b[RT]\d{4}`?\s*(?:–|—|-|to)\s*`?[RT]\d{4}\b")
NEW_CODE = re.compile(r"^([RT])(\d{2})_(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
OLD_CODE_EXACT = re.compile(r"^([RT])(\d{2})(\d{2})$")
# A code inside a URL is reported, never rewritten. (A hash can't hold a
# whole-token code: `R` and `T` aren't hex digits.)
URL = re.compile(r"\w+://\S+")
# The line in a chapter's check list (or Trace code list) that defines a code.
# Only the code's own chapter defines it (`R1301` in chapter 13), at its first
# such line: other chapters quote check lists (27) or summarise them in a
# table (34), and a later bullet may start with the code to say more about it.
DEFINITION = re.compile(r"^\s*-\s+`([RT]\d{4})`")
CHAPTER = re.compile(r"^docs/spec/(\d{2})-[^/]+\.md$")

MAX_WORDS = 4
SOFT_MAX_CHARS = 30

# Where live docs keep codes (issues/01, "The migration"). `.scratch` tickets
# count only when open, and this effort's own tickets are left alone: they
# quote old codes on purpose.
LIVE_TREES = ["docs/spec", "docs/guide", "docs/showcase", "docs/adr"]
LIVE_FILES = ["GLOSSARY.md"]
TEXT_SUFFIXES = {".md", ".regia", ".regin", ".trace", ".csv", ".txt"}
OWN_EFFORT = ".scratch/diagnostic-codes"


def ticket_is_open(path):
    """Whether a `.scratch` ticket's `Status:` line says `open`."""
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip() == "open"
    return False


def live_files(root):
    """The files the migration rewrites, as paths relative to `root`."""
    found = []
    for tree in LIVE_TREES:
        base = root / tree
        if base.is_dir():
            found += [p for p in base.rglob("*") if p.is_file()]
    found += [root / f for f in LIVE_FILES if (root / f).is_file()]
    scratch = root / ".scratch"
    if scratch.is_dir():
        for ticket in scratch.glob("*/issues/*.md"):
            rel = ticket.relative_to(root).as_posix()
            if not rel.startswith(OWN_EFFORT + "/") and ticket_is_open(ticket):
                found.append(ticket)
    skipped = [p for p in found if p.suffix not in TEXT_SUFFIXES]
    if skipped:
        names = ", ".join(sorted(p.relative_to(root).as_posix() for p in skipped))
        sys.exit(f"error: unexpected file type in the live set: {names}")
    return sorted(p.relative_to(root) for p in found)


def read(root, rel):
    # `newline=""` keeps line endings exactly as they are on disk.
    with open(root / rel, encoding="utf-8", newline="") as f:
        return f.read()


def scan(root, files):
    """Every code occurrence, and every suspicious token.

    Returns `(uses, suspects, guarded)`: `uses` maps a code to its `(file,
    line, is_definition, text)` occurrences; `suspects` lists `(file, line,
    token, reason)` for a person to check. A code inside a URL is a suspect,
    not a use, and its `(file, line, column)` is in `guarded`: it is never
    rewritten.
    """
    uses = defaultdict(list)
    suspects = []
    guarded = set()
    for rel in files:
        path = rel.as_posix()
        for number, line in enumerate(read(root, rel).splitlines(), start=1):
            urls = [m.span() for m in URL.finditer(line)]
            for m in OLD_CODE.finditer(line):
                if any(a <= m.start() < b for a, b in urls):
                    suspects.append((path, number, m.group(), "inside a URL, left as is"))
                    guarded.add((path, number, m.start()))
                    continue
                c = CHAPTER.match(path)
                d = DEFINITION.match(line)
                defines = bool(
                    c and d and d.group(1) == m.group() and c.group(1) == m.group()[1:3]
                ) and not any(o[2] for o in uses[m.group()])
                uses[m.group()].append((path, number, defines, line.strip()))
            for m in NEAR_MISS.finditer(line):
                if not OLD_CODE.fullmatch(m.group()):
                    suspects.append(
                        (path, number, m.group(), "not a whole token, left as is")
                    )
            for m in WILDCARD.finditer(line):
                suspects.append((path, number, m.group(), "a wildcard, left as is"))
            for m in RANGE.finditer(line):
                suspects.append(
                    (path, number, m.group(), "a range: both ends renamed, reword it")
                )
    return uses, suspects, guarded


def load_mapping(path):
    """Read and validate the mapping. Returns `(mapping, problems)`."""
    problems = []
    mapping = {}
    names = {}
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))
    if not rows or [c.strip() for c in rows[0]] != ["old", "new"]:
        return {}, [f"{path}: the first row must be `old,new`"]
    for n, row in enumerate(rows[1:], start=2):
        if not any(c.strip() for c in row):
            continue
        if len(row) != 2:
            problems.append(f"line {n}: expected 2 columns, found {len(row)}")
            continue
        old, new = (c.strip() for c in row)
        o = OLD_CODE_EXACT.match(old)
        m = NEW_CODE.match(new)
        if not o:
            problems.append(f"line {n}: `{old}` is not an old code (`R0111`)")
            continue
        if not m:
            problems.append(
                f"line {n}: `{new}` doesn't match `[RT]NN_NN-kebab-name`"
            )
            continue
        if o.groups() != m.groups()[:3]:
            problems.append(f"line {n}: `{new}` doesn't keep the number of `{old}`")
        name = m.group(4)
        if len(name.split("-")) > MAX_WORDS:
            problems.append(f"line {n}: `{name}` has more than {MAX_WORDS} words")
        if len(name) > SOFT_MAX_CHARS:
            print(f"warning: line {n}: `{name}` is over {SOFT_MAX_CHARS} characters")
        if old in mapping:
            problems.append(f"line {n}: `{old}` is mapped twice")
        if name in names:
            problems.append(
                f"line {n}: name `{name}` is already used by `{names[name]}`"
            )
        mapping[old] = new
        names.setdefault(name, old)
    return mapping, problems


def print_files(files):
    print(f"Live files ({len(files)}):")
    for rel in files:
        print(f"  {rel.as_posix()}")
    print()


def print_suspects(suspects):
    if not suspects:
        return
    print(f"Check by hand ({len(suspects)}):")
    for path, line, token, reason in suspects:
        print(f"  {path}:{line}: `{token}` ({reason})")
    print()


def inventory(root, files):
    uses, suspects, _ = scan(root, files)
    print_files(files)
    print(f"Codes ({len(uses)}). `*` marks the line that defines the code.")
    print()
    for code in sorted(uses, key=lambda c: (c[0], c[1:])):
        occurrences = uses[code]
        definitions = [o for o in occurrences if o[2]]
        print(code)
        if not definitions:
            print("  ! defined in no check list")
        elif len(definitions) > 1:
            print(f"  ! defined in {len(definitions)} places")
        for path, line, defines, text in definitions:
            print(f"  * {path}:{line}: {text}")
        for path, line, defines, _ in occurrences:
            if not defines:
                print(f"    {path}:{line}")
        print()
    print_suspects(suspects)


def check(root, files, mapping_path, partial=False):
    """Dry run. Returns whether the mapping and the files are clean.

    With `partial`, codes found but not mapped are only counted.
    """
    print_files(files)
    if not mapping_path.is_file():
        print(f"error: no mapping at {mapping_path}")
        return False
    mapping, problems = load_mapping(mapping_path)
    uses, suspects, _ = scan(root, files)

    unmapped = sorted(set(uses) - set(mapping))
    unused = sorted(set(mapping) - set(uses))
    if partial:
        print(f"partial: {len(unmapped)} codes found are not mapped yet")
        print()
    else:
        problems += [
            f"`{c}` is found but not mapped (first at {uses[c][0][0]}:{uses[c][0][1]})"
            for c in unmapped
        ]
    problems += [f"`{c}` is mapped but never found" for c in unused]

    counts = defaultdict(int)
    for code, occurrences in uses.items():
        if code in mapping:
            for path, *_ in occurrences:
                counts[path] += 1
    print(f"Replacements per file ({sum(counts.values())} in all):")
    for path in sorted(counts):
        print(f"  {counts[path]:5}  {path}")
    print()
    print_suspects(suspects)

    if problems:
        print(f"Problems ({len(problems)}):")
        for p in problems:
            print(f"  {p}")
        return False
    print("check: clean")
    return True


def apply(root, files, mapping_path):
    if not check(root, files, mapping_path):
        sys.exit("apply: check failed, nothing was rewritten")
    mapping, _ = load_mapping(mapping_path)
    _, _, guarded = scan(root, files)
    changed = 0
    for rel in files:
        path = rel.as_posix()
        text = read(root, rel)
        out = []
        for number, line in enumerate(text.splitlines(keepends=True), start=1):

            def rename(m, number=number):
                if (path, number, m.start()) in guarded:
                    return m.group()
                return mapping[m.group()]

            out.append(OLD_CODE.sub(rename, line))
        new = "".join(out)
        if new != text:
            with open(root / rel, "w", encoding="utf-8", newline="") as f:
                f.write(new)
            changed += 1
    print(f"apply: rewrote {changed} files")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("mode", choices=["inventory", "check", "apply"])
    parser.add_argument("--root", type=Path, default=HERE.parent.parent)
    parser.add_argument("--mapping", type=Path, default=HERE / "mapping.csv")
    parser.add_argument("--partial", action="store_true")
    args = parser.parse_args()
    if args.partial and args.mode != "check":
        parser.error("--partial works with `check` only")
    root = args.root.resolve()
    files = live_files(root)
    if args.mode == "inventory":
        inventory(root, files)
    elif args.mode == "check":
        if not check(root, files, args.mapping, args.partial):
            sys.exit(1)
    else:
        apply(root, files, args.mapping)


if __name__ == "__main__":
    main()
