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

COPY requirements.txt src ./
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD QUART_ENV=development QUART_APP="app:create_app()" quart run --host=0.0.0.0
