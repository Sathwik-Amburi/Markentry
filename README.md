# Markentry
Multi-Agent RAG System for Market Entry Strategic Development

## How to install the project
1. clone the repo locally
```bash
$ git clone https://github.com/Sathwik-Amburi/Markentry.git
```
2. go into the project
```bash
$ cd Markentry
```
3. Set the python interpreter to ./.venv/bin/python
4. Install [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
5. Install project dependencies
```
$ poetry install
```

## Add a data folder for RAG
1. create a folder called data in Markentry/markentry
```bash
$ cd markentry
$ mkdir data
```
2. Add the data files from the drive.

## How to run the project
1. create a copy of the .env.example file
2. rename the copy to .env
3. add dotenv to your local poetry instance
```bash
$ poetry self add poetry-dotenv-plugin
```
4. change the api key for OPENAI_API_KEY to your key
5. run to execute a test run
```bash
$ poetry run main
```
6. to check the generated report in website
$ streamlit run streamlit.py


## Citation
Please cite this repo as follows:
```
Beckenbauer, L.; Grosser, M.; Moreira, D. Jr.; Haverland, T. (2024). Orchestrator Multi-Agent App (Version 0.0.1).
```
