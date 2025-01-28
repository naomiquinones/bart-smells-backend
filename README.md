# bart-smells

Capstone project for Ada Developers Academy C15-Accelerate program. This MVP is the back end system that handles database connections to store users and their reports, including typical operations such as reading, writing, updating and deleting from the database.

## 2025 Update

Dependencies were updated, and notes were added to this README.

## Setup

Go to the [BART website](https://www.bart.gov/schedules/developers/api) to get an API key.

Make sure to have a database running. E.g. Postgres usually runs on port 5432.

In your .env file, specify the database and BART API key

```sh
DB_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/bart_smells
TEST_DB_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/bart_smells_test

BART_KEY=BART-API-KEY
```

## Running the project

Flask usually runs on port 5000.

```sh
flask run
```

**Note for Mac users**
On Macs, this port might be used by Airplay so specify an open port when running, e.g. 5001

```sh
flask run -p 5001
```

You'll notice that the front-end port number is set to 5173. If you change the port number that the front end runs on, you'll need to change the port number in the \_\_init__.py and routes.py files.
