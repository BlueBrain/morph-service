## Install it on a MacOS
```
brew install cmake npm
virtualenv -p python2 venv
source venv/bin/activate
git clone ssh://<your_user>@bbpcode.epfl.ch/nse/MorphService
```
[Change to the correct branch or version]
In the `MorphService` folder: `pip install . --process-dependency-links`
```
git clone ssh://<your user>@bbpcode.epfl.ch/molecularsystems/TMD
pip install git+https://github.com/bluebrain/morphio.git
```
Go inside `TMD` folder and do `git install -e .`
```
pip install django-cors-headers
python manage.py build_js
python manage.py runserver
```