# PastaWebsite
Website for the application [Pasta]( https://github.com/damianoazzolini/pasta) made by [Martini Thomas](https://github.com/MartiniThomas)<br />
(Since this is just an interface, there's no explenation on how Pasta module works)
## Download the package
First of all you need to clone this repository
```
git clone git@github.com:damianoazzolini/pasta_website.git
```
and add the [Pasta]( https://github.com/damianoazzolini/pasta) submodule (see .gitmodules).
<br />

## Local installation
To be able to use the web interface locally you'll need to first create and enter on a python `virtual environment`
and then install all the `requirements` <br />

```
python3 -m venv venv
```

```
. venv/bin/activate
```
The requirements for this application is just flask `Flask` as [Pasta](https://github.com/damianoazzolini/) is connected as a subdirectory to this package and doesn't need to be installed inside the `venv`
```
pip install -r requirements.txt
```
<br />

## Create a local Database
We'll use sqlite3 for this application. <br />
After you've installed it, you can creare your db file:
```
flask --app flaskr init-db
```

after that you can open it (`venv` not needed this and next step):
```
sqlite3 instance/flaskr.sqlite
```

at this point you can run some pre saved queries:
```
.read queries/last10_programs.txt
```
other preset queries are saved in /queries/. <br />
Note: the only way to have an empty db is to delete the "flaskr.sqlite" file and create it again.<br />

## Run tests
To run tests you can use:
```
python3 -m pytest
```
<br />

## RUN THE WEBSITE (locally)
As long as you are still inside the `venv` you can start your web application:
```
flask --app flaskr/main_interface run
```
optional for debug/programming purpose:
```
flask --app flaskr/main_interface --debug run
```
At this point your server will be running at standard ip/port 127.0.0.1:5000 (standard for flask applications). You can add `--host <ip>` to run the app on another ip.
<br />

## Create a Docker image
(there are no images on dockerhub yet) <br/>
To create your own docker image just run the command:
```
docker build -t <image name> .
```
and to run the container:
```
docker run -d -p 5000:5000 <image name>
```
at this point the server will be running locally at `localhost:5000` <br/>
You can also use [Docker Desktop](https://www.docker.com/products/docker-desktop/) to manage your images and containers.