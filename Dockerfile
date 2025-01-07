# Use the official micromamba base image
# build with docker build --platform=linux/amd64
FROM mambaorg/micromamba:jammy

# install mysql server and java
USER 0
RUN apt update && apt install -y --no-install-recommends \
    make gcc build-essential libgtk-3-dev wget git vim \
    mysql-server libmysqlclient-dev \
    openjdk-11-jdk-headless && \
    rm -r /var/lib/apt/lists/*

# install wxPython from wheel (pip tries to build wheel, which takes forever)
# RUN pip install https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-20.04/wxPython-4.2.1-cp39-cp39-linux_x86_64.whl

# copy the environment.yml file to the container
COPY --chown=$MAMBA_USER:$MAMBA_USER mm_wrmxpress_gui.yml /tmp/env.yml

# fix lockfile problems: https://stackoverflow.com/questions/76778360/micromamba-install-gets-stuck-when-run-in-docker-container-on-arm-mac
RUN micromamba config set extract_threads 1

# install dependencies
RUN micromamba install -y -n base -f /tmp/env.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1  

# clone wrmxpress and GUI
ARG CACHEBUST=1
RUN echo ${CACHEBUST} && cd /root/ && git clone --branch v2.0 https://github.com/zamanianlab/wrmXpress.git
RUN echo ${CACHEBUST} && cd /root/ && git clone --branch v2dev_merge https://github.com/wheelerlab-uwec/wrmXpress-gui.git


# COPY wrmXpress/ /wrmXpress/

# copy gui files
# RUN mkdir app
# RUN mkdir assets
# COPY app/ app/
# COPY app.py .
# COPY assets/ assets/

EXPOSE 9000

# The code to run when container is started:
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "/bin/bash", "-c", "while true; do sleep 30; done"]