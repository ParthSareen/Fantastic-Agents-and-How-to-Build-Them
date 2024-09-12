# Fantastic-Agents-and-How-to-Build-Them

<p align="center">
  <img src="image.webp" alt="Fantastic Agents and How to Build Them" width="300">
</p>

## Description
Dive into the elusive world of AI Agents and learn how to build them! There are so many frameworks, models, and practices to build them and the entire field is just getting started. In this workshop, we'll be building an agent to scrape and standardize data through a natural language interface.

## Installation

> Rye is not a necesary dependency but does make it **much** simpler. You can still create a virtual environment and install using the `requirements.lock` file

This project uses [Rye](https://rye-up.com/) for dependency management. Follow these steps to set up the project:

Instructions for installation on windows are on the Rye site

1. Install Rye if you haven't already:
   ```
   curl -sSf https://rye-up.com/get | bash
   ```

2. Clone the repository:
   ```
   git clone https://github.com/parthsareen/fantastic-agents-and-how-to-build-them.git
   cd fantastic-agents-and-how-to-build-them
   ```

3. Install dependencies using Rye:
   ```
   rye sync
   ```

This will create a virtual environment and install all the required dependencies specified in the `pyproject.toml` file.

4. Activate the virtual environment:
   ```
   . .venv/bin/activate
   ```

Now you're ready to start working on the project!


## API Key Setup

To use this project, you'll need to set up an API key for one of the following services:

### OpenAI API Key

1. Sign up for an account at [OpenAI](https://openai.com/).
2. Navigate to the [API keys page](https://platform.openai.com/account/api-keys).
3. Create a new secret key.
4. Set the API key as an environment variable:
   ```
   export OPENAI_API_KEY='your-api-key-here'
   ```

### Groq API Key

1. Sign up for an account at [Groq](https://console.groq.com/).
2. Navigate to the API keys section in your account settings.
3. Generate a new API key.
4. Set the API key as an environment variable:
   ```
   export GROQ_API_KEY='your-api-key-here'
   ```

### Ollama (Local Processing)

If you prefer to run models locally:

1. Install Ollama by following the instructions on the [Ollama website](https://ollama.ai/).
2. Pull the desired model:
   ```
   ollama pull llama3.1
   ```
3. No API key is required for Ollama, as it runs locally on your machine.

Choose the option that best suits your needs and ensure you have the necessary API key or local setup before proceeding with the workshop.

### Browserbase setup
To use Browserbase for web scraping and data processing, follow these steps:

1. Visit [Browserbase](https://www.browserbase.com/) and sign up for an account.
2. Once logged in, navigate to the settings page to find your API key.
3. Set the API key as an environment variable:
   ```
   export BROWSERBASE_API_KEY='your-api-key-here'
   ```
4. Use code `DEVTOOLS` for 1 free month - recommended if using browserbase for hackathon project.


## DAGent Basics

Source code and further reading: [DAGent GitHub repository](https://github.com/ParthSareen/DAGent/tree/main).


## Example Solutions

If you find yourself stuck or running short on time, you can refer to the finished versions of the examples:

1. Simple AI Agent: [simple_example_finished.py](src/fantastic_agents_and_how_to_build_them/simple_example_finished.py)
2. Complex AI Agent: [data_analysis_agent_finished.py](src/fantastic_agents_and_how_to_build_them/data_analysis_agent_finished.py)

These files contain the complete implementations of the agents we'll be building during the workshop. While it's recommended to work through the exercises on your own, these resources are available if you need additional guidance or want to compare your solution.

## Learning Outcomes
After this workshop, you will be able to:
- Conceptually understand the key components of AI Agents
- Learn why agents are so powerful
- Build an AI agent to scrape and standardize data

## Prerequisite Knowledge
- Familiarity with Python
- Using pip to manage dependencies

## Timeline
| Time | Module | Description |
|------|--------|-------------|
| 10 min | What are Agents | Learn what AI agents are, their anatomy, and why they're powerful |
| 10 min | Environment Setup | Learn how to setup and manage a Python environment for this project |
| 15 min | Simple AI Agent | We'll learn the basics of DAGent and build a simple AI agent |
| 30 min | Complex AI Agent | Build a complex AI Agent to process more data and interface with natural language | 

## Workshop Lead Contact
Parth Sareen
parth@extensible.dev
