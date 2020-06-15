# Audio validator

A custom application to validate/annotate short audio segments for creating a spoken language identification dataset.

## Installation

### Requirements

* Python 3
* Conda/Pip
* Npm/Node

### Setup

Clone/download the code. For example:

```bash
git clone https://github.com/jorgenvvv/audio_validator
```

It probably is wise to create a new virtual environment with conda or venv to install the dependencies and run the application.

```bash
conda create -y --name audio_validator python==3.7
```

Install the backend dependencies from the `requirements.txt` file with pip/conda.

```bash
pip install -r requirements.txt
```

### Backend config

There is an example `config.example.py` file in the root of the repository. Rename this file (or create a new one) to `config.py` and fill in the required details.

The values that should definitely be changed or added to the example config file are the following (others can be left as defaults):

* `JWT_SECRET_KEY` - a secret key for JWT authentication between the frontend and backend
* `GOOGLE_AUTH_CLIENT_ID` and `GOOGLE_AUTH_CLIENT_SECRET` - these are needed for the Google sign in option and can be obtained from https://console.developers.google.com
* `AUDIO_PATH` - path where the audio files are stored that will be used in the validation process
* `AUDIO_METADATA_PATH` - path where metadata for the previously set audio files is located

### Frontend setup & config

Navigate to the frontend directory and install the dependencies with npm.

```bash
npm install
```

For running the app in development mode run:

```bash
npm run serve
```

To build the app for production run:

```bash
npm run build
```

Currently the application is configured to be served on a url ending with `/lid_validate`. To change that edit the `frontend/vue.config.js` file and change the value of `"publicPath"`.

In production the frontend expects the backend to be running on port 5000 by default. To change that edit the `frontend/env.production` file and change the port of `VUE_APP_API_URL`.

### Running the app

For development the backend can be started by running:

```bash
FLASK_APP=audio_validator
FLASK_ENV=development
flask run
```

In production something like [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) (as shown in the Flask [documentation](https://flask.palletsprojects.com/en/master/tutorial/deploy/))should be used. Using waitress for starting the app in production would look like:

```bash
waitress-serve --call --port 5000 audio_validator:create_app'
```
