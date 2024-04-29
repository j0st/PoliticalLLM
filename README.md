# PoliticalLLM: Framework for Measuring Political Ideologies in LLMs
<p align="center">
  <img src="img/example_tests.png" alt="Wahl-O-Mat and PCT example" width="700"/>
</p>

Code and demo for the master's thesis _“Steering Large Language Models towards Political Ideologies on Prompt-Level”_.

## Quickstart
Clone the repo.

`git clone https://github.com/j0st/master-thesis/`

Navigate to PoliticalLLM/ and install dependencies from there.

`pip install -r requirements.txt`

To run this project with API models, you will need to add the following environment variables to your `.env` file. Create this file in the root directory of the project.
```plaintext
# .env file

# Models
OPENAI_API_KEY=

ANYSCALE_API_KEY=
ANYSCALE_BASE_URL="https://api.endpoints.anyscale.com/v1"

TOGETHER_AI_API_KEY=
TOGETHER_AI_BASE_URL="https://api.together.xyz/v1"

# Set this if you want to use your own llama.cpp model locally
LOCAL_LLAMA_MODEL_PATH=

# Data
MANIFESTO_PROJECT_API_KEY=
```

Go to main.py and create an instance of an LLM and start testing.

Results are saved in results/

## Project Files Description

## More Models
