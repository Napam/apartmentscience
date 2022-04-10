# apartmentscience

## How to develop in docker container
1. `make` &rarr; build docker image
1. `./run -dp` &rarr; run container in detached mode, port forwarding 7000:7000
1. `./enter` &rarr; enter docker container
## How to obtain data (WIP):
Assuming you either do this within the container or install the requirements into your environment 
1. `cd volume` &rarr; Switch working directory to `volume` if you are not in container
1. `alembic upgrade head` &rarr; upgrade database to latest revision
1. `python obtainer.py` &rarr; run the data gathering script, will store into database. 
