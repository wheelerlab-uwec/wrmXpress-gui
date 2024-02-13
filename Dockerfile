# Use the official micromamba base image
FROM --platform=linux/amd64 mambaorg/micromamba:jammy

WORKDIR /

# install mysql server and java
USER 0
RUN apt update && apt install -y --no-install-recommends \
    make gcc build-essential libgtk-3-dev wget git \
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
RUN micromamba install --yes --file /tmp/env.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1  

# clone wrmxpress
RUN git clone --branch gui-backend https://github.com/zamanianlab/wrmXpress.git

RUN mkdir /root/wrmXpress/
RUN mkdir /root/wrmXpress/cp_pipelines
RUN mkdir /root/wrmXpress/cp_pipelines/masks
RUN mkdir /root/wrmXpress/cp_pipelines/worm_models
RUN cp wrmXpress/cp_pipelines/masks/* /root/wrmXpress/cp_pipelines/masks
RUN cp wrmXpress/cp_pipelines/worm_models/*.xml /root/wrmXpress/cp_pipelines/worm_models

# copy gui files
RUN mkdir app
COPY app/ app/
COPY app.py .

EXPOSE 9000

# The code to run when container is started:
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "python", "app.py"]