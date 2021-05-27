all: up

.PHONY: clean down up distfile yagna api

down:
	docker-compose down

yagna_data:
	mkdir yagna_data || true

up: yagna_data yagna api
	DISTFILE=$$(ls yagna/*.deb) \
	COMMIT=$$(git rev-parse --short HEAD) \
	BRANCH=$$(git branch --show-current) \
	docker-compose up -d

clean: down
	docker rmi yagna-api yagna-service || true
	rm -rf yagna_data
	$(MAKE) -C yagna clean
	$(MAKE) -C api clean

yagna:
	$(MAKE) -C yagna

api:
	$(MAKE) -C api
