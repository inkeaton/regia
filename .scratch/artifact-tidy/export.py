#!/usr/bin/env python3
"""Build the anonymous submission archive from branch 1.0. For us only: not part of the artifact.

    python3 .scratch/artifact-tidy/export.py [--ref 1.0] [--out regia_paper.zip] [--pdf additional_material.pdf]

Reads the files from git, never from the working tree, so build output can't get in.
Fails, and writes nothing, if the zip is over 25 MB, if a file contains a string from
private-names.txt (one per line, next to this script, kept out of git), or if a text
this script adapts has changed on 1.0.
"""
import argparse, io, re, subprocess, sys, tarfile, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LIMIT = 25_000_000
ROOT = "regia_paper/"
EXCLUDE = ("science_game/demo_video/", "docs/")


def once(text, pattern, new, name):
    text, n = re.subn(pattern, new, text, flags=re.S | re.M)
    if n != 1:
        sys.exit(f"{name}: expected one match, found {n}: {pattern!r}. Update export.py.")
    return text


def adapt(files):
    """Remove mentions of what the zip leaves out, and links that need GitHub."""
    def edit(name, *rules):
        text = files[name].decode()
        for pattern, new in rules:
            text = once(text, pattern, new, name)
        files[name] = text.encode()

    edit("README.md",
         (r"^\[!\[CI\].*?\n\n", ""),
         (r"│   ├── minds/ ", "│   └── minds/ "),
         (r"^│   └── demo_video/[^\n]*\n", ""),
         (r"^├── docs/[^\n]*\n", ""),
         (r", the game design diagrams and the game art", " and the game art"),
         (r" \(tag `artifact-submitted`\)", ""))
    edit("NOTICE",
         (r"^Game design diagrams\n(?:  [^\n]*\n)+\n", ""),
         (r"^  The paper textures seen in the videos.*?as files\.\n", ""))
    edit("CHANGES.md",
         (r"The tag `artifact-submitted` is the artifact as it was submitted with the paper, except for the paper's supplementary PDF\. This file lists what has changed on branch `1\.0` since then\.",
          "This file lists what has changed since the artifact was submitted with the paper."),
         (r"\| Commit \|\n\|---\|---\|---\|", "|\n|---|---|"),
         (r"^- The demo videos and the snippet images[^\n]*\n", ""))
    # Commit hashes are searchable on GitHub: drop the column and the references.
    text = files["CHANGES.md"].decode()
    link = r"\[`[0-9a-f]{7}`\]\(\.\./\.\./commit/[0-9a-f]{7}\)"
    links = rf"{link}(?:, {link})*"
    text = re.sub(rf" \| {links} \|$", " |", text, flags=re.M)
    text = re.sub(rf" \({links}\)", "", text)
    files["CHANGES.md"] = text.encode()


def searchable(name, data):
    """The bytes to search: the file, and its text if it is compressed."""
    yield data
    if name.endswith(".xlsx"):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            yield from (z.read(i) for i in z.namelist())
    if name.endswith(".pdf"):
        for cmd in (["pdftotext", "-", "-"], ["pdfinfo", "-"]):
            yield subprocess.run(cmd, input=data, stdout=subprocess.PIPE, check=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="1.0", help="commit or tree to export")
    ap.add_argument("--out", type=Path, default=Path("regia_paper.zip"))
    ap.add_argument("--pdf", type=Path, help="additional_material.pdf to add")
    a = ap.parse_args()

    tar = subprocess.run(["git", "-C", HERE.parents[1], "archive", "--format=tar", a.ref],
                         stdout=subprocess.PIPE, check=True).stdout
    files, modes = {}, {}
    with tarfile.open(fileobj=io.BytesIO(tar)) as t:
        for m in t:
            if m.issym() or m.islnk():
                sys.exit(f"{m.name}: links are not supported")
            if m.isfile() and not m.name.startswith(EXCLUDE):
                files[m.name] = t.extractfile(m).read()
                modes[m.name] = 0o755 if m.mode & 0o100 else 0o644
    adapt(files)
    if a.pdf:
        files["additional_material.pdf"] = a.pdf.read_bytes()

    names_file = HERE / "private-names.txt"
    if not names_file.is_file():
        sys.exit(f"{names_file} is missing")
    private = [n.strip().lower().encode() for n in names_file.read_text().splitlines() if n.strip()]
    if not private:
        sys.exit(f"{names_file} is empty")
    hits = [(f, n.decode()) for f, d in files.items() for n in private
            if n in f.lower().encode() or any(n in s.lower() for s in searchable(f, d))]
    left = [f for f, d in files.items() if f.endswith(".md") and b"../../commit/" in d
            or f in ("README.md", "NOTICE", "CHANGES.md") and any(e in d for e in (b"demo_video", b"snippets references"))]
    for f, n in hits:
        print(f"PRIVATE  {f}: {n}")
    for f in left:
        print(f"STALE    {f} still mentions something left out")
    if hits or left:
        sys.exit(1)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(files):
            info = zipfile.ZipInfo(ROOT + f, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = (0o100000 | modes.get(f, 0o644)) << 16
            z.writestr(info, files[f], compresslevel=9)
        biggest = sorted(z.infolist(), key=lambda i: -i.compress_size)[:15]
    size = buf.tell()
    for i in biggest:
        print(f"{i.compress_size:>10,}  {i.filename}")
    print(f"{size:>10,}  total, {len(files)} files")
    if size > LIMIT:
        sys.exit(f"over the {LIMIT:,} byte limit; not written")
    a.out.write_bytes(buf.getvalue())
    print(f"wrote {a.out}")


main()
