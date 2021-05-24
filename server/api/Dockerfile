FROM python:3.8-slim

ARG BRANCH="master"
ARG COMMIT=""
LABEL git.branch=${BRANCH}
LABEL git.commit=${COMMIT}

ENV INSTALL_PATH /app
WORKDIR $INSTALL_PATH

ENV BRANCH=${BRANCH}
ENV COMMIT=${COMMIT}

# TODO: Download yagna inside container
COPY *.deb ./
RUN apt update \
    && yes | apt install -y ./*.deb \
    && apt install -y libssl-dev ca-certificates \
    && update-ca-certificates

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY src ./
CMD QUART_ENV=development QUART_APP="app:create_app()" quart run --host=0.0.0.0
