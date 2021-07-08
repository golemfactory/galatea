# Server API client of Yagna daemon

To run the api server inside a container simply run `make` in the terminal in this directory.

To remove docker artifacts run `make clean`

## Run unit test
Install `pytest` package, it's not added by the `requirements.txt` file.

in the terminal window inside `api` directory type: `pytest`

## Run tests on devnet
Having dockerized setup it's quite easy to run classifier tests on devnet (or any other subnet of choise)

Where are going to use `docker-compose` which setups connectivity between containers.
Switch to the `server` directory where docker-compose.yml is placed.

### Run yagna service
```bash
docker-compose up -d yagna
```

### Run classifier from api service
```bash
docker-compose run \
  -e YAGNA_APPKEY="$(jq -r '.values[0][1]' yagna_data/app_key)" \
  -e YAPAPI_SUBNET_TAG=devnet-beta.2 \
  -e DENY_LIST="" \
  api python classifier.py
```

Now, you are able to exclude some providers providing space delimited list of provider names for `DENY_LIST` env var.


