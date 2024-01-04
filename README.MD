# Run App
Install requirements. Get .env from Allen
```bash
$ python -m venv .venv
$ source .venv/bin/activate (OR source .venv/Scripts/activate if using Windows)
$ pip install -r requirements.txt
```
Run the app
```
flask --app app run
```


# Repo Description
This repo is split into 3 main sections: a Flask app in the `/app` folder, scraping functions in the `/scrapers` folder, and tests in the `/tests` folder. The scraping functions scrape the Mouser circular connectors and produce a JSON file to populate the Flask app database. The Flask app serves the web app where the user can compare parts and search for parts.

Scrapers use Playwright to scrape the Mouser circular connectors to tables, open the relevant links to get part details,  and return part info from the part details page. Browser context cookies are needed for mouser.com, so if you run `scrapers/main.py`, make sure that `cookies.csv` contains fresh cookies. 

The Flask app uses MongoDB as a data store and a vector store. Run `app/init_db.py` to populate the database. The data from the scrapers is inserted into a Mongo collection, and embeddings on the data are stored in another Mongo collection. In the Mongo console I created a vector search index to query embeddings. The Flask app uses Llamaindex throughout the app to interface Mongo, OpenAI, etc. 

There's one test right now that checks that output for the `/substitute/` endpoint is as expected. 


