FROM python:3.10-bullseye

WORKDIR /project

RUN apt-get update && apt-get install -y \
    chromium-driver \
    iputils-ping \
    tmux \
    sqlite3 \
    vim \
&& apt-get -y autoremove && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# User setup
COPY bashrc /etc/bash.bashrc
RUN chmod a+rwx /etc/bash.bashrc
ENV HOME=/project

CMD ["/bin/bash"]
