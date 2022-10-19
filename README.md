# PastaWebsite
NOT READY YET <br /><br />
Website for the application Pasta https://github.com/damianoazzolini/pasta <br />

### how to install locally
To be able to use the web interface locally you need to first create a python virtual environment 
and then install all dependencies described in "requirements.txt": <br />

```
python3 -m venv venv
```

```
. venv/bin/activate
```
```
pip install -r requirements.txt
```
<br />
Note: Pasta module will install his dependencies but not the pasta module itself (you can drag and drop /pasta/pasta folder inside /venv/lib/python3.8/site-packages)
<br />

### create your local Database and queries
To create your local db you'll need sqlite3. After you've installed it, you can creare your db file with:
```
flask --app flaskr init-db
```

after that you can open it with:
```
sqlite3 instance/flaskr.sqlite
```

at this point you can run some pre saved queries with:
```
.read queries/last10_programs.txt
```
other preset queries are saved in /queries/. <br />

### run tests
To run tests you can use:
```
python3 -m pytest
```

### DONE
- main interface
- static secondary pages
- tests for main_interface & database
- database

# notes for myself :)
