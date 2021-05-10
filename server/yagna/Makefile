# Makefile is your friend!
RELEASE_URL := https://github.com/golemfactory/yagna/releases/download
YAGNA_RELEASE := v0.6.4
FILE := golem-requestor_$(YAGNA_RELEASE)_amd64.deb

all: clean build_image

$(FILE):
	curl -L -o $(FILE) $(RELEASE_URL)/$(YAGNA_RELEASE)/$(FILE)

.PHONY: clean download build_image
download: $(FILE)

build:
	docker build --build-arg=DISTFILE=$(FILE) -t yagna-service .

clean:
	rm *.deb || true
	docker rmi yagna-service || true
