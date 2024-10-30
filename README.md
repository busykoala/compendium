# LLM for Compendium

This is a simple implementation of the LLM algorithm for the Compendium dataset. The dataset.

## Installation

```bash
poetry install
```

## Create Embeddings

1. Place the Compendium dataset in `./data/compendium.txt`
2. Export `OPENAI_API_KEY` with your OpenAI API key.
3. Run the following command:

```bash
poetry run python ./create_vectorstore.py
```

## Usage

1. Place the Compendium dataset in `./data/compendium.txt`
2. Export `OPENAI_API_KEY` with your OpenAI API key.
3. Run the following command:

```bash
poetry run uvicorn main:app --reload
```

To configure the models for the embeddings or chat, edit the config
in `./compendium/config.py`.

## Docker

```
docker build -t compendium .
docker run -d -p 127.0.0.1:8000:8000 -e OPENAI_API_KEY=your_key -e PASSWORD=your_password compendium
```
