# Makefile is your friend!
RELEASE_URL := https://github.com/golemfactory/yagna/releases/download
YAGNA_RELEASE := v0.6.7-beta.1
FILE := golem-requestor_$(YAGNA_RELEASE)_amd64.deb

all: build

$(FILE):
	curl -L -o $(FILE) $(RELEASE_URL)/$(YAGNA_RELEASE)/$(FILE)

.PHONY: clean download
download: $(FILE)

build: download
	docker build --build-arg=DISTFILE=$(FILE) -t yagna-service .

clean:
	rm *.deb || true
	docker rmi yagna-service || true
