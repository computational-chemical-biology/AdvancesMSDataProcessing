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
and sidebar are generated from `notebooks2.0.txt`:

```
0-Index.ipynb
tutorial_resumido_python.ipynb            # Python refresher (kept in the repo, not in the book index)
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

**Book config:** `myst.yml` (Jupyter Book v2 / MyST — `project.toc` drives the left panel),
`_config.yml` + `_toc.yml` (Jupyter Book v1). All three are generated from
`notebooks2.0.txt` by `jupyterhub/build_index.py`.
**Environment:** `requirements.txt` (pip) and `environment.yml` (conda).
**Containers:** `Dockerfile` + `docker-compose.yml` (lite JupyterLab image).

---

<!-- BEGIN GENERATED: notebook index (jupyterhub/build_index.py) -->

## Notebook index

26 notebooks in 8 sections, exactly as listed in `notebooks2.0.txt` and as served
by the book sidebar. Every notebook has an **Open in Colab** link; the *Source* column
repeats the original URL recorded in `notebooks2.0.txt`. The book landing page and
every section page repeat this same table.

[Online book](http://localhost:3001/) | [Repository](https://github.com/computational-chemical-biology/AdvancesMSDataProcessing) | [JupyterHub](https://seriema.fcfrp.usp.br/hub/)

### Introduction

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [PyOpenMS_Prerequisites.ipynb](SpectralDataPreprocessingTreatment/PyOpenMS_Prerequisites.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/SpectralDataPreprocessingTreatment/PyOpenMS_Prerequisites.ipynb) | https://github.com/timosachsenberg/PyOpenMSCourse |

### Pre-processing

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [basic_mass_spectrum_preprocessing_peak_detection.ipynb](SpectralDataPreprocessingTreatment/basic_mass_spectrum_preprocessing_peak_detection.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/SpectralDataPreprocessingTreatment/basic_mass_spectrum_preprocessing_peak_detection.ipynb) | — |
| [pyopenms-api.ipynb](SpectralDataPreprocessingTreatment/pyopenms-api.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/SpectralDataPreprocessingTreatment/pyopenms-api.ipynb) | https://github.com/computational-chemical-biology/SSIM |
| [PyOpenMS_Task1_Peaks.ipynb](SpectralDataPreprocessingTreatment/PyOpenMS_Peaks.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/SpectralDataPreprocessingTreatment/PyOpenMS_Peaks.ipynb) | https://github.com/timosachsenberg/PyOpenMSCourse |
| [python_in_proteomics_peerj_27736v1.ipynb](SpectralDataPreprocessingTreatment/python_in_proteomics_peerj_27736v1.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/SpectralDataPreprocessingTreatment/python_in_proteomics_peerj_27736v1.ipynb) | https://books.rsc.org/books/edited-volume/862/chapter-abstract/624111/Python-in-Proteomics?redirectedFrom=fulltext |

### Statistical robustness

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [QC-MXP_demo.ipynb](StatisticalValidationModelRobustness/QC-MXP_demo.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/StatisticalValidationModelRobustness/QC-MXP_demo.ipynb) | https://broadhurstdavid.github.io/QC-MXP/ |

### Signal annotation

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [matchms_spectral_library.ipynb](CheminformaticsAppliedMassSpectrometryStructuralAnalysis/matchms_spectral_library.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/CheminformaticsAppliedMassSpectrometryStructuralAnalysis/matchms_spectral_library.ipynb) | — |
| [matchms_networking.ipynb](CheminformaticsAppliedMassSpectrometryStructuralAnalysis/matchms_networking.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/CheminformaticsAppliedMassSpectrometryStructuralAnalysis/matchms_networking.ipynb) | — |
| [massql.ipynb](CheminformaticsAppliedMassSpectrometryStructuralAnalysis/massql.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/CheminformaticsAppliedMassSpectrometryStructuralAnalysis/massql.ipynb) | — |
| [iceberg_demo_pubchem_elucidation.ipynb](CheminformaticsAppliedMassSpectrometryStructuralAnalysis/iceberg_demo_pubchem_elucidation.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/CheminformaticsAppliedMassSpectrometryStructuralAnalysis/iceberg_demo_pubchem_elucidation.ipynb) | https://github.com/coleygroup/ms-pred |
| [PyOpenMS_ID.ipynb](CheminformaticsAppliedMassSpectrometryStructuralAnalysis/PyOpenMS_ID.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/CheminformaticsAppliedMassSpectrometryStructuralAnalysis/PyOpenMS_ID.ipynb) | https://github.com/timosachsenberg/PyOpenMSCourse |

### Exploratory data analysis

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [Stats_Untargeted_Metabolomics_python.ipynb](MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python.ipynb) | — |
| [Stats_Untargeted_Metabolomics_python_part1.ipynb](MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python_part1.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python_part1.ipynb) | — |
| [Stats_Untargeted_Metabolomics_python_part2.ipynb](MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python_part2.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python_part2.ipynb) | — |
| [Stats_Untargeted_Metabolomics_python_part3.ipynb](MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python_part3.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/Stats_Untargeted_Metabolomics_python_part3.ipynb) | — |
| [t_metabol_01_intro.ipynb](MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/t_metabol_01_intro.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/t_metabol_01_intro.ipynb) | https://omicverse.readthedocs.io/en/latest/Tutorials-metabol/t_metabol_01_intro.html |
| [t_metabol_02_multivariate.ipynb](MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/t_metabol_02_multivariate.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/MultivariateExploratoryAnalysisSupervisedModelsClassificationPrediction/t_metabol_02_multivariate.ipynb) | https://omicverse.readthedocs.io/en/latest/Tutorials-metabol/t_metabol_02_multivariate.html |

### Compound activity prediction

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [FERMO_core_case_study.ipynb](PredictiveModelingBioactivityChemicalProperties/FERMO_core_case_study.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/PredictiveModelingBioactivityChemicalProperties/FERMO_core_case_study.ipynb) | https://github.com/fermo-metabolomics |
| [chemprop_colab_demo_acs_fall2023.ipynb](PredictiveModelingBioactivityChemicalProperties/chemprop_colab_demo_acs_fall2023.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/PredictiveModelingBioactivityChemicalProperties/chemprop_colab_demo_acs_fall2023.ipynb) | https://github.com/chemprop/chemprop-workshop-acs-fall2023 |
| [chemprop_colab_demo_acs_fall2023_exercises.ipynb](PredictiveModelingBioactivityChemicalProperties/chemprop_colab_demo_acs_fall2023_exercises.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/PredictiveModelingBioactivityChemicalProperties/chemprop_colab_demo_acs_fall2023_exercises.ipynb) | — |

### Data Integration

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [multiomics.ipynb](DataIntegrationMassSpectrometry/multiomics.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/DataIntegrationMassSpectrometry/multiomics.ipynb) | https://github.com/Multiomics-Analytics-Group/course_multi-omics_data_science/blob/main/multiomics/notebooks/multiomics.ipynb |

### Emerging applications

| Notebook | Open in Colab | Source |
| --- | --- | --- |
| [dreams_beer_profiler_workshop.ipynb](SupervisedUnsupervisedMachineLearning/dreams_beer_profiler_workshop.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/SupervisedUnsupervisedMachineLearning/dreams_beer_profiler_workshop.ipynb) | https://github.com/pluskal-lab/DreaMS |
| [AlphaPept.ipynb](EmergingComputationalPlatformsPipelines/AlphaPept.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/EmergingComputationalPlatformsPipelines/AlphaPept.ipynb) | https://github.com/MannLabs/alphapept |
| [Modeling_Protein_Ligand_Interactions.ipynb](EmergingComputationalPlatformsPipelines/Modeling_Protein_Ligand_Interactions.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/EmergingComputationalPlatformsPipelines/Modeling_Protein_Ligand_Interactions.ipynb) | https://github.com/deepchem/deepchem |
| [ToolUniverse_CaseStudy.ipynb](EmergingComputationalPlatformsPipelines/ToolUniverse_CaseStudy.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/EmergingComputationalPlatformsPipelines/ToolUniverse_CaseStudy.ipynb) | https://aiscientist.tools/ |
| [googleADK.ipynb](EmergingComputationalPlatformsPipelines/googleADK.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/EmergingComputationalPlatformsPipelines/googleADK.ipynb) | https://adk.dev/ |

<!-- END GENERATED: notebook index -->

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

## Run with Docker (JupyterLab image)

A JupyterLab image ships all Python requirements:

```bash
docker build -t ams-data-processing .
# or simply
docker compose up
# open http://localhost:8888 in your browser
```

The course folder is mounted at `/work`, so notebook changes are kept on the host.

> **⚠ This host (seriema):** Docker 19.03's default seccomp profile breaks
> `dpkg` during image builds. Build with `docker run --security-opt seccomp=unconfined`
> + `docker commit`, or use the pre-built images.

## Multi-user access (JupyterHub, ~50 students)

This repository also ships a **JupyterHub** deployment (`docker-compose.yml` +
`jupyterhub/`) that gives each student their own isolated container behind a login
page. **See [JUPYTERHUB.md](JUPYTERHUB.md)** for setup, accounts, user data,
capacity planning and how to build the slim/hub images on a restricted host.

---

## Build the Jupyter Book (static HTML)

Two engines are supported and **they take different arguments**: Jupyter Book v2 is the
MyST CLI and takes **no directory argument**, while Jupyter Book v1 takes the book folder.

### Jupyter Book v2 (MyST-based, recommended)

```bash
pip install jupyter-book>=2
cd AdvancesMSDataProcessing          # run FROM INSIDE the book folder

