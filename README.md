#Siyavula Education Technical Project

## Environmental Variables
Copy `example.env` to `.env`.  
Put your SQLAlchemy connection string into `.env` where indicated.  


## Dev Instructions
Run `pipenv install --dev` to install the env.  
Run `pipenv run pre-commit install` to initialize the git hooks.  
Run `pipenv run pre-commit run --all-files` if there are file that were committed before adding the git hooks.  
Activate the shell with: `pipenv shell`  
Lint with: `pylint app/`  

## Run the App in Dev

### Flask App
Start the flask app on dev server: `export FLASK_APP=app.main:app && flask run --reload`  
Start the flask app in production server: `gunicorn app.main:app`  

## Build and Run the App With Docker)
Run `docker-compose build` to build the containers.  
Run `docker-compose up` to start the app.  
Run `docker-compose up -d` to start the app in detached mode.  
Run `docker-compose down` to stop the app.

## Deployment Instructions
Provision an Ubuntu instance (I've used Ubuntu 20.04 LTS) with suitable security settings.  
SSH into the instance.  
Run `sudo apt update` and `sudo apt install git -y` to install git if your image doesn't already have it.  
Clone this repo and change into it.  
Run `sudo sh setup.sh` to install and configure docker and docker-compose.  
Exit and SSH into the instance again.  
Run the commands in the above "Build and Run the App With Docker" with sudo.  


