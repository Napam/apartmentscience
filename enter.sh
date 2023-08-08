#!/usr/bin/env bash
containerEngine=${CONTAINER_ENGINE:-docker}
${containerEngine} exec -it $(rg -oP "IMG_NAME = \K\w+" Makefile)-cntr bash
