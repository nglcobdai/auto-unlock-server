FROM python:3.10

ENV LANG=C.UTF-8 \
    LANGUAGE=en_US \
    PYTHONPATH="/root/workspace/src:$PYTHONPATH"

WORKDIR /root/workspace

# システム依存のライブラリをインストール
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# pipをアップグレードし、必要なパッケージをインストール
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir notebook==6.4.6 jupyter_contrib_nbextensions jupyter_nbextensions_configurator

# Jupyterのnbextensionsをインストールし、nbextensions_configuratorを有効化
RUN jupyter contrib nbextension install --system && \
    jupyter nbextensions_configurator enable --system

# 特定のnbextensionsを有効にする
RUN jupyter nbextension enable codefolding/main && \
    jupyter nbextension enable contrib_nbextensions_help_item/main && \
    jupyter nbextension enable code_font_size/code_font_size && \
    jupyter nbextension enable collapsible_headings/main && \
    jupyter nbextension enable move_selected_cells/main && \
    jupyter nbextension enable printview/main

# Poetryをインストール
RUN pip install --upgrade poetry

# pyproject.toml、poetry.lock、poetry.tomlをコピーする
COPY pyproject.toml poetry.lock poetry.toml $WORKDIR/

RUN poetry install --no-root

RUN python -m ipykernel install --user --name python3.10 --display-name "Python 3.10.12"