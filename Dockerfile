# Lite JupyterLab image for the course "Advances in MS Data Processing"
# Includes every Python dependency from requirements.txt plus an R kernel
# for the R-based notebooks (mixOmics / DIABLO, MatrixQCvisUtils, Metanorm).
#
# Build:   docker build -t ams-data-processing .
# Run:     docker run -p 8888:8888 -v "$PWD":/home/jovyan/work ams-data-processing
# Compose: docker compose up

FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    JUPYTER_ENABLE_LAB=yes \
    MLFLOW_SKIP_IP_CHECK=1

# System dependencies: build tools, R with development headers and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        fonts-dejavu \
        r-base \
        r-base-dev \
        r-cran-ggplot2 \
        r-cran-dplyr \
        r-cran-reshape2 \
        r-cran-mgcv \
        r-cran-cowplot \
        r-cran-readxl \
        r-cran-gridextra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work

# CPU-only PyTorch first -> keeps the image "lite" (no CUDA)
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# Python course requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# R kernel + R packages used by the R notebooks
RUN R -e "install.packages('IRkernel')" \
    && R -e "options(repos = c(CRAN = 'https://cloud.r-project.org')); \
             install.packages(c('VennDiagram','extrafont','fANCOVA'))" \
    && R -e "if (!requireNamespace('BiocManager', quietly = TRUE)) \
               install.packages('BiocManager', repos = 'https://cloud.r-project.org'); \
             BiocManager::install('mixOmics', update = FALSE, ask = FALSE)" \
    && R -e "if (!requireNamespace('remotes', quietly = TRUE)) \
               install.packages('remotes', repos = 'https://cloud.r-project.org'); \
             remotes::install_github('tnaake/MatrixQCvisUtils', upgrade = 'never')" \
    && R -e "remotes::install_github('UGENT-LIMET/Metanorm', upgrade = 'never')" \
    && R -e "IRkernel::installspec()"

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--ServerApp.root_dir=/work"]