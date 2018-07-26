# Installation

```bash
virtualenv .morph-service-env && source .morph-service-env/bin/activate
git clone ssh://bbpcode.epfl.ch/nse/MorphService
cd MorphService
pip install --index-url https://bbpteam.epfl.ch/repository/devpi/bbprelman/dev/+simple/ --process-dependency-links .

 ```

### Install in MacOS
Please visit **/morph_service/docs/install_in_macos.md**

 # Build frontend app
 ```bash
 python manage.py build_js
 ```

 # Running the server
 ```bash
 python manage.py runserver
 ```
