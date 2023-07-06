# doc-similarity-mock

- Prerequisites
    1. postgresql
    2. python3.10
    3. pip
    4. python-venv

- Create Virtual Environment
    `python3.10 -m venv venv`

- Activate Virtual Environemnt
    `source venv/bin/activate`

- Install Dependencies
    `pip3 install -r requirements.txt`

- Set Env Variables by copying sample-env and renaming it to .env

- Gdrive Access Method is OAuth, make sure you have your credentials file ready and placed in the project dir

- Execute code using following command
    `python3 main.py`

- After this you will be prompted twice
        1. Give the file_id to index embeddings and data from google drive file(txt file) (not required)
        2. Give promopt to search in the database

