# Framework for Measuring Political Ideologies in LLMs

Master's thesis...

## Quickstart
Clone the repo.

`git clone https://github.com/j0st/master-thesis/`.

Install dependencies

`pip install -r requirements.txt`.

To run this project with API models, you will need to add the following environment variables to your `.env` file. Create this file in the root directory of the project.
```plaintext
# .env file
# Models
OPENAI_API_KEY=

ANYSCALE_API_KEY=
ANYSCALE_BASE_URL=

TOGETHER_AI_API_KEY=
TOGETHER_AI_BASE_URL=

# Data
MANIFESTO_PROJECT_API_KEY=
```

Go to main.py and create an instance of an LLM and start testing.

Results are saved in results/
