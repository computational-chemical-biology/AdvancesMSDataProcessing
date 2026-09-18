# Advances in MS Data Processing

<p align="center">
  <b>Advanced Mass Spectrometry Data Processing</b><br>
  Hands-on notebooks for the 5th IberoAmerican School on Advanced Mass Spectrometry
</p>

This repository hosts the interactive **Python book** used in the *Advances in MS Data Processing*
track of the [5th IberoAmerican School on Advanced Mass Spectrometry](https://5iberoamerican.brmass.com/),
organized by **BrMASS** (Brazilian Mass Spectrometry Society).

- **Event:** September 28 – October 2, 2026 — Windsor Excelsior Copacabana, Rio de Janeiro, Brazil
- **Instructor:** Ricardo R. Alves da Silva (University of São Paulo — USP, Ribeirão Preto, Brazil)
- **Course structure:** two full days of hands-on spectral data processing, chemometrics,
  cheminformatics and machine learning applied to mass spectrometry.

---

## Course program (Ricardo Silva — USP)

### Thursday, October 1 — Advances in MS Data Processing: Statistical Methods and Chemometrics

- Spectral Data Preprocessing and Treatment
- Multivariate Exploratory Analysis and Supervised Models for Classification and Prediction
- Data Integration (Data Fusion) in Mass Spectrometry
- Statistical Validation and Model Robustness
- Chemometric Interpretation and Biochemical Relevance

### Friday, October 2 — Advances in MS Data Processing: Cheminformatics and Machine Learning

- Cheminformatics Applied to Mass Spectrometry and Structural Analysis
- Mining and Prediction of Molecular and Structural Data
- Predictive Modeling of Bioactivity and Chemical Properties
- Supervised and Unsupervised Machine Learning
- Emerging Computational Platforms and Pipelines

---

## Repository structure

Notebooks are organized as a [Jupyter Book](https://jupyterbook.org/) whose table of contents
follows `notebooks.txt`:

```
0-Index.ipynb
tutorial_resumido_python.ipynb            # Python refresher (Introduction)
SpectralDataPreprocessingTreatment/       # pyOpenMS, matchms, peak processing
MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/   # PCA/PLS-DA/OPLS-DA, supervised models
DataIntegrationMassSpectrometry/          # DIABLO / N-integration (R), MatrixQCvis
StatisticalValidationModelRobustness/     # Metanorm, QC-MXP
ChemometricInterpretationBiochemicalRelevance/   # Omics interpretation
CheminformaticsAppliedMassSpectrometryStructuralAnalysis/  # docking, PubChem elucidation
MiningPredictionMolecularStructuralData/  # RDKit descriptors, solubility, venns
PredictiveModelingBioactivityChemicalProperties/  # eigenpages/FERMO, Chemprop
SupervisedUnsupervisedMachineLearning/    # DreaMS beer profiler
EmergingComputationalPlatformsPipelines/  # AlphaPept, protein–ligand modelling
```

**Book config:** `_config.yml` + `_toc.yml` (Jupyter Book).
**Environment:** `requirements.txt` (pip) and `environment.yml` (conda).
**Containers:** `Dockerfile` + `docker-compose.yml` (lite JupyterLab image).

---

## Install with conda/mamba (recommended)

```bash
conda env create -f environment.yml
conda activate ams-data-processing
jupyter lab
```

## Install with pip

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

> ℹ️ Some notebooks rely on packages not published on PyPI (`pyvenn`, `DreaMS`, `qcmxp`).
> They are installed *inside* their notebooks — run those notebooks in an environment
> with internet access, or see `requirements.txt` for the commands.

---

## Run with Docker (lite JupyterLab image)

A lightweight JupyterLab image ships all Python requirements plus an R kernel
for the R-based notebooks (mixOmics/DIABLO, MatrixQCvisUtils, Metanorm):

```bash
docker build -t ams-data-processing .
# or simply
docker compose up
# open http://localhost:8888 in your browser
```

The course folder is mounted at `/work`, so notebook changes are kept on the host.

---

## Build the Jupyter Book (static HTML)

```bash
pip install jupyter-book ghp-import
jupyter-book build .
# preview: open _build/html/index.html
```

Publish to GitHub Pages (optional):

```bash
ghp-import -n -p -f _build/html
```

---

## About the school

The 5th IberoAmerican School on Advanced Mass Spectrometry brings together world-renowned
experts in an interactive, in-depth program on the latest advances in mass spectrometry —
from metabolomics, proteomics and imaging to clinical MS, data processing and machine learning.
Registration, venue and program details: <https://5iberoamerican.brmass.com/>.

## License

Material is provided for educational purposes. If you reuse any notebook, please
cite the original authors/notebook sources and the 5th IberoAmerican School on
Advanced Mass Spectrometry.