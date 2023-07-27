<img src="./assets/pdx.png" height="40">

# Hello, I'm PDX 👋

**PDX is a framework for prompt engineering and a dev-ops toolkit.**

At the core, it provides a mental-model on how to build and manage `agents`. An agent is a collection of prompts and/or prompt templates with information that is used to interact with the Language Models.

**Documentation**: [pdxlabs.io/docs](https://pdxlabs.io/docs)

**Website**: [pdxlabs.io](https://pdxlabs.io/)

**Quickstart**: [create-an-agent](https://pdxlabs.io/docs/getting-started/create-an-agent)

## Installation

```bash
pip install pdx
```

## Quickstart

To create your first agent, run the following command:

```bash
pdx create my_first_agent
```

Run and test out the agent by running:

```bash
pdx test my_first_agent --verbose
```

More information here: [PDX - Main Concepts](https://pdxlabs.io/docs/getting-started/main-concepts)

## Why use PDX?

-   🗃️ Low dependency footprint -> ease of production deployment and maintainance.
-   📂 Mental model to separate prompt templates from the application code. (Similar to Flask blueprint or FastAPI router).
-   📌 Version control the prompts along with their evaluation metrics.
-   📸 Logging and tracing of inputs, prompt render, and model response made easy.
-   🧯 Standardize Error handling and logging.
-   💾 Caching for lowering latency. (Coming soon)
-   📊 Observability out-of-the-box. (Coming soon)
-   📩 Log feedback of the user. (Coming soon)
-   🛎️ A/B testing of prompts. (Coming soon)

## [Demos](https://github.com/pdx-labs/demos)

Check our the demos in the [demos repository](https://github.com/pdx-labs/demos).

## Models (APIs) currently supported:

-   OpenAI
-   Anthropic
