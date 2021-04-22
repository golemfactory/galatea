FROM debian:bullseye-slim

COPY *.deb init.sh ./

RUN chmod +x /usr/bin/* \
    && apt update \
    && yes | apt install -y ./*.deb \
    && apt install -y libssl-dev ca-certificates \
    && update-ca-certificates \
    && chmod +x init.sh

ENTRYPOINT ./init.sh
