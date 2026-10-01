"""Rebuild the Jupyter Book index and table of contents from notebooks2.0.txt.

Reads notebooks2.0.txt (sections + notebook paths, one per line) and regenerates:

    * 0-Index.ipynb  - landing page listing every section and notebook
    * sections/*.md  - one page per section, so the sidebar group headings are clickable
    * _toc.yml       - Jupyter Book v1 TOC (also read by jupyterhub/sync_notebooks.py)
    * myst.yml       - MyST-MD / Jupyter Book v2 config: project.toc drives the sidebar,
                       site.template picks the book theme
    * README.md      - the notebook index (Colab links), between the GENERATED markers

Run afterwards:

    python3 jupyterhub/sync_notebooks.py

Build the book with `jupyter-book build` (no path argument: the MyST CLI takes files, not
a project directory) or `jupyter-book start` to preview it.

Path quirks handled here: typo'd directories ("AEmergingComputationalPlatformsPipelines/lphaPept"),
renamed files ("PyOpenMS_Task1_Peaks" -> "PyOpenMS_Peaks"), and notebooks whose only copy
lives in a sibling directory. See RENAMES below.
"""
import json
import os
import re

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TXT = os.path.join(ROOT, "notebooks2.0.txt")
INDEX = os.path.join(ROOT, "0-Index.ipynb")
TOC = os.path.join(ROOT, "_toc.yml")
MYST = os.path.join(ROOT, "myst.yml")
README = os.path.join(ROOT, "README.md")
SECTION_DIR = "sections"

REPO_URL = "https://github.com/computational-chemical-biology/AdvancesMSDataProcessing"
REPO_SLUG = "computational-chemical-biology/AdvancesMSDataProcessing"
BRANCH = "master"
COLAB_URL = "https://colab.research.google.com/github/{slug}/blob/{branch}/{path}"

# the README notebook index is regenerated in place between these markers
README_BEGIN = "<!-- BEGIN GENERATED: notebook index (jupyterhub/build_index.py) -->"
README_END = "<!-- END GENERATED: notebook index -->"
README_ANCHOR = "## Install with conda/mamba (recommended)"

# kept out of the book: infrastructure, mirrors and data that sit next to the content
EXCLUDE = [
    "jupyterhub/**",
    "jupyterhub-notebooks/**",
    "_book/**",
    "_build/**",
    ".github/**",
    "data/**",
    "all_mzML/**",
    "**/*.zip",
    "**/*.mzML",
    "**/*.mzXML",
    "**/*.fasta",
    "**/*.fastq",
    "Untitled.ipynb",
    "untitled.md",
    "tutorial_resumido_python.ipynb",
    "core",
]

# txt path -> (real source path under ROOT, name to expose in the index/hub)
RENAMES = {
    "SpectralDataPreprocessingTreatment/PyOpenMS_Task1_Peaks.ipynb": (
        "SpectralDataPreprocessingTreatment/PyOpenMS_Peaks.ipynb",
        "PyOpenMS_Task1_Peaks.ipynb",
    ),
    "AEmergingComputationalPlatformsPipelines/lphaPept.ipynb": (
        "EmergingComputationalPlatformsPipelines/AlphaPept.ipynb",
        "AlphaPept.ipynb",
    ),
    "EmergingComputationalPlatformsPipelinesi/Modeling_Protein_Ligand_Interactions.ipynb": (
        "EmergingComputationalPlatformsPipelines/Modeling_Protein_Ligand_Interactions.ipynb",
        "Modeling_Protein_Ligand_Interactions.ipynb",
    ),
    "EmergingComputationalPlatformsPipelines/dreams_beer_profiler_workshop.ipynb": (
        "SupervisedUnsupervisedMachineLearning/dreams_beer_profiler_workshop.ipynb",
        "dreams_beer_profiler_workshop.ipynb",
    ),
}

