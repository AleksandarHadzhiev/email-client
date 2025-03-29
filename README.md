# email-client

The project is a simple email-client which aims to allow people to read/send messages, by using their Microsoft, Google accounts - abv.bg is to be added. Additionally they can use basic ToDo app integrated inside the email-client. The functionalities of the project follow a basic version of the Microsoft Outlook+To Do app on Windows.


## Description

The project is split in two parts `frontend` and `backend`. The frontend is build on Next.js and utilizes `typescrtipt` and `tailwind` for styling. On the other handthe backend is build using python - FastAPI - and utilizes basic `sqlite` DB with `SQLModel` as a library to create the modules representing the tables inside the DB.

The backend is build following the OOP principles and uses classes to represent not only the modules, but also the routers and helping classes.

Architecture of the application:

![Architecture of the applicaiton](/docs/images/architecture.png)

#### Backend

The backend utilizes the FactoryPattern for the use of the external services - Google, Microsoft, because it should allow the easy integration of new external services, without needing a lot of change in the current structure of the app (both frontend call to the backend and the backend itself). Here is an example:

![Flow of utilizing FactoryPattern](/docs/images/Flow-login.png)

In the flow we can see three different factories: One for the DTOs (based on the incoming data format generate a DTO object), one for the external services (based on the incoming email format - @gmail.com, @outlook.com, @abv.bg.. - return an object of the appropriate class to handle the functionality needed), finally for the validation, here the previously created DTO object is used and based on it a certain validation flow is used.

By utilizing all three factories the API call can be upgraded by simply adding new classses and not changing the already existing code. Here is an example:

```python
class DTOFactory:
    def __init__(self, data: dict):
        self.data = data
        self.supported_dtos = [
            [{"email":""},ExternalServiceLogin()],
            [{"email":"", "password": ""},EmailAndPasswordLogin()],
            [{"email":"", "password": "", "username": ""},EmailAndPasswordLogin()],
            [{"to": "", "from": "", "date": "", "subject": "", "body": ""}, CreateEmailDTO()],
            [{"to": "", "from": "", "date": "", "subject": "", "body": "", "attachments": []}, EmailWithAttachmentsDTO()],
            [{"title": "", "description": "", "due_date": "", "email": ""}, CreateTodoDTO()],
            [{"title": "", "due_date": "",  "email": ""}, CreateTodoNoDescDTO()],
            [{"title": "", "email": ""}, CreateTodoNoDateDTO()],
        ]
# The rest of the code
```

As you can see all I need to do is update the list of supported_dtos or incoming data formats and nothing else. That applies for the other factories as well.

Also the backend utilizes Singleton for two purposes. First for a custom logger. The logger saves all the error messages in a json file. Which can then be easily read from a developer. Scond for a CSRF Token creation, in this case to be able to store a initial value  of a secret/token and be able to use it across the whole application, the pattern waqs needed.

#### Frontend

The frontend is build on Next.js using tailwing for styling. It is seperating the structure into pages, components and APICallers. The more interesting part of the frontend is the APICallers. They have the following structure:
RequestHaldner, ExternalServiceRequestHandler and TodoRequestHandler. THe RequestHandler is where the API call is actually executed and is being used by the other two. They on heir end are doing the appropriate checks before returning the desired data to the components using them. The checks are in the from of whether the expected data is part of the response.

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