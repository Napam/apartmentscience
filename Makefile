BUILD_CMD = docker build --network=host
DOCKERFILE = Dockerfile
IMG_NAME = apartmentscience

USERNAME = $(shell whoami)
USERID = $(shell id -u)
GROUPID = $(shell id -g)

default:
	$(BUILD_CMD) -f $(DOCKERFILE) -t $(IMG_NAME) .

clean: 
	docker image rm $(IMG_NAME)
