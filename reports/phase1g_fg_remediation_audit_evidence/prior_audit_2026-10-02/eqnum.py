"""Reconstruct printed equation numbers from LaTeX (audit helper, independent of the audited code).

Counts numbered rows of equation / eqnarray / align / gather / multline (non-starred);
rows split on a top-level double backslash; nonumber / notag suppress; tag{} overrides.
Modes: flat (1,2,...; appendix letters), sec (section.n), with setcounter{equation}0 resets.
"""
import re
import sys

BS = "\\"


def strip_comments(s):
    out = []
    for line in s.split("\n"):
        i = 0
        cut = len(line)
        while i < len(line):
            if line[i] == BS:
                i += 2
                continue
            if line[i] == "%":
                cut = i
                break
            i += 1
        out.append(line[:cut])
    return "\n".join(out)


def expand_macros(s, macros):
    for k, v in macros.items():
        s = re.sub(re.escape(k) + r"(?![A-Za-z])", lambda m, v=v: v, s)
    return s


ENVS = "equation|eqnarray|align|gather|multline"
TOK = re.compile(
    r"\\(section|appendix)(?![A-Za-z])(\*?)"
    r"|\\begin\{(" + ENVS + r")(\*?)\}"
    r"|\\setcounter\{equation\}\{?0\}?"
)
ROWSPLIT = re.compile(r"\\\\(?![A-Za-z])")


INNER = re.compile(r"\\begin\{(cases|array|bmatrix|pmatrix|matrix|split|aligned|smallmatrix|subarray)\}(.*?)\\end\{\1\}", re.S)


def protect_inner(body):
    def rep(m):
        return m.group(0).replace(BS + BS, " ;; ")
    prev = None
    while prev != body:
        prev = body
        body = INNER.sub(rep, body)
    return body


def run(text, per_section=False, macros=None):
    text = strip_comments(text)
    k = text.find(BS + "begin{document}")
    if k >= 0:
        text = "\n" * text.count("\n", 0, k) + text[k:]
    if macros:
        text = expand_macros(text, macros)
    pos, sec, app, n, out = 0, 0, False, 0, []
    while True:
        m = TOK.search(text, pos)
        if not m:
            break
        if m.group(1) == "section":
            if not m.group(2):
                sec += 1
                if per_section or app:
                    n = 0
            pos = m.end()
            continue
        if m.group(1) == "appendix":
            app, sec, n = True, 0, 0
            pos = m.end()
            continue
        if m.group(0).startswith(BS + "setcounter"):
            n = 0
            pos = m.end()
            continue
        env, star = m.group(3), m.group(4)
        end = re.compile(r"\\end\{" + env + r"\*?\}").search(text, m.end())
        body = protect_inner(text[m.end():end.start()])
        pos = end.end()
        if star:
            continue
        if env in ("equation", "multline"):
            rows = [body]
        else:
            rows = ROWSPLIT.split(body)
            if len(rows) > 1 and rows[-1].strip() == "":
                rows = rows[:-1]
        line = text.count("\n", 0, m.start()) + 1
        for r in rows:
            if re.search(r"\\nonumber|\\notag", r):
                continue
            tag = re.search(r"\\tag\{([^}]*)\}", r)
            if tag:
                label = tag.group(1)
            else:
                n += 1
                if app:
                    label = f"{chr(64 + sec)}{n}"
                elif per_section:
                    label = f"{sec}.{n}"
                else:
                    label = str(n)
            lab = re.search(r"\\label\{([^}]*)\}", r)
            out.append((label, line, lab.group(1) if lab else "", " ".join(r.split())[:170]))
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    files = sys.argv[2:]
    text = "".join(open(f, encoding="latin-1").read() + "\n" for f in files)
    macros = {BS + "be": BS + "begin{equation}", BS + "ee": BS + "end{equation}",
              BS + "ba": BS + "begin{eqnarray}", BS + "ea": BS + "end{eqnarray}",
              BS + "beq": BS + "begin{equation}", BS + "eeq": BS + "end{equation}",
              BS + "bea": BS + "begin{eqnarray}", BS + "eea": BS + "end{eqnarray}"}
    for row in run(text, per_section=(mode == "sec"), macros=macros):
        print(*row, sep=" | ")
