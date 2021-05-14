# Client setup

## System requirements (at least)

| name | version |
| ---- | ------- |
| node | 14.15.3 |
| yarn | 1.22.4  |
| npm  | 6.14.9  |

Note: default package manager for the project is `yarn` but you can use `npm` as well.

However, to build an extension `yarn` is required.

## DIY

1. Make sure that backend is on
   

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

5. For extension

```
yarn build:extension
```

Then, add `client/build` folder to your Chrome extensions.

See [this page](https://webkul.com/blog/how-to-install-the-unpacked-extension-in-chrome/) for quick tutorial
