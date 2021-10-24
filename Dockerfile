FROM python:3.9-bullseye

WORKDIR /project

RUN apt-get update && apt-get install -y \
	chromium-driver \ 
&& apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# User setup
COPY bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc
ENV HOME=/project
ARG user
ARG uid
ARG gid
RUN groupadd -g $gid $user && \ 
    useradd --shell /bin/bash -u $uid -g $gid $user

CMD ["/bin/bash"] 