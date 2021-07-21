# tennis_elo_scraper

Scrape elo rating for tennis players from [tennisabstract.com](http://tennisabstract.com/) and save them as csv file.

Update on every monday automatically by github actions.

## Build Docker Image

Clone this repository and run below command

`$ docker build . -t tennis_elo_scraper`

## Get ELO rating and save to csv file

`$ docker run --rm -v ${PWD}:/app tennis_elo_scraper python main.py`

## Github Actions

To enable github actions, set `EMAIL` and `USERNAME` secrets value to the repository.
Or, remove `.github/workflows/schedule.yml` to disable github actions.
