# pull official base image
FROM python:3.10

# set work directory
WORKDIR /usr/app/

RUN pip install --upgrade pip
# install dependencies
COPY ./requierements.txt .

# install dependencies
RUN pip install -r requierements.txt

# copy project
COPY . /usr/app/

# start project
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh

#CMD ["python3", "testbot.py"]

## start entrypoint
#RUN chmod +x ./entrypoint.sh
#ENTRYPOINT ./entrypoint.sh
