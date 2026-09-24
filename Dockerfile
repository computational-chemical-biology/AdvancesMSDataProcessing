# Lite JupyterLab image for the course "Advances in MS Data Processing"
# Includes every Python dependency from requirements.txt.
#
# Build:   docker build -t ams-data-processing .
# Run:     docker run -p 8888:8888 -v "$PWD":/home/jovyan/work ams-data-processing
# Compose: docker compose up

FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    JUPYTER_ENABLE_LAB=yes \
    MLFLOW_SKIP_IP_CHECK=1

# Disable docker-clean hooks: their Post-Invoke `rm` fails under older Docker/overlay2
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# System dependencies: build tools and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# CPU-only PyTorch first -> keeps the image "lite" (no CUDA)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Python course requirements: pinned lockfile (uv pip compile), since the
# unpinned set is not resolvable to coherent versions (fermo-core/matchms
# pin an old rdkit while modern chemprop needs a new one).
COPY requirements-lock.txt /tmp/requirements-lock.txt
RUN pip install --no-cache-dir -r /tmp/requirements-lock.txt

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.root_dir=/work"]