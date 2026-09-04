# lang-graph-course

Follow-along code from a LangGraph course. Each sub-folder is a small, self-contained agent
built to practice one LangGraph idea: how state moves between nodes, how conditional edges
decide when a loop stops, and how to compile and run a graph against a real LLM. The code is
kept deliberately short so the graph structure stays readable.

## Projects

### reflection_agent_social_media_post

Builds a reflection agent that writes a tweet, critiques its own draft, and rewrites it. It
demonstrates the generate/reflect loop pattern on top of LangGraph's `MessageGraph`, where the
graph state is just a list of chat messages.

The graph has two nodes:

- `generate` (`generation_node`) runs `generate_chain`, a prompt that plays a Twitter tech
  influencer writing the post. It is the entry point.
- `reflect` (`reflection_node`) runs `reflect_chain`, a prompt that plays a viral influencer
  grading the tweet and returning critique on length, virality, and style. The critique is
  wrapped in a `HumanMessage` so the generator treats it as feedback from a person.

Edges: a conditional edge off `generate` calls `should_continue`, which ends the run once the
message list is longer than 6 and otherwise routes to `reflect`. A plain edge sends `reflect`
back to `generate`. That gives roughly three generate/reflect rounds before the graph stops.

Both chains use `ChatOpenAI` with `gpt-3.5-turbo`, wired in `chains.py`.

Running it prints the graph as Mermaid, then invokes it with a hardcoded prompt
("you should learn langchain and langraph to be more productive"). The final response is
assigned but not printed, so to see the tweet you need to print `response` yourself.

Run it:

```bash
cd reflection_agent_social_media_post
poetry install
cp .env-template .env   # then fill in the values
poetry run python main.py
```

Environment variables (see `.env-template`):

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Required. Used by `ChatOpenAI` for both chains. |
| `LANGCHAIN_API_KEY` | LangSmith tracing key. |
| `LANGCHAIN_TRACING_V2` | Set to `true` to send traces to LangSmith. |
| `LANGCHAIN_PROJECT` | LangSmith project name. |

Only `OPENAI_API_KEY` is read directly in the code. The `LANGCHAIN_*` variables are picked up
by LangChain itself when tracing is on, and the run works without them.

The sub-project has its own `README.md`, but it is currently empty.

## Requirements

- Python 3.11 or newer
- [Poetry](https://python-poetry.org/) for dependency management
- An OpenAI API key

Dependencies are pinned per sub-project. `reflection_agent_social_media_post` uses
`langchain`, `langchain-openai`, `langgraph`, and `python-dotenv`, with `black` and `isort`
for formatting.

## Installation

```bash
git clone https://github.com/espin086/lang-graph-course.git
cd lang-graph-course/reflection_agent_social_media_post
poetry install
```

There is no dependency file at the repo root. Install from inside the sub-project you want to
run.

## License

MIT. See [LICENSE](LICENSE).
