# email-client

The project is a simple email-client which aims to allow people to read/send messages, by using their Microsoft, Google accounts - abv.bg is to be added. Additionally they can use basic ToDo app integrated inside the email-client. The functionalities of the project follow a basic version of the Microsoft Outlook+To Do app on Windows.


## Description

The project is split in two parts `frontend` and `backend`. The frontend is build on Next.js and utilizes `typescrtipt` and `tailwind` for styling. On the other handthe backend is build using python - FastAPI - and utilizes basic `sqlite` DB with `SQLModel` as a library to create the modules representing the tables inside the DB.

The backend is build following the OOP principles and uses classes to represent not only the modules, but also the routers and helping classes.

#### Backend

The backend utilizes the FactoryPattern for the use of the external services - Google, Microsoft, because it should allow the easy integration of new external services (abv.bg), without needing a lot of change in the current structure of the app (both frontend call to the backend and the backend itself).

## Getting Started

### Installing

To install the latest updates (dependency wise) go to the ./frotend and run the `npm i` command.

For the backend go to the ./backend, the dependencies are all installed in the venv -> `devenv`. So for you to use them, you will have to setup the VSCode environment to use it.

### Running

For the backend first make sure you are in the ./backend directory. When there connect to the `devenv` environment in your IDE. Finally run the `fastapi dev app\main.py` command. This will start an http server for `localhost:8000`.

For the frontned first make sure you are in the ./frontend directory. When there make sure you have ran the `npm i` command to update the dependencies. Finally run the `npm run https` command. It will start an https server for `localhost:3000`. The server is https, because the project is utilizing `Google SSO`, which requires the use of https server to allow the user to login.


## Authors

Aleksandar Hadzhiev 
[LinkedIn](https://www.linkedin.com/in/aleksandar-hadzhiev-6ab055197/)