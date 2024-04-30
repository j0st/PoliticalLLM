# PoliticalLLM: Framework for Measuring Political Ideologies in LLMs
<p align="center">
  <img src="img/example_tests.png" alt="Wahl-O-Mat and PCT example" width="700"/>
</p>

Code and demo for the master's thesis _“Steering Large Language Models towards Political Ideologies on Prompt-Level”_.

## Quickstart
Clone the repo.

`git clone https://github.com/j0st/master-thesis/`

Navigate to \PoliticalLLM and install dependencies from there.

`pip install -r requirements.txt`

To run this project with API models, you will need to add the following environment variables to your `.env` file. Create this file in the root directory of the project. By default, [OpenAI](https://openai.com/blog/openai-api), [together.ai](https://www.together.ai/products#inference) and [Anyscale](https://www.anyscale.com/endpoints) API endpoints are integrated.
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

Testing can be done in a new Python file or in the existing `main.py`. After importing the LLM class from this project, you can create an instance with the desired LLM and call the ideology test methods. Possible arguments and explanations can be found here.
```python
# main.py

from llms import LLM

ChatGPT = LLM("gpt-3.5-turbo-0125")

ChatGPT.wahlomat(filename="YOUR_FILENAME", plot_results=True)
ChatGPT.pct(filename="YOUR_FILENAME", plot_results=True)
```

After finishing the tests, the following files are created in the results folder:

* `responses-YOUR_FILENAME.csv` -> Lists all (mapped) responses from the LLM to each political statement
* `descriptives-YOUR_FILENAME.csv` -> Descriptive stats for each statement answered by the LLM
* `plot-YOUR_FILENAME.png` -> Plot for the results

## Project Files Description

<ul>
  <li><b>main.py</b> - Used to run experiments with LLMs.</li>
  <li><b>llms.py</b> - Base class for implementing LLMs and ideology tests as methods.</li>
  <li><b>pct.py</b> - Selenium script to run the PCT test.</li>
  <li><b>wahlomat.py</b> - Calculates the agreement scores between parties.</li>
  <li><b>retriever.py</b> - Retrieves top k statement from manifesto database</li>
</ul>

### Some other supporting files
<ul>
  <li><b>map_answers.py</b> - Maps the answers from an LLM to the ideology tests (e.g. "Agree") to int values which are needed to do the ideology test.</li>
  <li><b>descriptives.py</b> - Calculates the mean, median, mode and std in the list of responses provided after iterating through the statements.</li>
  <li><b>pct_plot_spectrum.py</b> - Plots the PCT coordinates on a two-dimensional spectrum.</li>
  <li><b>wahlomat_radar_chart.py</b> - Plot the Wahl-O-Mat agreements scores between parties on a radar chart.</li>
  <li><b>chunking.py</b> - Chunks manifesto data for embedding model.</li>
  <li><b>embeddings.py</b> - Creates Chroma.db embeddings from manifesto dataset</li>
  <li><b>synthetic_dataset.py</b> - Generates a synthetic QA pair dataset.</li>
  <li><b>evaluation.py</b> - Evaluates embedding model against validation synthetic dataset.</li>
  <li><b>fine_tuning.ipynb</b> - Script for fine-tuning embedding model</li>
  <li><b>manifesto_project.py</b> - Get manifesto data from Manifesto Project API</li>
</ul>

## Supported Models

- [gpt-3.5-turbo-0125](https://platform.openai.com/docs/models/gpt-3-5-turbo)
- [Mixtral-8x7B-Instruct-v0.1](https://huggingface.co/mistralai/Mixtral-8x7B-Instruct-v0.1)
- [Qwen1.5-14B-Chat](https://huggingface.co/Qwen/Qwen1.5-14B-Chat)

## More Models
