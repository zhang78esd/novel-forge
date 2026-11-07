# -*- coding: utf-8 -*-
"""Check the RIA++ contract for every capability card and all SKILL.md references."""
import pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[2]
skill = root / "SKILL.md"
errors = []

if not skill.exists():
    errors.append("SKILL.md missing")
else:
    text = skill.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append("SKILL.md: missing frontmatter")
    else:
        front = text.split("---", 2)[1]
        for key in ("name:", "description:"):
            if key not in front:
                errors.append("SKILL.md: missing %s in frontmatter" % key)
    for ref in sorted(set(re.findall(r"references/[\w\-./]+\.md", text))):
        if not (root / ref).exists():
            errors.append("broken ref in SKILL.md: %s" % ref)

cap_dir = root / "references" / "capabilities"
caps = sorted(cap_dir.glob("*.md")) if cap_dir.is_dir() else []
if len(caps) != 15:
    errors.append("expected 15 capability cards, found %d" % len(caps))

sections = ("## R \u2014", "## I \u2014", "## A1 \u2014",
            "## A2 \u2014", "## E \u2014", "## B \u2014")
for p in caps:
    t = p.read_text(encoding="utf-8")
    missing = [s for s in sections if s not in t]
    if missing:
        errors.append("%s missing sections: %s" % (p.name, ", ".join(missing)))

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS: %d capability cards, RIA++ six sections complete, all SKILL.md refs resolve" % len(caps))
