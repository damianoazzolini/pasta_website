# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 5000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#copy main directory
WORKDIR /pastawebsite
COPY . /pastawebsite
#copy only /pasta/pasta
RUN rm -r pasta
COPY /pasta/pasta/ ./pasta/pasta

#### Install requirements

#same as requirements.txt
RUN pip install flask
#manually install pasta dependencies
RUN python3 -m pip install clingo
RUN python3 -m pip install numpy

#create empty db
RUN flask --app flaskr init-db

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /pastawebsite
USER appuser

CMD ["flask", "--app", "flaskr/main_interface", "run", "--host=0.0.0.0"]