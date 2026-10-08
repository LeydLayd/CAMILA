# CAMILA - Relationship Evaluation Chatbot

Version 1.0

CAMILA is an AI-powered assistant that evaluates romantic relationships through a structured 33-question survey. It uses a combination of a DeepSeek language model (via LiteLLM) and two machine learning models (Random Forest and Neural Network) to assess relationship functionality and toxicity.

## Project Structure

```
chatbot/
├── main.py                      # Entry point - starts the web server
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Pinned dependencies
├── uv.lock                      # uv lockfile
├── camila/                      # Main agent package
│   ├── __init__.py
│   ├── agent.py                 # ADK agent definition (root_agent)
│   ├── .env-example             # Environment variable template
│   ├── tools/
│   │   ├── __init__.py
│   │   └── tools.py             # Agent tools: save responses, evaluate relationship
│   ├── questions/
│   │   ├── __init__.py
│   │   └── questions.py         # 33 survey questions
│   ├── models/
│   │   ├── modelo_red_neuronal.h5   # Pre-trained neural network (TensorFlow/Keras)
│   │   ├── modelo_rf_multi.pkl      # Pre-trained Random Forest (scikit-learn)
│   │   └── scaler.joblib            # Feature scaler
│   └── test/
│       ├── __init__.py
│       └── test_features.py     # Unit tests
```

## Requirements

- Python >= 3.13
- API key for DeepSeek (or another LLM provider supported by LiteLLM)
- (Optional) Google Gemini API key

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone <repository-url>
cd chatbot

# Create virtual environment and install dependencies
uv venv
uv sync

# Activate the virtual environment
source .venv/bin/activate
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd chatbot

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

1. Copy the environment template and add your API keys:

```bash
cp camila/.env-example camila/.env
```

2. Edit `camila/.env` with your API keys:

```
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your_gemini_api_key_here
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

The agent uses DeepSeek Chat by default via LiteLLM. You can change the model in `camila/agent.py`.

## Usage

### Web Interface (recommended)

Start the web server with the ADK UI:

```bash
python main.py
```

Then open `http://localhost:8000` in your browser. The web UI provides a chat interface to interact with CAMILA.

### Environment Variables

- `HOST` - Server host (default: `0.0.0.0`)
- `PORT` - Server port (default: `8000`)

Example with custom port:

```bash
PORT=8080 python main.py
```

## How It Works

1. CAMILA introduces herself and explains the evaluation process.
2. The user provides their name, age, and gender.
3. CAMILA asks 33 questions about the user's relationship.
4. Each answer is saved via the `guardar_respuesta` tool.
5. After all questions, the `evaluar_relacion` tool runs two models:
   - **Neural Network**: predicts functional vs. dysfunctional relationship percentages.
   - **Random Forest**: predicts functionality and toxicity percentages.
6. CAMILA presents the results in a personalized message.

## Running Tests

```bash
PYTHONPATH=. python3 camila/test/test_features.py
```

## Tech Stack

- **Google ADK** - Agent framework
- **LiteLLM** - LLM proxy (DeepSeek Chat)
- **TensorFlow/Keras** - Neural network model
- **scikit-learn** - Random Forest model and scaler
- **pandas** - Data processing
- **joblib** - Model serialization
- **FastAPI / Uvicorn** - Web server

## 👥 Autores

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/LeydLayd">
        <img src="https://github.com/LeydLayd.png" width="100px;" alt=""/>
        <br />
        <sub><b>Diego Robles</b></sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/Itzel092">
        <img src="https://github.com/Itzel092.png" width="100px;" alt=""/>
        <br />
        <sub><b>Itzel Romano</b></sub>
      </a>
    </td>
  </tr>
</table>