# notebook name -> (real source path, exposed name) when the basename does not
# resolve directly. Kept in addition to RENAMES for the Stats_* split set.
EXTRA = {
    "Stats_Untargeted_Metabolomics_python_part1.ipynb": (
        "MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/"
        "Stats_Untargeted_Metabolomics_python_part1.ipynb", "Stats_Untargeted_Metabolomics_python_part1.ipynb"),
    "Stats_Untargeted_Metabolomics_python_part2.ipynb": (
        "MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/"
        "Stats_Untargeted_Metabolomics_python_part2.ipynb", "Stats_Untargeted_Metabolomics_python_part2.ipynb"),
    "Stats_Untargeted_Metabolomics_python_part3.ipynb": (
        "MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/"
        "Stats_Untargeted_Metabolomics_python_part3.ipynb", "Stats_Untargeted_Metabolomics_python_part3.ipynb"),
}


def resolve(rel):
    """Return (real_source_path, hub_name) for a path written in notebooks2.0.txt."""
    rel = rel.strip()
    if rel in RENAMES:
        return RENAMES[rel]
    base = os.path.basename(rel)
    if base in EXTRA:
        return EXTRA[base]
    if os.path.exists(os.path.join(ROOT, rel)):
        return rel, base
    # fallback: search top-level book dirs for the basename
    hits = []
    for d in sorted(x for x in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, x))):
        p = os.path.join(ROOT, d, base)
        if os.path.exists(p):
            hits.append(os.path.join(d, base))
    if len(hits) == 1:
        return hits[0], base
    raise SystemExit(f"cannot resolve {rel!r} (hits={hits})")


