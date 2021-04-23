FROM python:3.8-slim

ARG BRANCH="master"
ARG COMMIT=""
LABEL git.branch=${BRANCH}
LABEL git.commit=${COMMIT}

ENV INSTALL_PATH /app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

ENV BRANCH=${BRANCH}
ENV COMMIT=${COMMIT}

COPY init.sh requirements.txt src ./
RUN chmod +x init.sh && pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ./init.sh
