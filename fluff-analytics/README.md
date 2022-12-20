### Project setup

1. Install Poetry: run this command in your shell `curl -sSL https://install.python-poetry.org | python3 -`
2. Change your terminals current working directory from the root of this repository into the fluff-analytics folder `cd fluff-analytics`
3. Install needed packages using poetry `poetry run pip install -r requirements.txt`
4. Install the `fluff-analytics` package using `poetry install`
5. Set up your `league_analytics/scripts/env.sh` script with the needed API auth configurations
6. Install Docker and docker-compose 
7. Run `docker-compose up -d`

### Adding a new summoner
1. Navigate to http://localhost:5000/
2. Enter a name
3. Click submit

### Populating/refreshing a new summoner's data
1. `cd` into fluff-analytics
2. `poetry run python3 summoner_extract.py`
