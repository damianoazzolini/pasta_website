# PastaWebsite
Website for the application [Pasta]( https://github.com/damianoazzolini/pasta) made by [Martini Thomas](https://github.com/MartiniThomas)<br />
(Since this is just an interface, there's no explenation on how Pasta module works)
## Download the package
First of all you need to clone this repository
```
git clone git@github.com:damianoazzolini/pasta_website.git
```

## Local installation
To be able to use the web interface locally you'll need to first create and enter on a python `virtual environment`
and then install all the `requirements` <br />

```
python3 -m venv venv
```

```
. venv/bin/activate
```
The requirements for this application are `Flask` and [Pasta](https://github.com/damianoazzolini/) package
```
pip install -r requirements.txt
```
Note: Pasta module will install his dependencies but not the pasta module itself (you can drag and drop /pasta/pasta folder inside /venv/lib/python3.8/site-packages) - currently working on a fix
<br /><br />

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
other preset queries are saved in /queries/. <br /><br />

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
At this point your server will be running at standard ip/port 127.0.0.1:5000 (standard for flask applications)





<br /><br /><br />
### notes for myself :)
DONE
- main interface
- static secondary pages
- tests for main_interface & database
- database

TO DO<br />
- docker image