[![Docs](https://github.com/BrownandCaldwell/python-starter-template/actions/workflows/render_docs.yml/badge.svg)](https://silver-adventure-z4859ng.pages.github.io/)
[![Black](https://github.com/BrownandCaldwell/python-starter-template/actions/workflows/format.yml/badge.svg)](https://github.com/BrownandCaldwell/python-starter-template/actions/workflows/format.yml)

# Python Starter Template
This repo provides a basic starter template for best practices developing and testing *unpackaged* Python code. Emphasis on that last point - this is **not** a Python packaging template. This template is for use with generic Python projects that want to take advantage of automated tools to improve the development process, including: 

-  Virtual environment management with `venv`
-  Automated code review with `Pylint` and `Black`
-  Functional tests with `Pytest`
-  Remote tests to support reproducibility (via GitHub Actions)
-  Automated project documentation rendering with Quarto

> [!NOTE]  
> Many of the concepts implemented here are directly from the excellent Duke University Coursera Course by Noah Gift: [*Cloud Computing Foundations*](https://coursera.org/share/0e44a583040b010e6aeb674febbac00e)

# Usage

> [!WARNING]  
> This repo is a *template*. DO NOT clone it and then attempt to modify it (this will fail by design).

For usage details, see the project [website](https://silver-adventure-z4859ng.pages.github.io/).

# Documentation
Another critical component of any well-developed Python project is, of course, documentation. For this template, the documentation is *written/edited* in the `docs` directory (by humans) and is then automatically rendered into a website stored in the `build-docs` folder during the fully automated build process. More details on this procedure are included in the [documentation tools](https://silver-adventure-z4859ng.pages.github.io/tools/documentation.html) page.
