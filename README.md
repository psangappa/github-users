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

In order to start the server, you should set the `GITHUB_TOKEN` to your
personal access token. 

Checkout [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) on how to create your personal access token.

```shell script
export GITHUB_TOKEN=GithubPersonalAccessToken
```

To start the service, run:
```shell script
env/bin/start_api
```

### Testing

The **tests** live in the `tests/` directory, which mirrors the structure of the `github_users/` directory.

To run the tests of the project run:
```shell script
make test
```

Again, you might need to set the `GITHUB_TOKEN` to run integration tests.


### API documentation

Start the service, then open <http://localhost:8000/docs>
or <http://localhost:8000/redoc>.
