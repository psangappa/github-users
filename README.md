# Github Users

This is a library for GitHub API at https://developer.github.com/v3/, 
that implements aiohttp application in Python 3.8 that makes asynchronous calls
to github’s API concurrently to get users info.


### Dependencies

* Python >= 3.8
* Make
* The dependencies are listed in [pyproject.toml](./pyproject.toml).

### building and testing this project

To create a virtual environment (`/env`) that contains the Python dependencies run:
```shell script
make
```

### Starting the service

To start the service, run:
```shell script
env/bin/start_api
```


### API documentation

Start the service, then open <http://localhost:8000/docs>
or <http://localhost:8000/redoc>.