jupyter-book build --html            # static site -> _build/html/ (one dir per page)
jupyter-book start                   # runs the book: server on http://localhost:3000, auto-reloads
```

- **`jupyter-book build` takes no path.** The positional argument expects *files*, not a
  folder, so `jupyter-book build .` fails with
  `Error: EISDIR: illegal operation on a directory, read` / `No file exports found`.
- **Flags:** `--html` renders the deployable site (one `<page>/index.html` per notebook,
  plus `config.json` with the sidebar) — this is what you serve or upload to GitHub Pages.
  `--site` only emits the data/template bundle in `_build/site/`; plain
  `jupyter-book build` behaves like `--site` and produces **no HTML**. `--check-links`
  reports every broken internal link, `--strict` fails the build on them.
- **`jupyter-book start` runs the book** for local preview: it serves the site on
  `http://localhost:3000` (`--port 3001` to move it) and **rebuilds + reloads
  automatically** whenever you save a notebook or a config file. It is a dev server, so
  every page lives behind the single URL `/` — deep links such as `/pyopenms-prerequisites`
  only work in the built site (`--html`), not in `start`.
- If the build dies with `Emitted 'error' event ... spawn ps ENOENT`, the CLI needs `ps`:
  `apt-get install procps` (or `dnf install procps-ng`).
