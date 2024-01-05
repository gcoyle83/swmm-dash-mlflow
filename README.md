# SWMM-Dash-MLflow
This repo provides a minimum working example for an Azure web app (using Dash) that runs SWMM in the backend based on a constrained set of user inputs at the front end. 

Features include:
-  controls card for selecting system control settings and running sim
-  simulation flows tab
-  system profile (HGL) tab
Future work: 
-  log run info to an MLFlow tracking URI in an Azure ML workspace, and displays select outputs to the Dash layout.

Components:

-  Virtual environment management with `venv`
<!-- -  Automated code review with `Pylint` and `Black` (initially disabled)
<!-- -  Functional tests with `Pytest` (initially disabled) -->
<!-- -  Remote tests to support reproducibility (via GitHub Actions - initially disabled) -->
<!-- -  Automated project documentation rendering with Quarto (initially disabled) -->
-  Integration between an Azure web app, GitHub repo, Azure ML workspace and MLFlow tracking registry 

# Usage
Under construction.

# Documentation
Documentation is in development under `docs/` but note that GH Pages hosting is deferred during initial development. The docs website may be viewed under `docs/build-docs` by downloading and opening as a local website. Documentation is organized under a practical `design`, `implement`, `use` structure which should be intuitive enough to excuse further explanation.
