# Secure Register and Login: Frontend template

The front end uses React and Vite with HMR and some ESLint rules.

## Installation

Install packages and run the application with the following commands:

```pwsh
npm install
npm run dev
```

## Run tests

Run Jest tests with the following command:
```pwsh
npm run test
```

## Goals

Implement OWASP's top 10.
Link: https://www.cloudflare.com/en-gb/learning/security/threats/owasp-top-10/

## React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

React docstring syntax: https://jsdoc.app/

CHANGE FAVICON:

first delete the file named icon_lock.svg in the public folder and place the file of your desired favicon there.

then, in index.html you will see a link tag. Replace the name in the href with that of the svg of your desired favicon. If you are using another file format, you might want to change the type as well (eg: for a .ico file: type="image/png" href="/favicon.ico")

<pre>
```
<link rel="icon" type="image/svg+xml" href="/icon_lock.svg" />
```
</pre>

# React Helmet Async:
used to handle meta tags and other header elements.
https://www.youtube.com/watch?v=wWeG8rWkMsM