IMAGE_NAME = linebot-subsidy-fastapi
CONTAINER_NAME = fastapi-test
DOCKER_TAG = $(shell git rev-parse --abbrev-ref HEAD)
MY_FLASK_PORT = 8001

DOCKER_REGISTRY_NAME = fionn88

build:
	docker build -t $(DOCKER_REGISTRY_NAME)/$(IMAGE_NAME):$(DOCKER_TAG) .

run:
	docker run -d -p $(MY_FLASK_PORT):$(MY_FLASK_PORT) --name $(CONTAINER_NAME) $(DOCKER_REGISTRY_NAME)/$(IMAGE_NAME):$(DOCKER_TAG)
