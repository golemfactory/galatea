all: up

.PHONY: clean down up distfile
down:
	docker-compose down

up: yagna-download
	DISTFILE=$$(ls yagna/*.deb) \
	COMMIT=$$(git rev-parse --short HEAD) \
	BRANCH=$$(git branch --show-current) \
	docker-compose up -d

clean: down
	docker rmi yagna-api yagna-service || true
	rm -rf yagna_data

yagna-download:
	$(MAKE) -C yagna download
