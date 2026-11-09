# Ollama samples

This sample uses Ollama's OpenAI-compatible API with the existing `openai`
and `python_dotenv` dependencies. No Azure credentials are needed.

1. Install [Ollama](https://ollama.com/) and make sure it is running.
   If it is not already running, start it with `ollama serve`.
2. Download the default model:

   ```powershell
   ollama pull llama3.2
   ```

3. Optionally configure `18.ollama\.env`:

   ```dotenv
   OLLAMA_BASE_URL=http://localhost:11434/v1
   OLLAMA_MODEL=llama3.2
   ```

   To use another model, pull it with `ollama pull <model>` and set
   `OLLAMA_MODEL` to the same name.

4. From the repository root, activate your virtual environment and run:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   python .\18.ollama\1.faq-chat.py
   ```

Type `exit` to end the conversation.

## Timezone function calling

Run the timezone sample with the same environment activated:

```powershell
python .\18.ollama\2.Timezone.py
```

This sample uses the same `OLLAMA_BASE_URL` and `OLLAMA_MODEL` settings.
Use a model that supports tools, such as the default `llama3.2`.
It asks for the current time in San Francisco, Tokyo, and Rome, executes
the requested `get_current_time` tool calls locally, and sends the results
back to Ollama for the final answer. Paris is also supported by the tool.
