# Makefile is your friend!
all: build

.PHONY: clean

build:
	docker build -t yagna-service .

clean:
	rm *.deb || true
	docker rmi yagna-service || true
