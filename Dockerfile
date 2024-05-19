FROM ubuntu:22.04

ENV LANG=C.UTF-8 \
    LANGUAGE=en_US \
    PYTHONPATH="/root/workspace/app:$PYTHONPATH" \
    DEBIAN_FRONTEND=noninteractive

# 基本ツールのインストール
RUN apt-get update && apt-get install -y wget gnupg software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Pythonのインストール
RUN apt-get update && apt-get install -y python3.10 python3-pip \
    && ln -s /usr/bin/python3.10 /usr/bin/python \
    && rm -rf /var/lib/apt/lists/*

# CUDAをインストール
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin \
    && mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
RUN add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /" \
    && apt-get update
RUN apt-get install -y cuda-12-4 \
    && rm -rf /var/lib/apt/lists/*
ENV LD_LIBRARY_PATH="/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH" \
    PATH="/usr/local/cuda-12.4/bin:$PATH"

# システム依存のライブラリをインストール
RUN apt-get update && apt-get install -y libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/workspace

# pyproject.toml、poetry.lock、poetry.tomlをコピーする
COPY pyproject.toml poetry.lock poetry.toml $WORKDIR/

# Poetryのインストールと依存関係のインストール
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --upgrade poetry

# Temporary directory for Poetry and torch installation
ENV TMPDIR=/root/workspace/tmp
RUN mkdir -p $TMPDIR

# Poetry cache clear
RUN poetry cache clear pypi --all --no-interaction \
    && poetry cache clear cache --all --no-interaction

# Clear cache to free up space
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Poetryの依存関係インストール
RUN poetry install --no-root --only main

# OpenAI-Whisperに必要なライブラリをインストール
RUN apt-get update && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*
