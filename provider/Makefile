ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

all: virtualenv docker yagna-service-poc-provider.gvmi

.venv/bin/activate:
	python3 -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install gvmkit-build

virtualenv: .venv/bin/activate

docker: Dockerfile classifier
	docker build -t yagna-service-poc-provider -f Dockerfile classifier

yagna-service-poc-provider.gvmi: docker
	./.venv/bin/gvmkit-build --output yagna-service-poc-provider.gvmi yagna-service-poc-provider

push: yagna-service-poc-provider.gvmi
	./.venv/bin/gvmkit-build --push --output yagna-service-poc-provider.gvmi yagna-service-poc-provider

test: docker
	docker container rm -f yagna-service-poc-provider || true
	docker run -d --rm --volume $(ROOT_DIR)/test:/work --name yagna-service-poc-provider yagna-service-poc-provider
	docker exec yagna-service-poc-provider python classifier.py submit /work/the_queen_input.txt /work/test_output.txt
	diff test/test_output.txt test/the_queen_output.json && echo "Test OK"
	rm  -f test/test_output.txt
	docker stop yagna-service-poc-provider || true

clean:
	docker container rm -f yagna-service-poc-provider || true
	docker image rm yagna-service-poc-provider || true
	rm -f yagna-service-poc-provider.gvmi
	rm -f test/test_output.txt
	rm -rf .venv

.PHONY: all virtualenv docker push test clean
