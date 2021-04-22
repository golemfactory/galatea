# Don't fear the Makefile

all: build start

.PHONY: build start

build:
	docker build \
		--build-arg=COMMIT=$$(git rev-parse --short HEAD) \
		--build-arg=BRANCH=$$(git branch --show-current) \
		-t yagna-api .

start:
	# We assume that image is already built
	docker run --rm -it -p 8001:8001 --name poc-api yagna-api

clean:
	docker rmi yagna-api || true
