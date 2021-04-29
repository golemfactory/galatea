# Client setup

## System requirements (at least)

| name | version |
| ---- | ------- |
| node | 14.15.3 |
| yarn | 1.22.4  |
| npm  | 6.14.9  |

Note: default package manager for the project is `yarn` but you can use `npm` as well

## DIY

1. Make sure that backend is on

- in `client` dir create `.env.local` file and put there your local environment variable

```
REACT_APP_API=http://0.0.0.0:5000
```

2. Install dependencies (if you haven't earlier or new packages were added)

```
cd client
npm install or yarn install
```

3. Start the client server

```
npm start or yarn start
```

4. App is running on

```
localhost:3000
```
