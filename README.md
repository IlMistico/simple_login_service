# Simple login service
Some parameters of this service can be set as environment variables. 
By default, the service runs on host 0.0.0.0 and port 8765, without SSL/TLS certificates. 
If you want to change hostname and/or port, change the corresponding environment variables in the Dockerfile.
If certificates are installed and desired, the app can be run on https with a redirect from http. To do so, in the Dockerfile, insert the full paths to the keyfile and certfile in the `SSL_KEYFILE` and `SSL_CERTFILE` environment variables. For local runs without Docker, set the two variables in the environment before launching the app.

## Run the Docker image locally
- Clone the repo and `cd` inside it
- Build the image: `docker build -t <IMAGE-NAME> -f ./Dockerfile`
- Run the container: `docker run -p <HOST-PORT>:<SERVICE-PORT> <IMAGE-NAME>`

Don't forget, the service port is the one set in the Dockerfile, so if you change that, you must change `<SERVICE-PORT>` here too.

## Run the tests
The following instructions assume a Linux system with Python 3.10+ installed, but should hold true for Windows with minor changes at most.

- Clone the repo and `cd` inside it
- Create a local venv: `python -m venv venv_app`
- Activate the venv: `source venv_app/bin/activate`
- Install the libraries: `pip install -r requirements.txt`
- Run the tests: `pytest -s`
You can also run the app locally with `python src/main.py`.

As an alternative to `pip`, you can use [poetry](https://python-poetry.org/) to manage the packages and dependencies. Assuming you have poetry installed:
- Clone the repo and `cd` inside it
- Install the dependencies: `poetry install`
- Run the tests: `poetry run pytest -s`
You can also run the app locally with `poetry run python src/main.py`.

# Notes
1. The service doesn't really send emails with the OTP. If you want to manually test the 2FA login, you'll have to capture the stdout, get the generated OTP and use it.
2. The service uses a fake, in-memory database, so restarting it will effectively purge the database. 