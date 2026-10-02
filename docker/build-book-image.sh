#!/usr/bin/env bash
# Build ams-book on hosts where `docker build` is broken by the default seccomp profile
# (seriema: Docker 19.03 + modern glibc -> "can't start new thread", apt/dpkg failures).
#
# Same pipeline as Dockerfile.book, but every step that executes code runs through
# `docker run --security-opt seccomp=unconfined`; the `docker build` steps only COPY.
#
#   1. toolchain: python + procps + jupyter-book + Node      (run + commit)
#   2. copy the book into it                                 (COPY only)
#   3. jupyter-book build --html --check-links                (run + commit)
#   4. nginx runtime serving _build/html                      (COPY only)
#
# Usage:  ./docker/build-book-image.sh [port]
# Then:   docker run -d --name ams-book -p <port>:80 ams-book:latest
set -euo pipefail

PORT="${1:-3001}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DOCKERFILE="$(mktemp)"
trap 'rm -f "$TMP_DOCKERFILE"' EXIT
cd "$REPO"

cleanup() { docker rm -f ams-book-build >/dev/null 2>&1 || true; }

echo "==> 1/4 toolchain image (procps + jupyter-book + Node) - unconfined"
cleanup
docker run --name ams-book-build --security-opt seccomp=unconfined \
    -e JB_ALLOW_NODEENV=1 python:3.11-slim sh -c '
        set -e
        apt-get update -qq >/dev/null
        apt-get install -y -qq --no-install-recommends procps >/dev/null
        pip install --no-cache-dir "jupyter-book>=2" nodeenv >/dev/null
        jupyter-book --version'
docker commit ams-book-build ams-book-toolchain:local >/dev/null

echo "==> 2/4 copy the book into the toolchain image"
cat > "$TMP_DOCKERFILE" <<'EOF'
FROM ams-book-toolchain:local
WORKDIR /book
COPY . /book
EOF
docker build -f "$TMP_DOCKERFILE" -t ams-book-content:local "$REPO" >/dev/null

echo "==> 3/4 build the static site (--html --check-links) - unconfined"
docker rm -f ams-book-build >/dev/null 2>&1 || true
docker run --name ams-book-build --security-opt seccomp=unconfined \
    ams-book-content:local sh -c 'set -e
        rm -rf /book/_build
        jupyter-book build --html --check-links'
docker commit ams-book-build ams-book-site:local >/dev/null
cleanup

echo "==> 4/4 nginx runtime image: ams-book:latest"
cat > "$TMP_DOCKERFILE" <<'EOF'
FROM nginx:alpine
LABEL org.opencontainers.image.title="Advances in MS Data Processing - Jupyter Book"
COPY docker/book-nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=ams-book-site:local /book/_build/html /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q -O /dev/null http://127.0.0.1/ || exit 1
CMD ["nginx", "-g", "daemon off;"]
EOF
docker build -f "$TMP_DOCKERFILE" -t ams-book:latest "$REPO" >/dev/null

echo "==> done: ams-book:latest ($(docker images -q ams-book:latest | head -1))"
cat <<EOF

Start it:
  docker rm -f ams-book 2>/dev/null || true
  docker run -d --name ams-book -p ${PORT}:80 ams-book:latest

  # or, on this host, let compose manage it (restart: unless-stopped, port 3001):
  docker rm -f ams-book 2>/dev/null || true
  docker-compose up -d book

Verify the landing page, the sidebar and every notebook URL:
  python3 jupyterhub/check_book_indexes.py http://localhost:${PORT}

Public URL on this host: http://seriema.fcfrp.usp.br:${PORT}/  (plain HTTP: no certificate)
EOF
