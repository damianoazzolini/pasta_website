# PastaWebsite
Website for the application [Pasta]( https://github.com/damianoazzolini/pasta) made by [Martini Thomas](https://github.com/MartiniThomas)<br />
(Since this is just an interface, there's no explenation on how Pasta module works)
## Download the package
First of all you need to clone this repository
```
git clone git@github.com:damianoazzolini/pasta_website.git
```
or
```
git clone https://github.com/damianoazzolini/pasta_website
```
go inside the project directory (`cd pasta_website`) and add/download the [Pasta]( https://github.com/damianoazzolini/pasta) submodule (with similar command) on the same parent directory.<br/>
pasta_website<br/>
└─ pasta_website <br/>
└─ pasta
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
The requirements for this application are `Flask` and `pytest` for the interface and `clingo` and `numpy` for the Pasta submodule. <br/> Install them with:
```
pip install -r requirements.txt
```
be shure you are inside the `venv` while installing

## Create a local Database
We'll use sqlite3 for this application. <br />
After you've installed it, you can creare your db file:
```
flask --app pasta_website init-db
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
python3 -m pytest --ignore=pasta/
```
remember to ignore pasta/ folder to avoid errors since Pasta dependencies are installed inside the venv and not globally
and we want to test only the application.

## RUN THE WEBSITE (locally)
As long as you are still inside the `venv` you can start your web application with a local Werkzeug server that comes with Flask (only for development => you should use a WSGI server for production deployment es. Apache2):
```
flask --app pasta_website/main_interface run
```
optional for debug/programming purpose:
```
flask --app pasta_website/main_interface --debug run
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
## Run with Apache2
Running the server with Apache2 WSGI Server (mod_wsgi) is pretty simple. <br/>
Most of the work will be the [Apache](https://httpd.apache.org/) installation itself (and it's dependencies). Installing mod_wsgi requires a compiler and the Apache server and development headers installed. After you've installed it you can install the WSGI server (inside the `venv`)
```
pip install mod_wsgi
```
and start the Server (locally)
```
mod_wsgi-express start-server wsgi.py --processes 4
```
see https://flask.palletsprojects.com/en/2.2.x/deploying/mod_wsgi/ for more details and how to run the server on port 80.