# LangGraph Time Bot 🤖⏰

A minimal stateless chat bot built with LangGraph that can tell you the current time using tool calling.

## Features

- **Stateless chat**: Each message is processed independently
- **Tool calling**: Uses `get_current_time` tool when asked about time
- **Multiple model support**: OpenAI (default), Ollama, Gemini, DeepSeek
- **LangGraph dev ready**: Launch with `langgraph dev`

## Quick Start

### 1. Clone and Setup

```bash
git clone <your_repo>
cd langgraph-time-bot
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Model Provider

Create a `.env` file in the project root with your chosen model provider:

#### Option A: OpenAI (Default)
```bash
# Create .env file
echo "OPENAI_API_KEY=your-openai-api-key" > .env
```

#### Option B: Ollama (Local)
```bash
# Install Ollama: https://ollama.ai/
ollama pull llama3.2
# Default runs on http://localhost:11434

# Create .env file  
echo "# Using Ollama - no API key needed" > .env
```
Then uncomment the Ollama section in `app.py` and comment out OpenAI.

#### Option C: Google Gemini
```bash
pip install langchain-google-genai
echo "GOOGLE_API_KEY=your-gemini-api-key" > .env
```
Then uncomment the Gemini section in `app.py`.

#### Option D: DeepSeek
```bash
echo "DEEPSEEK_API_KEY=your-deepseek-api-key" > .env
```
Then uncomment the DeepSeek section in `app.py`.

### 4. Launch

#### With LangGraph Dev (Recommended)
```bash
langgraph dev
```
🚀 This will start the server at `http://localhost:2024` and open LangGraph Studio!

#### Direct Python Run (Testing)
```bash
python app.py
```

## Usage

Once running with `langgraph dev`:
1. Open LangGraph Studio in your browser (auto-opens)
2. Create a new thread 
3. Ask questions like:
   - "What time is it?"
   - "Can you tell me the current time?"
   - "What's the time right now?"

The bot will automatically call the `get_current_time` tool and return the current UTC time in ISO-8601 format.

## Example Interaction

```
You: What time is it?
Bot: The current UTC time is 2025-01-21T06:42:00Z.

You: Thanks!
Bot: You're welcome! Is there anything else you'd like to know?
```

## Project Structure

```
langgraph-time-bot/
├── app.py              # Main LangGraph application
├── requirements.txt    # Python dependencies
├── langgraph.json     # LangGraph configuration
├── .env               # Environment variables (you create this)
└── README.md          # This file
```

## How It Works

1. **LangGraph State**: Uses `MessagesState` to track conversation
2. **Tool Integration**: `get_current_time` tool bound to the language model
3. **Conditional Flow**: Agent decides when to call tools vs. respond directly
4. **Stateless Design**: Each conversation turn is independent

## Troubleshooting

### Model Provider Issues
- **OpenAI**: Ensure `OPENAI_API_KEY` is set in `.env` and valid
- **Ollama**: Verify Ollama is running on port 11434 and model is pulled
- **Gemini**: Check `GOOGLE_API_KEY` in `.env` and install `langchain-google-genai`

### Common Errors
- **"No module named 'langgraph'"**: Run `pip install -r requirements.txt`
- **API key errors**: Double-check `.env` file contents
- **Connection errors**: Verify internet connection and service availability

### LangGraph Dev Issues
- **"langgraph: command not found"**: Install CLI with `pip install langgraph-cli`
- **Configuration errors**: Ensure `langgraph.json` is in project root
- **Port conflicts**: Use `langgraph dev --port 8080` to change port

## Development

To modify the bot:
1. Edit `app.py` for functionality changes
2. Update `requirements.txt` for new dependencies
3. Test with `python app.py` before using `langgraph dev`
4. The `langgraph dev` server has hot-reload enabled

## License

MIT License - feel free to use and modify as needed. 