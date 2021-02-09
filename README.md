# Installation

### Install in Linux
```bash
virtualenv .morph-service-env && source .morph-service-env/bin/activate
git clone ssh://bbpcode.epfl.ch/nse/MorphService
cd MorphService
pip install --index-url https://bbpteam.epfl.ch/repository/devpi/bbprelman/dev/+simple/ .
```


### Install in MacOS
```
brew install cmake npm
python3 -m venv .morph-service-env && source .morph-service-env/bin/activate
git clone ssh://<your_user>@bbpcode.epfl.ch/nse/MorphService
pip3 install git+https://github.com/bluebrain/morphio.git
cd MorphService
# Change to the correct branch or version
pip3 install .
```

# Running app
### Running the frontend
```bash
cd morph_service/frontend
npm run dev
```

### Running the server
```bash
python3 manage.py runserver
```

### Test full docker
```bash
make docker_full_build && make local_test
```
