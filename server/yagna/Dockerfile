FROM debian:bullseye-slim

ARG DISTFILE=""
LABEL dist_file=${DISTFILE}

# TODO: Download yagna inside container
ADD https://github.com/golemfactory/yagna/releases/download/v0.7.1/golem-requestor_v0.7.1_amd64.deb ./
COPY init.sh ./

RUN chmod +x /usr/bin/* \
    && apt update \
    && yes | apt install -y ./*.deb \
    && apt install -y libssl-dev ca-certificates \
    && update-ca-certificates \
    && chmod +x init.sh

ENTRYPOINT ./init.sh
