# Don't fear the Makefile
RELEASE_URL := https://github.com/golemfactory/yagna/releases/download
YAGNA_RELEASE := v0.6.7-beta.1
FILE := golem-requestor_$(YAGNA_RELEASE)_amd64.deb

all: download build

.PHONY: download build start

$(FILE):
	curl -L -o $(FILE) $(RELEASE_URL)/$(YAGNA_RELEASE)/$(FILE)

download: $(FILE)

build: download
	docker build \
		--build-arg=COMMIT=$$(git rev-parse --short HEAD) \
		--build-arg=BRANCH=$$(git branch --show-current) \
		-t yagna-api .

start:
	# We assume that image is already built
	docker run --rm -it -p 5000:5000 --name poc-api yagna-api

clean:
	rm *.deb || true
	docker rmi yagna-api || true
