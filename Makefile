INSTALL_MODULES=.

TEST_MODULES=morph_service/annotations

COVER_PACKAGES=morph_service

PYTHON_PIP_VERSION=pip==9.0.1

OPTIONAL_FEATURES:='[extension_tests]'

VERSION=$(shell python -c 'from morph_service.version import VERSION; print(VERSION)')
DOCKER_IMAGE=docker-registry-default.ocp.bbp.epfl.ch/bbp-ou-nse/morph-service


##### DO NOT MODIFY BELOW #####################

CI_REPO?=ssh://bbpcode.epfl.ch/platform/ContinuousIntegration.git
CI_DIR?=ContinuousIntegration

FETCH_CI := $(shell \
        if [ ! -d $(CI_DIR) ]; then \
            git clone $(CI_REPO) $(CI_DIR) > /dev/null ;\
        fi;\
        echo $(CI_DIR) )
include $(FETCH_CI)/python/common_makefile

##### Override the Common Makefile ######

devinstall: virtualenv
	for f in $(INSTALL_MODULES); do \
		if [ -f $$f/setup_requirements.txt ]; then \
			$(PIP) install $(PIPPROXY) -r $$f/setup_requirements.txt; \
                fi; \
		(cd $$f && $(PIP) install $(PIPPROXY) --pre -e .$(OPTIONAL_FEATURES) --process-dependency-links); \
	done

test_morph_service/annotations:
		@-rm .coverage 2> /dev/null
		$(PLATFORM_VENV)/bin/coverage run manage.py test morph_service $* $(NOSEOPS) --exe --with-xunit --xunit-file=$(TEST_REPORTS_DIR)/nosetests_$(subst /,_,$*).xml && \
		cd ..
		mv .coverage .coverage.$(subst /,_,$*)

ci_dep.txt: virtualenv
	touch $@

$(PLATFORM_VENV)/bin/activate:
	$(CHECK_PYTHON_PATH)
	virtualenv --no-site-packages $(PLATFORM_VENV)
	touch $(PLATFORM_VENV)/bin/activate

##### Docker ######

.PHONY: local_test

local_test:
	docker run -it --rm -p 8000:8000 morph-service:$(VERSION)

docker_shell:
	docker run -it --rm morph-service:$(VERSION) /bin/bash

docker_full_build: local_sdist build

local_sdist:
	python setup.py sdist

build:
	@echo "building docker image version:$(VERSION)"
	docker build -t morph-service:$(VERSION) \
		--build-arg=http_proxy=http://bbpproxy.epfl.ch:80/ \
		--build-arg=https_proxy=http://bbpproxy.epfl.ch:80/ \
		.
	@if echo $(VERSION) | grep -q '^[0-9]\{1,\}\.[0-9]\{1,\}\.[0-9]\{1,\}$$'; then \
		docker tag morph-service:$(VERSION) $(DOCKER_IMAGE):$(VERSION) && \
		docker push $(DOCKER_IMAGE):$(VERSION) && \
		echo "morph-service version:$(VERSION) pushed to OpenShift registy"; \
	else \
		echo "version is DEV, skipping docker image push"; \
	fi

release:
	@echo "releasing $(VERSION) with latest tag"
	@echo "make sure your version.py contains release version and not dev"
	docker pull $(DOCKER_IMAGE):$(VERSION)
	docker tag $(DOCKER_IMAGE):$(VERSION) $(DOCKER_IMAGE):latest
	docker push $(DOCKER_IMAGE):latest
