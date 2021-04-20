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

COPY ./src .
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD gunicorn -b 0.0.0.0:8001 --access-logfile - "app:create_app()"
