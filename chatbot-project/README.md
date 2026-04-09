# Anchor Customs - AI Chatbot

A Gen AI-powered chatbot for **Anchor Customs** that helps customers discover products, get pricing info, and answer FAQs. Runs 100% locally on Windows — no GPU, no cloud API keys needed.

## Prerequisites

- **Python 3.10+** — Download from https://www.python.org/downloads/
  - During installation, check **"Add Python to PATH"**
- **Internet** — needed only once to download the AI model (~80MB)

## How to Run on Windows

### First-Time Setup

Open **Command Prompt** or **PowerShell**, then:

```bash
# 1. Navigate to the project folder
cd  C:\Users\bhoomi\Documents\GitHub\anchor-customs\chatbot-project

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
venv\Scripts\activate

# 4. Install dependencies (takes 2-5 minutes)
pip install -r requirements.txt

# 5. Train the model — downloads AI model & runs test queries (~1-2 minutes)
python train_model.py

# 6. Start the chatbot server
python app.py
```

### After Setup (Quick Start)

Double-click **`run.bat`** or run:

```bash
cd  C:\Users\bhoomi\Documents\GitHub\anchor-customs\chatbot-project
venv\Scripts\activate
python app.py
```

### Open the Chatbot

Once the server starts, open your browser and go to:

**http://localhost:5000**

## Example Queries

| You type                     | The bot does                   |
| ---------------------------- | ------------------------------ |
| "hi"                         | Greets you                     |
| "what can I buy under 500?"  | Shows products under Rs.500    |
| "show me frames"             | Lists all frame products       |
| "tell me about the magazine" | Shows magazine details         |
| "do you have combos?"        | Lists all combo deals          |
| "cheapest product"           | Returns the lowest-priced item |
| "gift for my boyfriend"      | Suggests relevant products     |
| "what products do you have?" | Shows full catalog             |
| "how to order"               | Explains the ordering process  |

## Project Structure

```
chatbot-project/
|-- README.md                  # You are here
|-- PLAN.md                    # Detailed project plan (architecture, AI concepts)
|-- requirements.txt           # Python dependencies
|-- app.py                     # Flask server (main entry point)
|-- train_model.py             # Downloads model & runs tests
|-- run.bat                    # One-click Windows launcher
|-- chatbot/
|   |-- __init__.py
|   |-- intent_classifier.py   # AI intent classification
|   |-- product_search.py      # Semantic search over products
|   |-- response_generator.py  # Formats chat responses
|   |-- training_data.py       # Intent examples & training data
|-- data/
|   |-- products.json          # Product catalog (16 products + 4 combos)
|-- static/
|   |-- style.css              # Chat UI styles
|-- templates/
|   |-- index.html             # Chat UI page
```

## Tech Stack

| Component | Technology                                | Size/Notes             |
| --------- | ----------------------------------------- | ---------------------- |
| Language  | Python 3.10+                              | —                      |
| AI Model  | `all-MiniLM-L6-v2`                        | ~80MB, runs on CPU     |
| NLP       | Sentence Transformers + Cosine Similarity | Semantic understanding |
| Backend   | Flask                                     | Lightweight web server |
| Frontend  | HTML/CSS/JS                               | No build step needed   |

## System Requirements

| Spec | Minimum                            |
| ---- | ---------------------------------- |
| OS   | Windows 10/11                      |
| RAM  | 4 GB (8 GB recommended)            |
| CPU  | Any x64 processor                  |
| GPU  | Not required                       |
| Disk | ~500 MB (for model + dependencies) |

## Troubleshooting

| Problem                 | Fix                                                                    |
| ----------------------- | ---------------------------------------------------------------------- |
| `python` not recognized | Reinstall Python with "Add to PATH" checked                            |
| `pip install` fails     | Run `python -m pip install --upgrade pip` first                        |
| Model download hangs    | Check internet connection; the first download needs ~80MB              |
| Port 5000 in use        | Change port in `app.py`: `app.run(port=5001)`                          |
| Page won't load         | Make sure you see "Anchor Customs Chatbot is running!" in the terminal |
