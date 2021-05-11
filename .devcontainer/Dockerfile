FROM mcr.microsoft.com/vscode/devcontainers/base:stretch

# install python build dependencies
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends ca-certificates git make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV PYENV_ROOT /opt/pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:$PATH

# install pyenv globally
RUN curl https://pyenv.run | bash

# install the default python versions from the repo file
COPY .python-version /tmp/.python-version
RUN (cat /tmp/.python-version | xargs -L1 pyenv install ) \
 && pyenv global $(cat /tmp/.python-version) \
 && rm -Rf /tmp/.python-version \
 && pyenv rehash

RUN chmod -R a+rwx /opt/pyenv

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
    && rm -rf /tmp/pip-tmp
