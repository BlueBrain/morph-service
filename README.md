# Installation

Web service to upload morphologies, and get a report on issues.


# Installation

## Install in Linux

```bash
    virtualenv .morph-service-env && source .morph-service-env/bin/activate
    git clone https://github.com/BlueBrain/morph-service/ 
    cd MorphService
    pip install .
```

# Running app

## Running the frontend

```bash
    cd morph_service/frontend
    npm run dev
```

## Running the server

```bash
    cd morph_service
    python3 manage.py runserver
```

## Test full docker

```bash
    make docker_full_build && make local_test
```

# Acknowledgements


The development of this software was supported by funding to the Blue Brain Project, a research
center of the École polytechnique fédérale de Lausanne (EPFL), from the Swiss government’s ETH Board
of the Swiss Federal Institutes of Technology.

For license and authors, see LICENSE.txt respectively.

Copyright (c) 2017-2024 Blue Brain Project/EPFL
