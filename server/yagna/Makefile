# Makefile is your friend!
all: build

.PHONY: build clean

build:
	docker build -t yagna-service .

clean:
	rm *.deb || true
	docker rmi yagna-service || true
