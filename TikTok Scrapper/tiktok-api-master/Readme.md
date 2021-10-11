# TikTok Scrapper

## Crontab
```
DATABASE_URL=postgres://datawizard:dataroXX!@tiktok-comments-included.cxyylfgchn3l.us-east-1.rds.amazonaws.com:5432/tiktok
0 10 * * * /home/ec2-user/.config/yarn/global/node_modules/pm2/bin/pm2 reload all
20 13 * * * cd /home/ec2-user/tiktok-api/tiktok-api && /home/ec2-user/.local/bin/pipenv run python handler.py > /home/ec2-user/tiktok-api/api.log 2>&1
```

## Deps install
```
cd tiktok-api
pipenv install

cd tiktok-signature
yarn install
```

## Run manually
### Start tiktok-signature
```
cd tiktok-signature
yarn start
```
### Start tiktok-api (scrapper)
```
cd tiktok-api
pipenv run python handler.py
```

## Run manually
### Start tiktok-signature
git clone https://github.com/carcabot/tiktok-signature.git


#### Build

```sh
docker build . -t tiktok-signature
```

#### Run

```sh
docker run -p 80:8080 -v $(pwd):/usr/app tiktok-signature

To generate signatures dynamically this repo comes with an integrated http server (listen.js) which accepts POST requests to http://localhost/signature with url in request body.