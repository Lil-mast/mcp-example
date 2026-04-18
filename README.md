# mcp-example

A simple MCP (Model Context Protocol) server built with FastMCP, demonstrating how to expose custom tools to AI assistants.

## What This Repo Is About

This project provides a minimal example of creating an MCP server using the `fastmcp` library. It exposes a single tool (`greet`) that AI assistants can call to generate personalized greetings.

The MCP protocol allows AI assistants to interact with external tools and data sources in a standardized way.

## Requirements

- Python 3.10+
- `uv` - A fast Python package manager and runner
- `fastmcp` library

## Installation

### Install uv (if you don't have it)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup the Project

```bash
# Create a virtual environment
uv venv

# Install dependencies
uv pip install fastmcp
```

## How to Run the Server

### Development Mode with MCP Inspector

Use the built-in MCP Inspector to test your server:

```bash
uv run fastmcp dev inspector server.py
```

This will start the MCP Inspector UI where you can interact with your tools:

![MCP Inspector](mcp-inspector.png)

### Production Mode (SSE transport)

```bash
uv run server.py --transport sse --port 8000
```

## Available Tools

- **`greet(name: str)`** - Returns a personalized greeting message
- **`calculate(expression: str)`** - Evaluates a mathematical expression (e.g., "2 + 2 * 3")
- **`get_current_time()`** - Returns the current date and time

## Available Resources

- **`config://app`** - Returns the application configuration (version, name)

## Available Prompts

- **`greeting_prompt(name: str)`** - Creates a warm greeting prompt for the user

## Connect to Claude Desktop

To use your MCP server with Claude Desktop:

1. **Install Claude Desktop** from [claude.ai/download](https://claude.ai/download)

2. **Find your configuration file:**
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

3. **Add your MCP server to the configuration:**

```json
{
  "mcpServers": {
    "hello-mcp": {
      "command": "uv",
      "args": [
        "run",
        "--cwd",
        "C:\\Users\\admin\\desktop\\mcp-example",
        "server.py"
      ]
    }
  }
}
```

4. **Restart Claude Desktop** - Your tools will now be available in conversations!

---

## Next Steps

### Debugging the MCP Server with Claude

If your tools don't appear in Claude Desktop:

1. **Check the MCP server logs** in Claude Desktop:
   - Open Claude → **Settings** → **Developer** → **MCP Servers**
   - Look for error messages under `hello-mcp`

2. **Verify the server starts manually**:
   ```bash
   uv run server.py
   ```
   Should show: `Uvicorn running on http://127.0.0.1:8000`

3. **Test with MCP Inspector** (no API key needed):
   ```bash
   npx @modelcontextprotocol/inspector uv run server.py
   ```
   Then open the URL shown and manually test your tools.

4. **Common issues**:
   - Config file in wrong location (must be `%APPDATA%\Claude\claude_desktop_config.json` on Windows)
   - Path to project directory is incorrect
   - `uv` not in PATH for Claude Desktop process
   - Firewall blocking localhost connections

5. **Enable verbose logging**:
   Add `"env": { "LOG_LEVEL": "debug" }` to your mcp server config.

### Integrating a Voice Agent

To build a voice-activated agent that uses your MCP server:

**Architecture Overview:**

```
[Voice Input] → [STT: Whisper/Deepgram] → [LLM + MCP Tools] → [TTS: ElevenLabs/OpenAI] → [Voice Output]
```

**Option A: Local Voice Agent (Python)**

Install dependencies:
```bash
uv pip install openai-whisper speechrecognition pyttsx3 pyaudio sounddevice
```

Create `voice_agent.py`:
```python
import whisper
import speech_recognition as sr
import openai
from openai import OpenAI
import sounddevice as sd
import numpy as np

# Load your MCP server via stdio or HTTP
MCP_SERVER_URL = "http://localhost:8000/sse"

class VoiceAgent:
    def __init__(self):
        self.stt = whisper.load_model("base")
        self.recognizer = sr.Recognizer()
        self.tts_client = OpenAI()  # For TTS
        
    def listen(self):
        """Capture audio from microphone"""
        with sr.Microphone() as source:
            audio = self.recognizer.listen(source)
            return audio
    
    def transcribe(self, audio):
        """Speech to text"""
        text = self.recognizer.recognize_whisper(audio)
        return text
    
    def think(self, text):
        """Send to LLM with MCP tools enabled"""
        # Connect to your MCP server and use tools
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": text}],
            tools=[mcp_tools],  # Your MCP tools here
        )
        return response.choices[0].message.content
    
    def speak(self, text):
        """Text to speech"""
        response = self.tts_client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        # Play audio
        
    def run(self):
        while True:
            audio = self.listen()
            text = self.transcribe(audio)
            reply = self.think(text)
            self.speak(reply)

if __name__ == "__main__":
    agent = VoiceAgent()
    agent.run()
```

**Option B: Web-Based Voice Agent**

Use the Web Speech API + your HTTP-exposed MCP server:

```javascript
// Frontend voice agent
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.onresult = async (event) => {
  const transcript = event.results[0][0].transcript;
  
  // Send to backend with MCP server connection
  const response = await fetch('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ message: transcript })
  });
  
  const reply = await response.json();
  speak(reply.text); // Web Speech API TTS
};

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.speak(utterance);
}
```

**Option C: Existing Frameworks**

- **LiveKit Agents**: https://github.com/livekit/agents
- **VAPI**: https://vapi.ai (managed)
- **Retell**: https://retellai.com (managed)

**Testing Your Voice Agent:**

1. Start your MCP server: `uv run server.py`
2. Start ngrok for remote access: `ngrok http 8000`
3. Update your voice agent to use the ngrok URL
4. Speak a command: "What time is it?" or "Calculate 15 times 23"
5. Verify the agent calls your MCP tools and responds verbally

**Cost-Effective Options (Free Tiers):**
- STT: Whisper (local, free) or AssemblyAI ($50 credit free)
- LLM: Ollama (local, free) or OpenRouter (pay-as-you-go)
- TTS: Piper TTS (local, free) or Coqui TTS
