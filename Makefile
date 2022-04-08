.PHONY: local_test

VERSION=$(shell python -c 'from morph_service.version import VERSION; print(VERSION)')
IMAGE_NAME=morph-service
DOCKER_IMAGE=bbpgitlab.epfl.ch:5050/bbp-ou-nse/$(IMAGE_NAME)

local_test:
	docker run -it --rm -p 8000:8000 $(IMAGE_NAME):$(VERSION)

docker_shell:
	docker run -it --rm $(IMAGE_NAME):$(VERSION) /bin/bash

clean:
	rm -drf morph_service/frontend/dist
	rm -drf morph_service/static
	rm -drf .tox/dist

docker_full_build: clean local_sdist build

local_sdist:
	which python
	tox -v -e py38

build:
	@echo "building docker image version:$(VERSION)"
	docker build -t $(IMAGE_NAME):$(VERSION) \
		--build-arg=http_proxy=http://bbpproxy.epfl.ch:80/ \
		--build-arg=https_proxy=http://bbpproxy.epfl.ch:80/ \
		.
	@if echo $(VERSION) | grep -q '^[0-9]\{1,\}\.[0-9]\{1,\}\.[0-9]\{1,\}$$'; then \
		docker tag $(IMAGE_NAME):$(VERSION) $(DOCKER_IMAGE):$(VERSION) && \
		docker push $(DOCKER_IMAGE):$(VERSION) && \
		echo "$(IMAGE_NAME) version:$(VERSION) pushed to Gitlab registy"; \
	else \
		echo "version is DEV, skipping docker image push"; \
	fi

release:
	@echo "releasing $(VERSION) with latest tag"
	@echo "make sure your version.py contains release version and not dev"
	docker pull $(DOCKER_IMAGE):$(VERSION)
	docker tag $(DOCKER_IMAGE):$(VERSION) $(DOCKER_IMAGE):latest
	docker push $(DOCKER_IMAGE):latest
