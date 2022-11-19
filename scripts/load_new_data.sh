#!/bin/bash
cd $HOME/Coding/python_projects/league_analytics/ 

cat assets/fluff_analytics.txt
poetry run python3 fluff_analytics/app.py
git add fluff.db
git commit -m "build: updated database"
git push origin main