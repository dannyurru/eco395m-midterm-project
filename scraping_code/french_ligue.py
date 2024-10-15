import os
import csv
import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = "csv_collection"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "french_ligue_data.csv")

headers = {
    "Accept": "/", 
    "Accept-Encoding": "gzip, deflate, br",
    "User-Agent": "Chrome/58.0.3029.110",
    "Connection": "keep-alive",
    "Cookie": "SWID=75534310-463B-4EC6-CE90-8370E807F123;dcf=1; connectionspeed=full; country=us; edition=espn-en-us; edition-view=espn-en-us; region=ccpa"
}

with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Standing", "Team Name", "Games Played", "Wins", "Draws", "Losses", 
                     "Goals For", "Goals Against", "Goal Difference", "Points", "Year"])

    for year in range(2003, 2024):
        url = f"https://www.espn.com/soccer/standings/_/league/FRA.1/season/{year}"
        rq = requests.get(url, headers=headers)
        html = rq.text
        soup = BeautifulSoup(html, features="html.parser")

        # Extract teams and their stats
        teams = [row.get_text() for row in soup.find_all("span", class_="hide-mobile")]
        stats = [stat.get_text() for stat in soup.find_all("span", class_="stat-cell")]

        # Extract standings (assumes standings are in order of appearance)
        standings = list(range(1, len(teams) + 1))

        # Write data to CSV with standings included
        for i, team in enumerate(teams):
            stats_for_team = stats[i*8:(i+1)*8]
            writer.writerow([standings[i], team] + stats_for_team + [year])

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)