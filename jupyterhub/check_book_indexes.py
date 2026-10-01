"""Check the book index, the sidebar and the served pages against notebooks2.0.txt.

Usage:

    python3 jupyterhub/check_book_indexes.py                     # source-level checks
    python3 jupyterhub/check_book_indexes.py http://localhost:3001   # + HTTP checks

What is verified:

  1. every ``file:`` in myst.yml (project.toc) exists in the repo
  2. every notebook listed in notebooks2.0.txt is present in myst.yml and in _toc.yml,
     in the same order, and the two agree
  3. every link of the 0-Index.ipynb landing page resolves
  4. the sidebar titles in myst.yml are exactly the section names of notebooks2.0.txt
  5. the generated sections/*.md pages exist, carry the section name as their H1 and
     list exactly that section's notebooks, linking to the slugs the theme generates
  6. (with a URL) the site answers 200 on the landing page, on every section page and on
     every page slug, and the built sidebar exposes the same section/notebook names

Exit code is non-zero if any check fails.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT = os.path.join(ROOT, "notebooks2.0.txt")
MYST = os.path.join(ROOT, "myst.yml")
TOC = os.path.join(ROOT, "_toc.yml")
INDEX = os.path.join(ROOT, "0-Index.ipynb")

# slug rules and section file names come from the generator, so there is one definition
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_index import myst_slug, section_file  # noqa: E402  (needs ROOT above)

failures = []
notes = []

# deliberate differences between notebooks2.0.txt and what the repo actually ships
# (both handled by jupyterhub/build_index.py: RENAMES/EXTRA)
# typos in the txt: the sidebar shows the corrected name
TITLE_FIX = {
    "lphaPept.ipynb": "AlphaPept.ipynb",          # AEmergingComputationalPlatformsPipelines/lphaPept
    "Pipelinesi/Modeling_Protein_Ligand_Interactions.ipynb": "Modeling_Protein_Ligand_Interactions.ipynb",
}
# the file was renamed in the repo, but the panel keeps the name written in the txt
FILE_FIX = {
    "PyOpenMS_Task1_Peaks.ipynb": "PyOpenMS_Peaks.ipynb",
    "dreams_beer_profiler_workshop.ipynb": "dreams_beer_profiler_workshop.ipynb",  # moved dir only
}
# notebooks2.0.txt only mentions these as annotations of the combined Stats notebook
EXTRA_SHIPPED = {
    "Stats_Untargeted_Metabolomics_python_part1.ipynb",
    "Stats_Untargeted_Metabolomics_python_part2.ipynb",
}


def check(ok, message):
    print(("  OK   " if ok else "  FAIL ") + message)
    if not ok:
        failures.append(message)
    return ok


def parse_txt():
    """Section names and notebook paths exactly as written in notebooks2.0.txt.

    The same path can appear on several lines (the combined Stats notebook is listed once
    per absorbed part), so basenames are de-duplicated while keeping the first occurrence.
    """
    sections, cur = [], None
    for line in open(TXT, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("- "):
            cur = {"name": line[2:].strip(), "notebooks": []}
            sections.append(cur)
            continue
        m = re.match(r"^(.+?\.ipynb)\s*(?:-\s*(.+?))?$", line)
        if m and cur is not None:
            base = os.path.basename(m.group(1).strip())
            if base not in cur["notebooks"]:
                cur["notebooks"].append(base)
    return sections


def get(url, timeout=20):
    with urllib.request.urlopen(url, timeout=timeout) as resp:
        return resp.status, resp.read().decode("utf-8", "replace")


def ast_links(node, out=None):
    """Collect every link target from a MyST .json payload (type: link -> url)."""
    if out is None:
        out = []
    if isinstance(node, dict):
        if node.get("type") == "link" and node.get("url"):
            out.append(node["url"])
        for v in node.values():
            ast_links(v, out)
    elif isinstance(node, list):
        for v in node:
            ast_links(v, out)
    return out


def main():
    base = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else None
    txt_sections = parse_txt()
    myst = yaml.safe_load(open(MYST, encoding="utf-8"))
    toc = yaml.safe_load(open(TOC, encoding="utf-8"))
    md = "".join(json.load(open(INDEX, encoding="utf-8"))["cells"][1]["source"])

    print("notebooks2.0.txt: %d sections, %d notebooks"
          % (len(txt_sections), sum(len(s["notebooks"]) for s in txt_sections)))

    print("\n[1] myst.yml (sidebar source) - every referenced file exists")
    entries = [e for e in myst["project"]["toc"] if "file" in e]
    children = [c for e in myst["project"]["toc"] for c in e.get("children", [])]
    check(all(os.path.exists(e["file"]) for e in entries + children),
          "%d file entries exist" % (len(entries) + len(children)))

    print("\n[2] myst.yml vs _toc.yml vs notebooks2.0.txt")
    myst_secs = [(e["title"], [(c["title"], c["file"]) for c in e.get("children", [])])
                 for e in myst["project"]["toc"] if "children" in e]
    toc_secs = [(p["caption"], [os.path.basename(c if isinstance(c, str) else c["file"])
                                for c in p["chapters"]]) for p in toc["parts"]]
    expected_secs = [s["name"] for s in txt_sections]
    expected = set()
    for s in txt_sections:
        # sidebar titles must match notebooks2.0.txt verbatim (minus the extension),
        # but correct obvious typos in the title
        for b in s["notebooks"]:
            expected.add(os.path.splitext(TITLE_FIX.get(b, b))[0])
    expected |= {os.path.splitext(x)[0] for x in EXTRA_SHIPPED}
    shipped = {t for _, c in myst_secs for t, _ in c}
    # every title must point at the file the txt name is expected to resolve to
    wrong_file = [t for _, c in myst_secs for t, f in c
                  if os.path.basename(f) != FILE_FIX.get(t + ".ipynb", t + ".ipynb")]

    check([s for s, _ in myst_secs] == expected_secs,
          "sidebar sections == notebooks2.0.txt sections")
    check([s for s, _ in toc_secs] == expected_secs,
          "_toc.yml sections == notebooks2.0.txt sections")
    check(len(shipped) == len(expected),
          "sidebar has %d notebooks (expected %d)" % (len(shipped), len(expected)))
    missing = sorted(expected - shipped)
    extra = sorted(shipped - expected)
    check(not missing, "every notebooks2.0.txt notebook is in the sidebar"
          + ("" if not missing else " - missing: %s" % missing))
    check(not extra, "sidebar has no notebook outside notebooks2.0.txt"
          + ("" if not extra else " - extra: %s" % extra))
    check(not wrong_file, "every title points at the file notebooks2.0.txt resolves to"
          + ("" if not wrong_file else " - wrong: %s" % wrong_file))
    for src, dst in sorted(TITLE_FIX.items()):
        if os.path.splitext(dst)[0] in shipped:
            notes.append("%s: the txt path is a typo, the panel shows %s"
                         % (src, os.path.splitext(dst)[0]))
    for src, dst in sorted(FILE_FIX.items()):
        if os.path.splitext(src)[0] in shipped:
            notes.append("%s: the panel keeps the txt name, the file is %s" % (src, dst))
    for x in sorted(EXTRA_SHIPPED):
        notes.append("%s is shipped although the txt only names it as an annotation" % x)

    print("\n[3] 0-Index.ipynb landing page")
    links = re.findall(r"- \[([^\]]+)\]\(\./([^)]+)\)", md)
    check(len(links) == len(expected), "index lists %d bullets (expected %d)" % (len(links), len(expected)))
    broken = [t for _, t in links if not os.path.exists(t)]
    check(not broken, "all index links resolve" + ("" if not broken else " - broken: %s" % broken))
    for s in txt_sections:
        if ("## " + s["name"]) not in md:
            failures.append("index page is missing section %r" % s["name"])
    check(all(("## " + s["name"]) in md for s in txt_sections),
          "every section name is a heading on the index page")

    print("\n[4] README notebook index (Colab links)")
    try:
        readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
    except OSError as exc:
        readme = ""
        check(False, "README.md could not be read: %s" % exc)
    if readme:
        rows = re.findall(
            r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*\[!\[Open In Colab\]\([^)]+\)\]"
            r"\((https://colab\.research\.google\.com/[^)]+)\)\s*\|", readme)
        check(len(rows) == len(expected),
              "README lists %d notebooks with a Colab link (expected %d)" % (len(rows), len(expected)))
        names = {os.path.splitext(n)[0] for n, _, _ in rows}
        check(not (expected - names), "every notebook has a Colab row"
              + ("" if not (expected - names) else " - missing: %s" % sorted(expected - names)))
        bad_rel = [t for _, t, _ in rows if not os.path.exists(t)]
        check(not bad_rel, "every README notebook link points at an existing file"
              + ("" if not bad_rel else " - broken: %s" % bad_rel))
        bad_colab = [u for _, _, u in rows
                     if not u.startswith("https://colab.research.google.com/github/")]
        check(not bad_colab, "Colab links are well formed"
              + ("" if not bad_colab else " - bad: %s" % bad_colab[:2]))
        # the Colab target must be the file the sidebar serves
        mismatched = [n for n, t, u in rows
                      if not u.endswith("/blob/%s/%s" % ("master", t))]
        check(not mismatched, "each Colab link points at its notebook path on master"
              + ("" if not mismatched else " - off: %s" % mismatched[:3]))

    print("\n[5] sections/*.md - one clickable page per section")
    want_files = {os.path.basename(section_file(i, s))
                  for i, (s, _k) in enumerate(myst_secs)}
    for i, (sec, kids) in enumerate(myst_secs):
        rel = section_file(i, sec)
        path = os.path.join(ROOT, rel)
        if not check(os.path.exists(path), "%s exists" % rel):
            continue
        text = open(path, encoding="utf-8").read()
        h1 = re.search(r"^#\s+(.+)$", text, re.M)
        check(bool(h1) and h1.group(1).strip() == sec, "%s H1 is %r" % (rel, sec))
        listed = re.findall(r"^-\s+\[([^\]]+)\]\(\.\./([^/]+)/\)$", text, re.M)
        want = [(t, myst_slug(os.path.splitext(os.path.basename(f))[0])) for t, f in kids]
        check(listed == want,
              "%s lists its %d notebook%s with the theme slugs"
              % (rel, len(want), "" if len(want) == 1 else "s")
              + ("" if listed == want else " - got: %r" % (listed,)))
    stray = sorted(f for f in os.listdir(os.path.join(ROOT, "sections"))
                   if f.endswith(".md") and f not in want_files)
    check(not stray, "no stale section pages" + ("" if not stray else " - %s" % stray))

    if base:
        print("\n[6] served site: %s" % base)
        try:
            status, html = get(base + "/")
            check(status == 200, "GET / -> %s" % status)
            check("root" in html.lower(), "landing page returns the book app shell")
        except (urllib.error.URLError, OSError) as exc:
            check(False, "GET / failed: %s" % exc)
            html = ""

        print("\n[7] served sidebar (config.json) vs notebooks2.0.txt")
        try:
            status, cfg_raw = get(base + "/config.json")
            cfg = json.loads(cfg_raw) if status == 200 else {}
        except (urllib.error.URLError, OSError, ValueError) as exc:
            cfg, status = {}, "error: %s" % exc
        if cfg:
            proj = (cfg.get("projects") or [{}])[0]
            pages = proj.get("pages") or []

            def titles(node, out):
                if isinstance(node, list):
                    for n in node:
                        titles(n, out)
                elif isinstance(node, dict):
                    if node.get("title"):
                        out.add(node["title"])
                    titles(node.get("children") or [], out)
                return out

            nav_titles = titles(proj.get("toc"), set())
            expected_titles = {t for _, c in myst_secs for t, _ in c} | {s for s, _ in myst_secs}
            absent = sorted(expected_titles - nav_titles)
            check(not absent, "sidebar advertises all %d section + notebook titles"
                  % len(expected_titles) + ("" if not absent else " - absent: %s" % absent[:5]))

            slugs = {p.get("short_title") or p.get("title"): p.get("slug")
                     for p in pages if p.get("slug")}
            no_slug = sorted(t for t, _f in [(t, 1) for _, c in myst_secs for t, _ in c]
                             if t not in slugs)
            check(not no_slug, "every notebook has a page slug"
                  + ("" if not no_slug else " - missing: %s" % no_slug[:5]))

            # the theme slugs a notebook after its file name, so a section page linking
            # ../<slug>/ must use the file, not the title it displays
            drift = sorted("%s: /%s != %s" % (t, slugs.get(t), myst_slug(
                os.path.splitext(os.path.basename(f))[0]))
                for _s, c in myst_secs for t, f in c
                if t in slugs and slugs[t] != myst_slug(os.path.splitext(os.path.basename(f))[0]))
            check(not drift, "notebook slugs are the file names"
                  + ("" if not drift else " - %s" % drift[:3]))

            print("\n[8] served site: one URL per notebook")
            bad = []
            for title, _f in [(t, f) for _, c in myst_secs for t, f in c]:
                slug = slugs.get(title)
                if not slug:
                    bad.append("%s (no slug)" % title)
                    continue
                try:
                    st, body = get(base + "/" + slug)
                except (urllib.error.URLError, OSError) as exc:
                    st, body = getattr(exc, "code", str(exc)), ""
                if st != 200:
                    bad.append("%s -> /%s (%s)" % (title, slug, st))
                elif title.split("_")[0] and title.replace("_", "-").lower() not in \
                        body.lower().replace("_", "-"):
                    notes.append("/%s loaded but the title is rendered from the notebook H1" % slug)
            check(not bad, "%d notebook URLs return 200"
                  % sum(len(c) for _, c in myst_secs)
                  + ("" if not bad else " - failing: %s" % bad[:5]))

            print("\n[9] served landing page: section headings + notebook links")
            if html:
                missing_h = [s for s, _ in myst_secs if s not in re.sub(r"<[^>]+>", " ", html)]
                check(not missing_h, "every section name is rendered on the landing page"
                      + ("" if not missing_h else " - absent: %s" % missing_h))
                hrefs = set(re.findall(r'href="(/[^"#?]*)"', html))
                missing_l = sorted(t for t, s in slugs.items() if s and "/" + s not in hrefs)
                check(not missing_l, "landing page links to every notebook"
                      + ("" if not missing_l else " - absent: %s" % missing_l[:5]))

            print("\n[10] served section pages: headings are clickable")
            # a group entry that is only a heading has no slug; with sections/*.md every
            # section is a page, so each one has a slug and a URL of its own
            by_slug = {p.get("slug"): p for p in pages if p.get("slug")}
            no_page, bad_status, slug_drift = [], [], []
            for i, (sec, _kids) in enumerate(myst_secs):
                slug = myst_slug(sec)
                if slug not in by_slug:
                    no_page.append(sec)
                    continue
                if (by_slug[slug].get("short_title") or by_slug[slug].get("title")) != sec:
                    slug_drift.append(sec)
                try:
                    st, _body = get(base + "/" + slug)
                except (urllib.error.URLError, OSError) as exc:
                    st = getattr(exc, "code", str(exc))
                if st != 200:
                    bad_status.append("%s -> /%s (%s)" % (sec, slug, st))
            check(not no_page, "every section heading is a page in the built sidebar"
                  + ("" if not no_page else " - still a plain heading: %s" % no_page[:4]))
            check(not slug_drift, "section slugs match the generator"
                  + ("" if not slug_drift else " - drifted: %s" % slug_drift[:4]))
            check(not bad_status, "%d section pages return 200" % len(myst_secs)
                  + ("" if not bad_status else " - failing: %s" % bad_status[:4]))

            # every ../<slug>/ link on a section page must name a page that really exists:
            # nginx falls back to the app shell, so a 200 alone proves nothing
            known = set(by_slug) | {"index"}
            dangling = []
            for i, (sec, _kids) in enumerate(myst_secs):
                slug = myst_slug(sec)
                try:
                    st, raw = get(base + "/" + slug + ".json")
                except (urllib.error.URLError, OSError):
                    continue
                if st != 200:
                    continue
                for url in sorted(set(ast_links(json.loads(raw)))):
                    target = url.strip("./").rstrip("/")
                    if target and target not in known:
                        dangling.append("%s: %s" % (sec, url))
            check(not dangling, "every link on the section pages points at a real page"
                  + ("" if not dangling else " - dangling: %s" % dangling[:4]))
        else:
            check(False, "could not read /config.json (%s)" % status)

    print("")
    for n in notes:
        print("note: " + n)
    if failures:
        print("\n%d CHECK(S) FAILED" % len(failures))
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
