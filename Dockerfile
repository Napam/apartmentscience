FROM python:3.9-bullseye

WORKDIR /project

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Common bashrc
COPY bashrc /etc/bash.bashrc
# Assert everyone can use bashrc
RUN chmod a+rwx /etc/bash.bashrc

ENV HOME=/project

# Configure user
ARG user
ARG uid
ARG gid

RUN groupadd -g $gid $user && \ 
    useradd --shell /bin/bash -u $uid -g $gid $user