.PHONY: local_test

VERSION=$(shell python -c 'from morph_service.version import VERSION; print(VERSION)')

local_test:
	docker run -it --rm -p 8000:8000 morph-service:$(VERSION)

docker_shell:
	docker run -it --rm morph-service:$(VERSION) /bin/bash

docker_full_build: local_sdist build

local_sdist:
	which python
	tox -e py36

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
