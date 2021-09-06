# RelyComply Risk Management System

## Run the App in Dev

### Flask App
#### ENV command:
export FLASK_APP=app.main
#### Migrations
#### Run the following commands:
`flask  db init && flask db migrate && flask db upgrade`
Start the flask app on dev server: `flask run --reload`

Start the flask app in production server: `gunicorn app.main`  

## Deployment Instructions
Provision an Ubuntu instance (I've used Ubuntu 20.04 LTS) with suitable security settings.  
SSH into the instance.  
Run `sudo apt update` and `sudo apt install git -y` to install git if your image doesn't already have it.  
Clone this repo and change into it.  
Run `sudo sh setup.sh` to install and configure docker and docker-compose.  
Exit and SSH into the instance again.  
Run the commands in the above "Build and Run the App With Docker" with sudo.  


