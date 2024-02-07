FROM python:3.8.3
# Base docker image of python 3.x

RUN pip install --upgrade pip
# Upgrade pip package 

WORKDIR /app
# Change working dir to app

ADD requirements.txt /app/
# Copy requirements.txt from local into app dir inside the container

COPY . .
# Copy the source code from local to app dir

RUN pip install -r requirements.txt
# Refering to copied file inside the app dir install the user dependency

EXPOSE 8080
# Expose a port inside the container on which services run


CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
# Run the command to start the service


