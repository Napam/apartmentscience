CONTAINER_ENGINE ?= docker
CONTAINER_FILE ?= Dockerfile
build_cmd = $(CONTAINER_ENGINE) build --network=host
img_name = apartmentscience

default:
	$(build_cmd) -f $(CONTAINER_FILE) -t $(img_name) .
clean: 
	$(CONTAINER_ENGINE) image rm $(img_name)
