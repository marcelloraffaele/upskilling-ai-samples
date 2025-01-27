# Assistants

## Assistant code interpreter
This script creates an AI assistant that can interpret code. It uploads a file, creates an assistant, and runs a thread to process a user query about plotting a graph from the file data.

```powershell
py .\1.assistant-code-interpreter.py
```

## Assistant function calling
This script creates an AI assistant that can call functions. It includes an example function get_weather and demonstrates how the assistant can use this function to answer user queries about the weather.
```powershell
py .\2.assistant-function-calling.py
```



## cleane all assitants we have created
This script deletes all assistants and files created by the Azure OpenAI Service. It lists the files and assistants, prompts the user for confirmation, and proceeds with deletion if confirmed.
```powershell
py .\99.assitant-cleaner.py
```

