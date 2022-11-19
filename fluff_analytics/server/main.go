package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"github.com/joho/godotenv"
	_ "github.com/mattn/go-sqlite3"
	"io"
	"log"
	"net/http"
	"os"
)

type Summoner struct {
	Name  string
	Puuid string
}

func getPUUID(summoner_name string) Summoner {
	godotenv.Load()

	url := fmt.Sprintf("https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/%s", summoner_name)
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		log.Fatal(err)
	}
	req.Header.Set("X-Riot-Token", os.Getenv("API_KEY"))

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatal(err)
	}
	defer resp.Body.Close()

	b, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	var summoner Summoner
	json.Unmarshal(b, &summoner)
	return summoner

}

func insertSummoner(summoner Summoner) {
	insertNewSummoner := `INSERT OR IGNORE INTO summoners(name, puuid) VALUES(?,?)`
	db, err := sql.Open("sqlite3", "./fluff.db")
	if err != nil {
		log.Fatal(err)
	}
	_, err = db.Exec(insertNewSummoner, summoner.Name, summoner.Puuid)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
}

func insertSummonerHandler(w http.ResponseWriter, r *http.Request) {
	summoner_name := r.FormValue("summoner")
	if summoner_name == "" {
		log.Print("Summoner names can not be blank")
		return
	}
	log.Printf("Attempting to insert new summoner %s", summoner_name)
	summoner := getPUUID(summoner_name)
	insertSummoner(summoner)
}

func main() {
	http.HandleFunc("/summoner", insertSummonerHandler)
	err := http.ListenAndServe(":3333", nil)
	if err != nil {
		log.Fatal(err)
	}
}