- Notebooks are **not executed** during the build — outputs are rendered as stored
  (the equivalent of Jupyter Book v1's `execute_notebooks: off`).
- Page URLs are **slugified without the `.html` extension**, e.g.
  `http://localhost:3000/pyopenms-prerequisites` — do **not** append `.html` or the
  original path. ("Document not found" for a `.html` URL means you are using the v1-style
  URL — drop the extension.)

### Jupyter Book v1 (Sphinx-based)

```bash
pip install "jupyter-book<2"
jupyter-book build .                 # v1 DOES take the folder (this is the only place "." is right)
# preview: open _build/html/index.html
```

Publish to GitHub Pages (optional):

```bash
ghp-import -n -p -f _build/html
```

## Serve the book over the web (Docker)

`Dockerfile.book` builds the book and serves it with nginx:

```bash
docker build -f Dockerfile.book -t ams-book .
docker run -d --name ams-book -p 3001:80 ams-book      # http://<host>:3001
```

Then check the landing page, the sidebar and every notebook URL at once:

```bash
python3 jupyterhub/check_book_indexes.py http://localhost:3001
```

It verifies that `myst.yml`, `_toc.yml` and `0-Index.ipynb` all agree with
`notebooks2.0.txt`, that the sidebar advertises every section and notebook, that each
notebook URL returns 200, and that the landing page renders every section heading and
link. Run it without a URL for source-level checks only.

> ⚠ **This host (seriema):** Docker 19.03's default seccomp profile breaks threaded
> programs (`can't start new thread`) and `apt`/`dpkg`, so `docker build` cannot run the
> builder stage. Use the wrapper, which builds via `docker run --security-opt
> seccomp=unconfined` + `docker commit`:
>
> ```bash
> ./docker/build-book-image.sh 3001
> docker run -d --name ams-book -p 3001:80 ams-book:latest
> ```

## Regenerating the index and sidebar

The book index, the table of contents and the JupyterHub notebook set are all generated
from `notebooks2.0.txt`:

```bash
python3 jupyterhub/build_index.py     # rewrites 0-Index.ipynb, _toc.yml and myst.yml
python3 jupyterhub/sync_notebooks.py  # refreshes jupyterhub-notebooks/ (what students see)
```

- `myst.yml` → `project.toc` is what builds the **left panel** in Jupyter Book v2:
  one entry per section name from `notebooks2.0.txt`, with its notebooks nested
  underneath as clickable children. `_toc.yml` is the Jupyter Book v1 equivalent and is
  only read for compatibility.
- `0-Index.ipynb` is the landing page: each section heading followed by a bulleted
  (`-`) list of its notebooks, linking to the source files.

## Updating the book after edits

1. Save your notebook/config changes (no extra step — the build reads the files directly).
2. If the **structure** changed (a notebook added, renamed or moved), regenerate the
   index/sidebar first: `python3 jupyterhub/build_index.py` (see above).
3. Regenerate the site:
   - **With the live server running** (`jupyter-book start`): it watches files and
     rebuilds automatically — just reload the page in your browser.
   - **Manually:** rerun the build command, then clear the browser cache or hard-refresh
     (`Ctrl+Shift+R`) since MyST hashes assets per build:
     ```bash
     jupyter-book clean --all    # optional: wipe the previous _build output
     jupyter-book build --html   # v2 static site (no path argument)
     jupyter-book build .        # v1 only
     ```
4. Preview at `_build/html/index.html` (v2) or `_build/html/index.html` (v1) — or, with
   the Docker image, at `http://<host>:3001/`.
5. After a fresh clone, always run `pip install -r requirements.txt` (or the conda env)
   before building, so the R/pyOpenMS kernels and notebook deps match.

## Colab badges and source links

Every notebook starts with a **“Open in Colab”** badge and a **Source** link:

```markdown
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](
  https://colab.research.google.com/github/computational-chemical-biology/AdvancesMSDataProcessing/blob/master/<path-to-notebook>)

> **Source:** [host](https://original-URL-from-notebooks.txt)
```

- Badges point to this repo on branch `master` (`computational-chemical-biology/AdvancesMSDataProcessing`).
- If the repository/branch changes, update:
  - the badge path in every notebook,
  - `repository.url`/`branch` in `_config.yml`,
  - `github:` in `myst.yml`.

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