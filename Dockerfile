FROM ubuntu:22.04

ENV LANG=C.UTF-8 \
    LANGUAGE=en_US \
    PYTHONPATH="/root/workspace/app:$PYTHONPATH"

# 環境変数の設定（非対話的インストールを有効にするため）
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y wget gnupg software-properties-common

RUN apt install -y python3.10 python3-pip
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# CUDAをインストール
RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
RUN mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/3bf863cc.pub
RUN add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/ /"
RUN apt update

# キーボード設定のためのdebconf設定を追加
RUN echo 'keyboard-configuration keyboard-configuration/layoutcode string jp' | debconf-set-selections && \
    echo 'keyboard-configuration keyboard-configuration/xkb-keymap select jp' | debconf-set-selections

# CUDAのインストール
RUN apt install -y cuda-12-4

ENV LD_LIBRARY_PATH="/usr/local/cuda-12.4/lib64:$LD_LIBRARY_PATH" \
    PATH="/usr/local/cuda-12.4/bin:$PATH"

WORKDIR /root/workspace

# システム依存のライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# pyproject.toml、poetry.lock、poetry.tomlをコピーする
COPY pyproject.toml poetry.lock poetry.toml $WORKDIR/

# Poetry
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --upgrade poetry
RUN poetry install --no-root

# OpenAI-Whisperに必要なライブラリをインストール
RUN apt-get update && apt-get install -y ffmpeg
