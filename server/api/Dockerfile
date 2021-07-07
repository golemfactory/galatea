FROM python:3.8-slim

ARG BRANCH="master"
ARG COMMIT=""
LABEL git.branch=${BRANCH}
LABEL git.commit=${COMMIT}

ENV INSTALL_PATH /app
WORKDIR $INSTALL_PATH
ENV MODELS_DIR $INSTALL_PATH/models
ENV MODELS_JSON $INSTALL_PATH/models.json

ENV BRANCH=${BRANCH}
ENV COMMIT=${COMMIT}

ADD https://github.com/golemfactory/yagna/releases/download/v0.7.1/golem-requestor_v0.7.1_amd64.deb ./
RUN apt update \
    && yes | apt install -y ./*.deb \
    && apt install -y libssl-dev ca-certificates \
    && update-ca-certificates

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src ./

# Download models
RUN python download_models.py && rm -rf /root/.cache/huggingface

CMD QUART_ENV=development QUART_APP="app:create_app()" quart run --host=0.0.0.0
