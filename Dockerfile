# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# copy the requirements file into the image
COPY . .

RUN pip install -r requirements.txt
# switch working directory

EXPOSE 5000

# install the dependencies and packages in the requirements file

# configure the container to run in an executed manner

WORKDIR /src
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
