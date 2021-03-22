Installation
============

Install in Linux
~~~~~~~~~~~~~~~~

.. code:: bash

    virtualenv .morph-service-env && source .morph-service-env/bin/activate
    git clone ssh://bbpcode.epfl.ch/nse/MorphService
    cd MorphService
    pip install --index-url https://bbpteam.epfl.ch/repository/devpi/bbprelman/dev/+simple/ .

Install in MacOS
~~~~~~~~~~~~~~~~

::

    brew install cmake npm
    python3 -m venv .morph-service-env && source .morph-service-env/bin/activate
    git clone ssh://<your_user>@bbpcode.epfl.ch/nse/MorphService
    pip3 install git+https://github.com/bluebrain/morphio.git
    cd MorphService
    # Change to the correct branch or version
    pip3 install .

Running app
===========

Running the frontend
~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    cd morph_service/frontend
    npm run dev

Running the server
~~~~~~~~~~~~~~~~~~

.. code:: bash

    cd morph_service
    python3 manage.py runserver

Test full docker
~~~~~~~~~~~~~~~~

.. code:: bash

    make docker_full_build && make local_test

Deployement
===========

1. After having merged the PR containing the new features. Makes a PR to
   bump the release.
2. Once the release has been created, go to
   https://bbpcode.epfl.ch/ci/job/nse.morph-service/build?delay=0sec
   check the box "release" and click "Bulid". This is all that is
   required to trigger the deployement of the new release.

Accessing the production image
==============================

You can find the running image at
https://ocp.bbp.epfl.ch:8443/console/project/bbp-ou-nse/browse/dc/morph-service?tab=history
On this page you can also force the redeployement of a given image by
clicking the "Deploy" button at the top right of the page.

Logs and debugging terminal can be found at:

- Go to the `deployment <https://ocp.bbp.epfl.ch:8443/console/project/bbp-ou-nse/browse/dc/morph-service?tab=history>`_ 
- Select the latest deployment
- Scroll down until Pods
- Click on the name of the pod
- Click on Terminal tab (for debugging) or Logs for the latest logs

If after the new deployment you want to rollback, just go to the previous deployment and under Status you will see a "Roll Back" button.
