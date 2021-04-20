# Don't fear the Makefile

all: build start

.PHONY: build start

requirements.txt:
	pipenv lock --keep-outdated --requirements > src/requirements.txt

build:
	docker build \
		--build-arg=COMMIT=$$(git rev-parse --short HEAD) \
		--build-arg=BRANCH=$$(git branch --show-current) \
		-t ya-poc-api .

start:
	# We assume that image is already built
	docker run --rm -it -p 8001:8001 --name poc-api ya-poc-api

clean:
	rm requirements.txt || true
	docker rmi ya-poc-api || true
