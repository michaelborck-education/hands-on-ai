# Setting Up Ollama for Hands-On AI

This guide will walk you through setting up Ollama as a **local, privacy-focused** option for powering your Hands-On AI projects. 

> **Note**: HandsOnAI works with **any OpenAI-compatible provider** including OpenAI, OpenRouter, Together AI, and others. This guide focuses specifically on Ollama for users who want to run models locally.

---

## 🧭 Who Is This Guide For?

This guide is written for:
- **Beginners** who want to run Hands-On AI with local LLMs using [Ollama](https://ollama.com)
- **Educators** seeking privacy-focused solutions for classroom use
- **Students** who prefer not to send data to cloud providers
- **Anyone** who wants to understand how local LLMs work

If you're comfortable using cloud providers like OpenAI or OpenRouter, you can skip this guide and configure HandsOnAI with your preferred provider instead.

---

## 🌍 Ollama vs Other Providers

| Feature | Local Ollama | Cloud Providers |
|---------|--------------|----------------|
| **Privacy** | ✅ All data stays local | ❌ Data sent to external servers |
| **Cost** | ✅ Free after initial setup | ❌ Pay per token/request |
| **Internet** | ✅ Works offline | ❌ Requires internet connection |
| **Setup** | ⚠️ Requires installation | ✅ Just need API key |
| **Performance** | ⚠️ Limited by your hardware | ✅ High-end GPUs available |
| **Latest Models** | ⚠️ Community releases | ✅ Cutting-edge models first |


## What is Ollama?

Ollama is a lightweight tool that allows you to run large language models (LLMs) locally on your computer. It makes it easy to download and run models like Llama 3 without needing specialized hardware or complex setup.

## System Requirements

- **Windows, macOS, or Linux** computer
- At least **8GB RAM** (16GB+ recommended for better performance)
- At least **10GB** of free disk space
- An **internet connection** (for the initial model download)

## Installation Guide

### For macOS

1. Download the Ollama installer from [ollama.ai](https://ollama.ai)
2. Open the downloaded file and drag the Ollama app to your Applications folder
3. Launch Ollama from your Applications folder
4. Ollama will run in your menu bar (look for the llama icon)

### For Windows

1. Download the Windows installer from [ollama.ai](https://ollama.ai)
2. Run the installer and follow the on-screen instructions
3. Once installed, Ollama will start automatically and run in the system tray

### For Linux

1. Run the following command in your terminal:
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```
2. Start the Ollama service:
   ```bash
   ollama serve
   ```

## Downloading Your First Model

After installing Ollama, you'll need to download at least one model. For beginners, we recommend the `llama3` model, which offers a good balance of performance and quality.

1. Open a terminal or command prompt
2. Run the following command:
   ```bash
   ollama pull llama3
   ```
3. Wait for the download to complete (this may take a few minutes depending on your internet speed)

The first time you run this command, it will download the model files (about 4GB). Once downloaded, the model will be available locally on your computer.

## Testing Your Installation

Let's make sure everything is working properly:

1. In your terminal or command prompt, run:
   ```bash
   ollama run llama3 "Hello, how are you today?"
   ```
2. You should see a response from the model

If you received a response, congratulations! Ollama is set up correctly and ready to use with HandsOnAI.

## Using Ollama with HandsOnAI

HandsOnAI is designed to work with Ollama by default. As long as Ollama is running in the background, HandsOnAI will automatically connect to it at `http://localhost:11434`.

**No additional configuration is required** - HandsOnAI detects the local Ollama server automatically.


> ## 🧪 Test Your Installation
>
> Once you’ve started a model using:
>
> ```bash
> ollama run llama3
> ```
>
You can test Hands-On AI in Python with:
>
```python
from hands_on_ai.chat import get_response
print(get_response("What is 3 + 4?"))
```

You should get a real-time AI response!

---

### ✅ Optional Tip (Advanced Config):

> ### ⚙️ Advanced: Custom Model Host

If you're running Ollama on a different host or port (e.g. remote or Docker), you can create a config file to tell Hands-On AI where to send requests.

> ### 🔑 Using API Key Authentication

If your Ollama server requires API key authentication, you can configure it in two ways:

1. **Using environment variables:**
   ```bash
   export HANDS_ON_AI_API_KEY=your-api-key
   ```

2. **Using a config file:**
   Create or edit `~/.hands-on-ai/config.json`:
   ```json
   {
     "api_key": "your-api-key"
   }
   ```

See: [docs/configuration.md](configuration.md) for complete configuration options.

## Troubleshooting

### "Connection refused" error

If Hands-On AI shows a connection error:
1. Make sure Ollama is running
2. Check that you haven't changed the default port (11434)
3. On Windows or macOS, you might need to restart the Ollama application

### Slow responses

1. Try a smaller model like `llama3:8b` which requires fewer resources
2. Close other resource-intensive applications
3. Ensure your computer meets the minimum requirements

### "Out of memory" error

1. Try a smaller model like `llama3:8b`
2. Increase your system's virtual memory (swap file)
3. Close other applications to free up RAM

## Available Models

Here are some models you can use with HandsOnAI via Ollama:

- `llama3` - The recommended default model for most users
- `llama3:8b` - A smaller, faster version if you have limited resources
- `codellama` - Specialised for programming tasks (recommended for code-related exercises)
- `mistral` - An alternative model with good performance
- `phi` - A smaller model with good capabilities for simpler tasks

To download any of these models, use:
```bash
ollama pull model_name
```

## Need More Help?

For more detailed information about Ollama, visit their official documentation at [ollama.ai/docs](https://ollama.ai/docs).

---

## 📚 Related Docs

- [Chat Module Guide](chat-guide.md) - Learn about using the chat module with Ollama
- [RAG Module Guide](rag-guide.md) - Learn about using the RAG module with Ollama
- [Agent Module Guide](agent-guide.md) - Learn about using the agent module with Ollama
- [Configuration Guide](configuration.md) - Advanced configuration options
- [Education Guide](education-guide.md) - Use Hands-On AI in educational settings

---

## 🌍 Beyond Ollama

Once comfortable with local Ollama, you can easily switch HandsOnAI to use other providers:

### Cloud Providers (for more advanced models)
```python
import os
# Switch to OpenAI
os.environ['HANDS_ON_AI_SERVER'] = 'https://api.openai.com'
os.environ['HANDS_ON_AI_API_KEY'] = 'your-openai-key'
os.environ['HANDS_ON_AI_MODEL'] = 'gpt-4'
```

### Multiple Providers in One Project
```python
import os

# Use Ollama for privacy-sensitive tasks
os.environ['HANDS_ON_AI_SERVER'] = 'http://localhost:11434'
privacy_response = get_response("Analyze this personal data...")

# Switch to cloud for advanced reasoning
os.environ['HANDS_ON_AI_SERVER'] = 'https://api.openai.com' 
os.environ['HANDS_ON_AI_API_KEY'] = 'your-key'
advanced_response = get_response("Solve this complex math problem...")
```

See the main README for full provider compatibility information.

---

Now that you have Ollama set up, you're ready to use Hands-On AI! You can start with local privacy-focused projects and expand to cloud providers as needed.