#!/bin/bash
# Seed a writable per-user copy of the course notebooks, then start the server
# as the shared non-root user 'jovyan'. Runs inside the user container on every
# start (paths below are the container's).
set -e

mkdir -p /home/jovyan/work
# -n: never overwrite files the user already modified; missing ones are copied in
# so topic updates show up on restart.
cp -rn /home/jovyan/course-notebooks/. /home/jovyan/work/ 2>/dev/null || true

# Hand home + work to the (previously root-owned) volume to the app user.
# Never recurse into the read-only course-notebooks mount: chown the home dir
# itself and the writable work tree; any dirs the app creates later already
# belong to jovyan because singleuser runs as that user.
chown jovyan:jovyan /home/jovyan
chown -R jovyan:jovyan /home/jovyan/work/ 2>/dev/null || true

# runuser -p keeps the docker-provided env as-is, which still has the base
# image's HOME=/root; singleuser would then try to write /root/.local. Point it
# at the app user's writable home instead.
export HOME=/home/jovyan
export SHELL=/bin/bash
export USER=jovyan

# Cap BLAS threads: the seccomp policy on this host intermittently refuses
# OpenBLAS pthread creation when scipy/sparse is imported.
export OPENBLAS_NUM_THREADS=2

exec runuser -u jovyan --preserve-environment -- jupyterhub-singleuser "$@"