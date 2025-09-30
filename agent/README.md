## Local Agent

Minimal local agent that can use tools (shell, filesystem, web), reason with an OpenAI model, and loop until the goal is achieved or max steps are reached.

### Setup

1. Python 3.10+
2. Create and activate a virtualenv (recommended)
3. Install dependencies
4. Set environment variables

```bash
cd /workspace/agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your `OPENAI_API_KEY` and optional `OPENAI_MODEL`.

### Run

```bash
python -m agent.cli "List current directory and summarize files" --tools shell.run,fs.list_dir
```

### Tools

- shell.run: Run non-interactive shell commands
- fs.read_file / fs.write_file / fs.list_dir
- web.search / web.get

### Notes

- Tool calls use a simple JSON protocol: `{ "tool": string, "args": object }`.
- The agent automatically appends tool results back into the conversation.
