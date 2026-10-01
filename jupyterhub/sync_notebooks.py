"""Regenerate the curated `jupyterhub-notebooks/` tree from the Jupyter Book TOC.

Users in JupyterHub only see notebooks listed in `_toc.yml` (the book index).
This copies exactly those files (plus the 0-Index root) into
`jupyterhub-notebooks/`, which is bind-mounted read-only as
`/home/jovyan/course-notebooks`. Run it whenever the book changes:

    python3 jupyterhub/sync_notebooks.py
"""
import os
import shutil

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOC = os.path.join(ROOT, "_toc.yml")
DEST = os.path.join(ROOT, "jupyterhub-notebooks")


def main() -> None:
    toc = yaml.safe_load(open(TOC))
    # clear contents in place (never rmtree DEST: it is bind-mounted read-only into
    # every running user container, and replacing the directory inode would leave
    # those mounts pointing at a deleted, empty directory)
    if os.path.isdir(DEST):
        for name in os.listdir(DEST):
            p = os.path.join(DEST, name)
            if os.path.isdir(p) and not os.path.islink(p):
                shutil.rmtree(p)
            else:
                os.unlink(p)
    else:
        os.makedirs(DEST)

    count = 0
    for part in toc["parts"]:
        for chapter in part["chapters"]:
            if isinstance(chapter, dict):
                files = [chapter] + list(chapter.get("sections", []))
            else:
                files = [chapter]
            for e in files:
                if isinstance(e, dict):
                    f = e["file"]
                    name = e.get("name")
                else:
                    f = e
                    name = None
                src = next(f + sfx for sfx in [".ipynb", ".md"] if os.path.exists(f + sfx))
                name = name or os.path.basename(src)
                # mirror the book layout so the index links work in the book and in JupyterHub
                rel_dir = os.path.dirname(f).replace(os.sep, "/")
                out_dir = os.path.join(DEST, rel_dir) if rel_dir else DEST
                os.makedirs(out_dir, exist_ok=True)
                shutil.copyfile(os.path.join(ROOT, src), os.path.join(out_dir, name))
                count += 1

    shutil.copyfile(os.path.join(ROOT, "0-Index.ipynb"), os.path.join(DEST, "0-Index.ipynb"))
    print(f"synced {count + 1} notebooks into {DEST}")


if __name__ == "__main__":
    main()