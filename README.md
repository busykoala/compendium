# LLM for Compendium

This is a simple implementation of the LLM algorithm for the Compendium dataset. The dataset.

## Installation

```bash
poetry install
```

## Usage

1. Place the Compendium dataset in `./data/compendium.txt`
2. Export `OPENAI_API_KEY` with your OpenAI API key.
3. Run the following command:

```bash
poetry run python run.py
```

To configure the models for the embeddings or chat, edit the config
in `./compendium/config.py`.
