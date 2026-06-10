#!/usr/bin/env python3
"""
check_notebooks.py - sanity-check Jupyter notebooks before they go live.

For every code cell it:
  1. compiles the Python (the authoritative check) to catch SyntaxErrors, and
  2. flags the specific corruption that Colab's "Save to GitHub" keeps
     introducing: a multi-line docstring glued onto the next line with a
     dropped quote -- the closing triple-quote becomes two quotes followed
     by spaces and the next line of code on the SAME line, e.g. a line that
     ends `...PyTorch."" <spaces> return ...` (two quotes + glued code)
     instead of a proper closing triple-quote on its own line followed by
     the next statement. That is a SyntaxError.

Usage
-----
  python check_notebooks.py                     # all *.ipynb in the current dir
  python check_notebooks.py notebooks           # all *.ipynb directly under notebooks/
  python check_notebooks.py -r notebooks        # recurse into sub-folders
  python check_notebooks.py a.ipynb b.ipynb     # specific notebooks

Exit code: 0 = all clean, 1 = problems found (so it works in CI / a git hook).
"""
import sys, os, re, json, glob, argparse

# A docstring close that lost a quote ("" instead of """) and was glued to code:
# two quotes NOT flanked by another quote, then >=2 spaces, then non-space.
MANGLED = re.compile(r'(?<!")""(?!")[ \t]{2,}\S')

# Prefer IPython's real input transformer (turns !shell, %magic, %%cellmagic,
# `x = !ls`, etc. into valid Python) so we only flag GENUINE syntax errors.
try:
    from IPython.core.inputtransformer2 import TransformerManager
    _TM = TransformerManager()
    def to_python(src):
        return _TM.transform_cell(src)
except Exception:                              # fallback: blank out magic/shell lines
    import re as _re
    _MAGIC = _re.compile(r'^(\s*)([!%?]|\w+\s*=\s*[!%])')
    def to_python(src):
        out = []
        for line in src.split("\n"):
            m = _MAGIC.match(line)
            out.append((m.group(1) + "pass") if m else line)
        return "\n".join(out)

def is_cell_magic(src):
    for line in src.split("\n"):
        if line.strip() == "":
            continue
        return line.lstrip().startswith("%%")   # %%bash, %%html, %%writefile, ...
    return False

def looks_like_markdown(src):
    """Some notebooks keep markdown (``` fenced blocks, prose) in *code* cells.
    Those aren't executable Python; a bare ``` fence is the giveaway."""
    return any(line.lstrip().startswith("```") for line in src.split("\n"))

def check_cell(cell_idx, src):
    """Return a list of problem strings for one code cell."""
    problems = []
    # 1) mangled-docstring heuristic (friendly, specific message)
    for ln, line in enumerate(src.split("\n"), 1):
        if MANGLED.search(line):
            problems.append("cell %d, line %d: docstring looks glued to the next "
                            "line / missing a quote -> %s"
                            % (cell_idx, ln, line.strip()[:70]))
    # 2) authoritative: does the Python compile? (after IPython transforms;
    #    cell-magic cells like %%bash aren't Python, so skip those.)
    if is_cell_magic(src) or looks_like_markdown(src):
        return problems
    try:
        compile(to_python(src), "<cell %d>" % cell_idx, "exec")
    except SyntaxError as e:
        msg = "cell %d, line %s: SyntaxError: %s" % (cell_idx, e.lineno, e.msg)
        if not any(("cell %d," % cell_idx) in p and "line %s:" % e.lineno in p for p in problems):
            problems.append(msg)
    return problems

def check_notebook(path):
    try:
        nb = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        return ["could not read/parse: %s" % e]
    problems = []
    for i, c in enumerate(nb.get("cells", [])):
        if c.get("cell_type") != "code":
            continue
        problems += check_cell(i, "".join(c.get("source", [])))
    return problems

def collect(args, recursive):
    paths = []
    targets = args or ["."]
    for t in targets:
        if os.path.isdir(t):
            pat = os.path.join(t, "**", "*.ipynb") if recursive else os.path.join(t, "*.ipynb")
            paths += glob.glob(pat, recursive=recursive)
        else:
            paths.append(t)
    # skip checkpoints
    return sorted(p for p in paths if ".ipynb_checkpoints" not in p)

def main():
    ap = argparse.ArgumentParser(description="Compile code cells and flag mangled docstrings.")
    ap.add_argument("paths", nargs="*", help="notebook files and/or directories (default: .)")
    ap.add_argument("-r", "--recursive", action="store_true", help="recurse into sub-directories")
    a = ap.parse_args()

    nbs = collect(a.paths, a.recursive)
    if not nbs:
        print("No .ipynb files found."); return 0

    total_problems = 0
    for path in nbs:
        probs = check_notebook(path)
        name = os.path.relpath(path)
        if probs:
            total_problems += len(probs)
            print("FAIL  %s  (%d issue%s)" % (name, len(probs), "" if len(probs) == 1 else "s"))
            for p in probs:
                print("        - " + p)
        else:
            print("ok    %s" % name)

    print("-" * 60)
    if total_problems:
        print("%d problem(s) across %d notebook(s). Fix before publishing." % (total_problems, len(nbs)))
        return 1
    print("All %d notebook(s) clean." % len(nbs))
    return 0

if __name__ == "__main__":
    sys.exit(main())
