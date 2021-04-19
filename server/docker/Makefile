# Makefile is your friend!
RELEASE_URL := https://github.com/golemfactory/yagna/releases/download
YAGNA_RELEASE := v0.6.4
FILE := golem-requestor_$(YAGNA_RELEASE)_amd64.deb

all: clean build_image start_yagna

$(FILE):
	curl -L -o $(FILE) $(RELEASE_URL)/$(YAGNA_RELEASE)/$(FILE)

.PHONY: clean build_image start_yagna 
build_image: $(FILE)
	docker build -t yagna:$(YAGNA_RELEASE) -f yagna.Dockerfile .

clean:
	rm *.deb || true
	docker container rm -f janka
	docker rmi yagna:$(YAGNA_RELEASE) || true

start_yagna:
	# assumes the image is already built
	# temporary solution (we want docker-compose)
	docker run -d --name janka yagna:$(YAGNA_RELEASE)
