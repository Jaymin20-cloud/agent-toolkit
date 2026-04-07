# Agent Toolkit

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

A full toolkit for running an AI agent service built with LangGraph, FastAPI and Streamlit.

It includes a [LangGraph](https://langchain-ai.github.io/langgraph/) agent, a [FastAPI](https://fastapi.tiangolo.com/) service to serve it, a client to interact with the service, and a [Streamlit](https://streamlit.io/) app that uses the client to provide a chat interface. Data structures and settings are built with [Pydantic](https://github.com/pydantic/pydantic).

This repository extends the [agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit) template with a **Vercel-compatible** FastAPI entrypoint (`server.py` at the repo root) and optional slim deploy files (`requirements-vercel.txt`, `vercel.json`).

**[Video walkthrough of the upstream template](https://www.youtube.com/watch?v=pdYVHw_YCNY)**

## Overview

### API docs (local)

With the service running (`python src/run_service.py` or Docker), open **`http://localhost:8080/docs`** or **`/redoc`** for interactive OpenAPI. A public “try it” deployment link will be added back to this README once hosting is stable.

### Streamlit chat UI

The chat UI is normally run **locally** (`streamlit run src/streamlit_app.py`) or on [Streamlit Community Cloud](https://streamlit.io/cloud) with `AGENT_URL` pointing at your API.

<img src="media/app_screenshot.png" width="600" alt="Streamlit chat UI (run locally)">

### Quickstart

Run directly in python

```sh
# At least one LLM API key is required
echo 'OPENAI_API_KEY=your_openai_api_key' >> .env

# uv is the recommended way to install agent-service-toolkit, but "pip install ." also works
# For uv installation options, see: https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/0.7.19/install.sh | sh

# Install dependencies. "uv sync" creates .venv automatically
uv sync --frozen
source .venv/bin/activate
python src/run_service.py

# In another shell
source .venv/bin/activate
streamlit run src/streamlit_app.py
```

Run with docker

```sh
echo 'OPENAI_API_KEY=your_openai_api_key' >> .env
docker compose watch
```

### Architecture Diagram

<img src="media/agent_architecture.png" width="600">

### Key Features

1. **LangGraph Agent and latest features**: A customizable agent built using the LangGraph framework. Implements the latest LangGraph v1.0 features including human in the loop with `interrupt()`, flow control with `Command`, long-term memory with `Store`, and `langgraph-supervisor`.
1. **FastAPI Service**: Serves the agent with both streaming and non-streaming endpoints.
1. **Advanced Streaming**: A novel approach to support both token-based and message-based streaming.
1. **Streamlit Interface**: Provides a user-friendly chat interface for interacting with the agent, including voice input and output.
1. **Multiple Agent Support**: Run multiple agents in the service and call by URL path. Available agents and models are described in `/info`
1. **Asynchronous Design**: Utilizes async/await for efficient handling of concurrent requests.
1. **Content Moderation**: Implements Safeguard for content moderation (requires Groq API key).
1. **RAG Agent**: A basic RAG agent implementation using ChromaDB - see [docs](docs/RAG_Assistant.md).
1. **Feedback Mechanism**: Includes a star-based feedback system integrated with LangSmith.
1. **Docker Support**: Includes Dockerfiles and a docker compose file for easy development and deployment.
1. **Testing**: Includes robust unit and integration tests for the full repo.

### Key Files

The repository is structured as follows:

- `src/agents/`: Defines several agents with different capabilities
- `src/schema/`: Defines the protocol schema
- `src/core/`: Core modules including LLM definition and settings
- `src/service/service.py`: FastAPI service to serve the agents
- `src/client/client.py`: Client to interact with the agent service
- `src/streamlit_app.py`: Streamlit app providing a chat interface
- `tests/`: Unit and integration tests

## Changelog

Updates in this workspace compared to the baseline [agent-service-toolkit](https://github.com/JoshuaC215/agent-service-toolkit) template:

| Area | Change |
|------|--------|
| `src/service/service.py` | The FastAPI app now sets **OpenAPI metadata**: `title` (“Agent service”), `description` (short summary of the HTTP API), and `version` (`0.1.0`). This appears in Swagger UI (`/docs`), ReDoc (`/redoc`), and any OpenAPI clients. **No change** to routes, handlers, status codes, or JSON response shapes. |
| `server.py` (repo root) | **Vercel entrypoint**: exposes the same `app` as `run_service.py`, after adding `src/` to `sys.path` so imports match local development. Required for Vercel’s FastAPI detection ([docs](https://vercel.com/docs/frameworks/backend/fastapi)). |
| `src/server.py`, `api/index.py` | Extra entrypoints for the same `app` if Vercel’s **Root Directory** is `src` or if the builder prefers the `api/` layout. |
| `README.md` | Project-specific notes and changelog; public demo link removed until hosting is stable. |
| `requirements-vercel.txt` + `vercel.json` | **Slim pip install** for Vercel: skips Streamlit, ONNX, Pandas/PyArrow, Chroma, Postgres/Mongo drivers, and extra LangChain vendor packages so the deployment is far smaller (targeting the [function bundle limit](https://vercel.com/docs/functions/limitations)). |
| `AGENT_TOOLKIT_SLIM=1` | When set (included in `vercel.json` for Vercel), only the **`chatbot`** agent is registered so imports match the slim dependency set. Full Docker/local installs omit this variable to load every agent. |
| `src/memory/__init__.py`, `src/core/llm.py`, `src/service/service.py` | **Lazy imports** for DB backends (Postgres/Mongo/SQLite), LLM providers, and Langfuse so unused options are not loaded at import time—smaller memory and fewer optional wheels on minimal installs. |

### Deploying the FastAPI service on Vercel

1. This repo ships **`vercel.json`** with `installCommand: pip install -r requirements-vercel.txt` so Vercel does **not** install the full `pyproject.toml` dependency set (which is far above typical serverless limits). [FastAPI on Vercel](https://vercel.com/docs/frameworks/backend/fastapi).
2. **`AGENT_TOOLKIT_SLIM=1`** is set in `vercel.json` for production/preview runtimes. That exposes only the **`chatbot`** agent and matches the slim requirements. Use **`OPENAI_API_KEY`** and keep the default OpenAI model (or set **`DEFAULT_MODEL`** to an OpenAI enum your app supports). To use Anthropic, Google, etc. on Vercel you must add the matching packages to `requirements-vercel.txt` and turn off slim mode (or extend the slim list carefully).
3. **Root Directory** should be the repository root (empty). If it is set to `src`, use the included **`src/server.py`** entrypoint. If the build says **“No fastapi entrypoint found”**, redeploy without cache and confirm `server.py` exists on `main`.
4. In **Project → Settings → Environment Variables**, set **`OPENAI_API_KEY`**, **`SQLITE_DB_PATH=/tmp/checkpoints.db`**, and any other vars from [`.env.example`](./.env.example) you need. Redeploy after changes.

Vercel runs your API as a **single serverless function**; cold starts, execution time limits, and bundle size still apply. If the slim build is **still** over the limit, use Docker, Fly.io, Railway, or a VM for the full dependency graph.

## Setup and Usage

1. Clone the repository:

   ```sh
   git clone https://github.com/Jaymin20-cloud/agent-toolkit.git
   cd agent-toolkit
   ```

2. Set up environment variables:
   Create a `.env` file in the root directory. At least one LLM API key or configuration is required. See the [`.env.example` file](./.env.example) for a full list of available environment variables, including a variety of model provider API keys, header-based authentication, LangSmith tracing, testing and development modes, and OpenWeatherMap API key.

3. You can now run the agent service and the Streamlit app locally, either with Docker or just using Python. The Docker setup is recommended for simpler environment setup and immediate reloading of the services when you make changes to your code.

### Additional setup for specific AI providers

- [Setting up Ollama](docs/Ollama.md)
- [Setting up VertexAI](docs/VertexAI.md)
- [Setting up RAG with ChromaDB](docs/RAG_Assistant.md)

### Building or customizing your own agent

To customize the agent for your own use case:

1. Add your new agent to the `src/agents` directory. You can copy `research_assistant.py` or `chatbot.py` and modify it to change the agent's behavior and tools.
1. Import and add your new agent to the `agents` dictionary in `src/agents/agents.py`. Your agent can be called by `/<your_agent_name>/invoke` or `/<your_agent_name>/stream`.
1. Adjust the Streamlit interface in `src/streamlit_app.py` to match your agent's capabilities.


### Handling Private Credential files

If your agents or chosen LLM require file-based credential files or certificates, the `privatecredentials/` has been provided for your development convenience. All contents, excluding the `.gitkeep` files, are ignored by git and docker's build process. See [Working with File-based Credentials](docs/File_Based_Credentials.md) for suggested use.


### Docker Setup

This project includes a Docker setup for easy development and deployment. The `compose.yaml` file defines three services: `postgres`, `agent_service` and `streamlit_app`. The `Dockerfile` for each service is in their respective directories.

For local development, we recommend using [docker compose watch](https://docs.docker.com/compose/file-watch/). This feature allows for a smoother development experience by automatically updating your containers when changes are detected in your source code.

1. Make sure you have Docker and Docker Compose (>= [v2.23.0](https://docs.docker.com/compose/release-notes/#2230)) installed on your system.

2. Create a `.env` file from the `.env.example`. At minimum, you need to provide an LLM API key (e.g., OPENAI_API_KEY).
   ```sh
   cp .env.example .env
   # Edit .env to add your API keys
   ```

3. Build and launch the services in watch mode:

   ```sh
   docker compose watch
   ```

   This will automatically:
   - Start a PostgreSQL database service that the agent service connects to
   - Start the agent service with FastAPI
   - Start the Streamlit app for the user interface

4. The services will now automatically update when you make changes to your code:
   - Changes in the relevant python files and directories will trigger updates for the relevant services.
   - NOTE: If you make changes to the `pyproject.toml` or `uv.lock` files, you will need to rebuild the services by running `docker compose up --build`.

5. Access the Streamlit app by navigating to `http://localhost:8501` in your web browser.

6. The agent service API will be available at `http://0.0.0.0:8080`. You can also use the OpenAPI docs at `http://0.0.0.0:8080/redoc`.

7. Use `docker compose down` to stop the services.

This setup allows you to develop and test your changes in real-time without manually restarting the services.

### Building other apps on the AgentClient

The repo includes a generic `src/client/client.AgentClient` that can be used to interact with the agent service. This client is designed to be flexible and can be used to build other apps on top of the agent. It supports both synchronous and asynchronous invocations, and streaming and non-streaming requests.

See the `src/run_client.py` file for full examples of how to use the `AgentClient`. A quick example:

```python
from client import AgentClient
client = AgentClient()

response = client.invoke("Tell me a brief joke?")
response.pretty_print()
# ================================== Ai Message ==================================
#
# A man walked into a library and asked the librarian, "Do you have any books on Pavlov's dogs and Schrödinger's cat?"
# The librarian replied, "It rings a bell, but I'm not sure if it's here or not."

```

### Development with LangGraph Studio

The agent supports [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/), the IDE for developing agents in LangGraph.

`langgraph-cli[inmem]` is installed with `uv sync`. You can simply add your `.env` file to the root directory as described above, and then launch LangGraph Studio with `langgraph dev`. Customize `langgraph.json` as needed. See the [local quickstart](https://langchain-ai.github.io/langgraph/cloud/how-tos/studio/quick_start/#local-development-server) to learn more.

### Local development without Docker

You can also run the agent service and the Streamlit app locally without Docker, just using a Python virtual environment.

1. Create a virtual environment and install dependencies:

   ```sh
   uv sync --frozen
   source .venv/bin/activate
   ```

2. Run the FastAPI server:

   ```sh
   python src/run_service.py
   ```

3. In a separate terminal, run the Streamlit app:

   ```sh
   streamlit run src/streamlit_app.py
   ```

4. Open your browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## Projects built with or inspired by agent-service-toolkit

The following are a few of the public projects that drew code or inspiration from this repo.

- **[PolyRAG](https://github.com/QuentinFuxa/PolyRAG)** - Extends agent-service-toolkit with RAG capabilities over both PostgreSQL databases and PDF documents.
- **[alexrisch/agent-web-kit](https://github.com/alexrisch/agent-web-kit)** - A Next.JS frontend for agent-service-toolkit
- **[raushan-in/dapa](https://github.com/raushan-in/dapa)** - Digital Arrest Protection App (DAPA) enables users to report financial scams and frauds efficiently via a user-friendly platform.

**Please create a pull request editing the README or open a discussion with any new ones to be added!** Would love to include more projects.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Currently the tests need to be run using the local development without Docker setup. To run the tests for the agent service:

1. Ensure you're in the project root directory and have activated your virtual environment.

2. Install the development dependencies and pre-commit hooks:

   ```sh
   uv sync --frozen
   pre-commit install
   ```

3. Run the tests using pytest:

   ```sh
   pytest
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
