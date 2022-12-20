# syntax=docker/dockerfile:1

FROM python:3.8.3-slim

COPY . .
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install -r fluff-analytics/requirements.txt
# copy the requirements file into the image


EXPOSE 5000

# install the dependencies and packages in the requirements file

# configure the container to run in an executed manner

WORKDIR /fluff-analytics
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]