def parse():
    sections = []          # [{name, groups: [(trail, [entry...]), ...]}]
    cur = None
    trail = None
    for line in open(TXT, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        if line.startswith("- ") or line.strip().startswith("- "):
            name = line.lstrip("- ").strip()
            cur = {"name": name, "items": []}
            sections.append(cur)
            trail = None
            continue
        if line.strip().lower() in ("metabolomics trail", "proteomics trail"):
            trail = line.strip()
            continue
        # notebook line, optional "- source" annotation
        m = re.match(r"^\s*(.+?\.ipynb)\s*(?:-\s*(.+?))?\s*$", line)
        entry = {"path": m.group(1).strip(), "note": (m.group(2) or "").strip()}
        cur["items"].append((trail, entry))
    return sections


def build_chapters(sections):
    chapters_by_section = {}
    hub = {}  # section -> [(real_path, name_from_txt, note)]
    stats_parts = ("Stats_Untargeted_Metabolomics_python_part1.ipynb",
                   "Stats_Untargeted_Metabolomics_python_part2.ipynb")
    for sec in sections:
        seen = set()
        chapters = []
        hub_list = []
        is_eda = sec["name"].lower().startswith("exploratory")
        for trail, entry in sec["items"]:
            real, hub_name = resolve(entry["path"])
            if hub_name in seen:
                continue
            seen.add(hub_name)
            chapters.append({"real": real, "name": hub_name})
            hub_list.append((real, hub_name, entry["note"]))
            # the combined stats notebook absorbs part1/part2 (see notebooks2.0.txt)
            if is_eda and hub_name == "Stats_Untargeted_Metabolomics_python.ipynb":
                for key in stats_parts:
                    real, hub_name = EXTRA[key]
                    chapters.append({"real": real, "name": hub_name})
                    hub_list.append((real, hub_name, ""))
                    seen.add(hub_name)
        chapters_by_section[sec["name"]] = chapters
        hub[sec["name"]] = hub_list
    return chapters_by_section, hub


def toc_file(entry):
    # _toc.yml stores real source paths (no extension); the index and the hub tree
    # use the same layout, so one set of relative links works in the book AND in JupyterHub
    return os.path.splitext(entry["real"])[0].replace(os.sep, "/")


def myst_slug(text):
    """The slug the theme builds for a page: lowercase, runs of non-alphanumerics -> '-'.

    MyST derives a page slug from the title given in the toc, so the generated section
    pages can link to their neighbours with `../<slug>/` without hardcoding URLs.
    """
    return re.sub(r"[^a-z0-9]+", "-", text.strip().lower()).strip("-")


def section_file(idx, name):
    """Repo-relative path of the generated page for section `idx` (0-based)."""
    return "%s/%02d-%s.md" % (SECTION_DIR, idx + 1, myst_slug(name))


def section_pages(sections, chapters):
    """Write one MyST page per section: the sidebar group heading becomes a real page.

    Each page repeats the section name as its H1 and lists that section's notebooks,
    linking to their book pages with the slug the theme generates (`../<slug>/`), so the
    links hold no matter which path the book is served from.
    """
    folder = os.path.join(ROOT, SECTION_DIR)
    os.makedirs(folder, exist_ok=True)
    written = []
    for i, s in enumerate(sections):
        rel = section_file(i, s["name"])
        entries = chapters[s["name"]]
        lines = [
            "# %s" % s["name"],
            "",
            "%d notebook%s in this section, as listed in `notebooks2.0.txt`."
            % (len(entries), "" if len(entries) == 1 else "s"),
            "",
            "Back to the [complete course index](../).",
            "",
        ]
        for entry in entries:
            title = os.path.splitext(entry["name"])[0]
            # the theme slugs a notebook after its file name, not after the title we show
            # (PyOpenMS_Task1_Peaks is served as /pyopenms-peaks), so link to the file
            page = os.path.splitext(os.path.basename(entry["real"]))[0]
            lines.append("- [%s](../%s/)" % (title, myst_slug(page)))
        with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")
        written.append(rel)
    # drop pages left behind by an older section list
    keep = {os.path.basename(p) for p in written}
    for name in sorted(os.listdir(folder)):
        if name.endswith(".md") and name not in keep:
            os.remove(os.path.join(folder, name))
    return written


def myst_toc(sections, chapters):
    """MyST-MD project.toc: one clickable page per section, notebooks nested underneath.

    A group entry carrying both `file` and `children` is a page with nested items, so the
    panel shows the section names from notebooks2.0.txt as links with their notebooks
    underneath. Each entry carries an explicit `title` (the name as written in
    notebooks2.0.txt) so the panel does not fall back to a notebook's first heading.
    """
    toc = [{"file": "0-Index.ipynb"}]
    for i, s in enumerate(sections):
        children = []
        for entry in chapters[s["name"]]:
            children.append({
                "file": entry["real"].replace(os.sep, "/"),
                "title": os.path.splitext(entry["name"])[0],
            })
        toc.append({"file": section_file(i, s["name"]), "title": s["name"], "children": children})
    return toc


def colab_url(path):
    return COLAB_URL.format(slug=REPO_SLUG, branch=BRANCH, path=path.replace(os.sep, "/"))


def readme_index(sections, hub):
    """Markdown notebook index for the README: one table per section, Colab link each.

    Generated from notebooks2.0.txt, so the list cannot drift from the book or the hub.
    """
    lines = [
        README_BEGIN,
        "",
        "## Notebook index",
        "",
        "%d notebooks in %d sections, exactly as listed in `notebooks2.0.txt` and as served"
        % (sum(len(v) for v in hub.values()), len(sections)),
        "by the book sidebar. Every notebook has an **Open in Colab** link; the *Source* column",
        "repeats the original URL recorded in `notebooks2.0.txt`.",
        "",
        "[Online book](http://localhost:3001/) | "
        "[Repository](%s) | [JupyterHub](https://seriema.fcfrp.usp.br/hub/)" % REPO_URL,
        "",
    ]
    for s in sections:
        lines += ["### %s" % s["name"], "",
                  "| Notebook | Open in Colab | Source |",
                  "| --- | --- | --- |"]
        for rel, name, note in hub[s["name"]]:
            colab = colab_url(rel)
            # only real URLs belong in the Source column; notebooks2.0.txt also uses the
            # annotation field for internal notes (e.g. "part of the combined notebook")
            source = note if note.startswith(("http://", "https://")) else "—"
            lines.append("| [%s](%s) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](%s) | %s |"
                         % (name, rel, colab, source))
        lines.append("")
    lines.append(README_END)
    return "\n".join(lines) + "\n"


def update_readme(block):
    """Replace the generated notebook index in README.md (idempotent)."""
    try:
        text = open(README, encoding="utf-8").read()
    except FileNotFoundError:
        return False
    if README_BEGIN in text and README_END in text:
        pre = text[:text.index(README_BEGIN)]
        post = text[text.index(README_END) + len(README_END):]
    elif README_ANCHOR in text:
        pre, post = text[:text.index(README_ANCHOR)], text[text.index(README_ANCHOR):]
    else:
        pre, post = text.rstrip("\n") + "\n\n", ""
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(pre.rstrip("\n") + "\n\n" + block + "\n" + post.lstrip("\n"))
    return True


def main():
    sections = parse()
    chapters, hub = build_chapters(sections)
    pages = section_pages(sections, chapters)

    toc = {"format": "jb-book", "root": "0-Index", "parts": [
        {"caption": s["name"], "chapters": [toc_file(e) for e in chapters[s["name"]]]}
        for s in sections
    ]}
    with open(TOC, "w", encoding="utf-8") as fh:
        yaml.safe_dump(toc, fh, sort_keys=False, default_flow_style=False)

    myst = {
        "version": 1,
        "project": {
            "title": "Advanced Mass Spectrometry Data Processing",
            "description": (
                "Interactive notebooks for the Advances in MS Data Processing track of the "
                "5th IberoAmerican School on Advanced Mass Spectrometry (BrMASS)."
            ),
            "github": "https://github.com/computational-chemical-biology/AdvancesMSDataProcessing",
            "license": "CC-BY-4.0",
            "exclude": EXCLUDE,
            "toc": myst_toc(sections, chapters),
        },
        "site": {
            "template": "book-theme",
            "options": {"hide_toc": False},
        },
    }
    with open(MYST, "w", encoding="utf-8") as fh:
        yaml.safe_dump(myst, fh, sort_keys=False, default_flow_style=False, width=100)

    md = [
        "# Advanced Mass Spectrometry Data Processing",
        "",
        "Interactive notebooks for the **Advances in MS Data Processing** track of the",
        "[5th IberoAmerican School on Advanced Mass Spectrometry](https://5iberoamerican.brmass.com/)",
        "(Rio de Janeiro, September 28 - October 2, 2026).",
        "",
        "This online book collects the hands-on notebooks used during the course. The material is",
        "organized following the course program:",
        "",
    ]
    for s in sections:
        md.append(f"## {s['name']}")
        md.append("")
        for rel, name, note in hub[s["name"]]:
            cell_line = f"- [{name}](./{rel})"
            if note and note.startswith(("http://", "https://")):
                cell_line += f"  — {note}"
            md.append(cell_line)
        md.append("")

    nb = {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [
                "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]"
                "(https://colab.research.google.com/github/computational-chemical-biology/"
                "AdvancesMSDataProcessing/blob/master/0-Index.ipynb)\n"]},
            {"cell_type": "markdown", "metadata": {}, "source": [l + "\n" for l in md]},
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                     "language_info": {"name": "python", "version": "3.11"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with open(INDEX, "w", encoding="utf-8") as fh:
        json.dump(nb, fh, indent=1, ensure_ascii=False)

    total = sum(len(c) for c in chapters.values())
    readme_ok = update_readme(readme_index(sections, hub))
    print(f"wrote {INDEX}, {TOC} and {MYST} ({len(sections)} sections, {total} notebooks)")
    print(f"wrote {len(pages)} section pages in {SECTION_DIR}/ ({', '.join(pages)})")
    print(f"updated the notebook index in {README}" if readme_ok
          else f"WARNING: {README} not found, notebook index not written")
    print("build with: jupyter-book build --html     (no path argument)")
    print("next: python3 jupyterhub/sync_notebooks.py")


if __name__ == "__main__":
    main()