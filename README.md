# Little Legend Lab

This is a React application for the Little Legend Lab, a personalized story book generator for kids.

Currently, for the ease of development, this repo contains both the frontend code and the backend code. The frontend runs on React while the backend is a Flask app.

Don't forget to create a .env file to store your environment variables in backend and frontend directories. One different file for each. In the frontend, your .env file should have at least this line: 

```bash
REACT_APP_API_BASE_URL=http://localhost:8000
```
-------------------
## React Frontend Usage

Have NPM installed and add all dependencies. Ideally use a "conda" to activate a new environment. 

```bash
npm install
npm audit fix
npm run build
```
## Quickstart

Start React App
```bash
npm start
```
