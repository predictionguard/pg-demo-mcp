# Prediction Guard × MCP Demo

A minimal CLI demo showing how to connect [Prediction Guard's Responses API](https://docs.predictionguard.com/api-reference/api-reference/responses) to a remote **Model Context Protocol (MCP)** server. The agent uses a mock / demo Salesforce MCP server as its tool backend and maintains a running conversation in the terminal.

## What this shows

- How to pass MCP servers as tools via the `responses.create` API
- How to parse the Responses API output format (`output[].content[].text`)
- How to maintain multi-turn conversation history with the Responses API

## Prerequisites

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) (package manager)
- A Prediction Guard API key → [get one here](https://predictionguard.com)

## Setup

```bash
# 1. Clone the repo
git clone <repo-url>
cd pg-demo-mcp

# 2. Copy the env template and add your API key
cp .env_example .env
# Edit .env and set: PREDICTIONGUARD_API_KEY=<your key>

# 3. Install dependencies
uv sync
```

## Run

```bash
uv run python main.py
```

You'll see an interactive prompt:

```
=== GTM Agent | PredictionGuard + Salesforce ===
Type 'quit' to exit.

You: What does our renewal pipeline look like?

Agent: Here's a summary of upcoming renewals...
```

Type `quit` or `exit` (or press `Ctrl+C`) to stop.

## How it works

```python
client.responses.create(
    model="gpt-oss-120b",
    input=conversation,       # full conversation history
    tools=sf_tools_json,      # MCP server config
)
```

The `tools` list declares the MCP server — its URL, label, and which tools the model is allowed to call. Prediction Guard handles the MCP protocol; your code only sees the final text response.

### MCP tool config shape

```python
{
    "type": "mcp",
    "server_url": "https://your-mcp-server/mcp",
    "server_label": "my-mcp-server",
    "allowed_tools": ["tool_one", "tool_two"],
    "server_description": "What this server does"
}
```

## Project structure

```
main.py          # All demo logic
.env_example     # API key template
pyproject.toml   # Dependencies (managed by uv)
```
