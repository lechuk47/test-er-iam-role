IMAGE=quay.io/app-sre/external-resources-tests:0.0.2

.PHONY: all
all: build push

.PHONY: build
build:
	docker build -t ${IMAGE} .

.PHONY: push
push:
	docker push ${IMAGE}
