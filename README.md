## Installing 
1. Install Poetry
2. `poetry install`

## Adding a new summoner to track data
1. In your terminal, make sure you are at the root of the project
2. `go run fluff_analytics/server/main.go`
3. In a new terminal, run `curl "http://localhost:3333/summoner?summoner={SUMMONER}"`
    1. NOTE: `{SUMMONER}` is the in game name of the user you want to track

## Configuring and Setting the API key
1. Create a file at the root directory called `.env`
2. Navigate to the product's page in the Riot Games Dev portal, and copy the API key
3. In the `.env` file, type `API_KEY={API_KEY_COPIED}`
