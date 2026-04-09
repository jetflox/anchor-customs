# Anchor Customs Chatbot - Project Plan

## Overview

A Gen AI-powered chatbot for **Anchor Customs** that helps customers discover products, get pricing info, and answer FAQs. It runs **100% locally** on a Windows laptop (8GB RAM, Intel i5-1235U, no GPU required).

---

## System Specs (Target Machine)

| Spec | Value |
|------|-------|
| **OS** | Windows 11 Home (24H2) |
| **Processor** | 12th Gen Intel Core i5-1235U (1.30 GHz) |
| **RAM** | 8 GB (7.73 GB usable) |
| **GPU** | None (integrated only) |
| **Architecture** | x64 |

---

## Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **Language** | Python 3.10+ | Industry standard for AI/ML |
| **AI Model** | `all-MiniLM-L6-v2` (sentence-transformers) | Only ~80MB, runs on CPU, great for semantic search |
| **NLP** | Sentence Transformers + Cosine Similarity | Understands meaning, not just keywords |
| **Backend** | Flask | Lightweight Python web framework |
| **Frontend** | HTML/CSS/JS (chat widget) | No extra dependencies |
| **Data** | JSON (product catalog) | Simple, no database needed |

---

## Architecture

```
User Query
    |
    v
[Flask Web Server (app.py)]
    |
    v
[Intent Classifier (intent_classifier.py)]
    |--- Greeting / Farewell / Thanks --> Static Response
    |--- Product Query ----------------> [Product Search Engine]
    |                                         |
    |                                         v
    |                                   [Sentence Transformer Model]
    |                                   Encodes query + product data
    |                                         |
    |                                         v
    |                                   [Cosine Similarity Matching]
    |                                         |
    |                                         v
    |                                   Ranked Product Results
    |
    v
[Response Generator (response_generator.py)]
    |
    v
Formatted Chat Response (JSON)
    |
    v
[Chat UI (index.html)]
```

---

## How the AI Works (For Your Report)

### 1. Sentence Embeddings (The "Brain")
- We use the **`all-MiniLM-L6-v2`** model from the `sentence-transformers` library.
- This model converts text into **384-dimensional vectors** (embeddings).
- Similar meanings produce similar vectors, even if the words are different.
  - e.g., "gift for boyfriend" and "present for him" will have similar vectors.

### 2. Cosine Similarity (The "Matching")
- When a user asks a question, we convert it into an embedding.
- We compare it against pre-computed embeddings of all product descriptions.
- Products with the **highest similarity scores** are returned.

### 3. Intent Classification (The "Router")
- Before semantic search, we classify the user's **intent**:
  - `greeting` - "hi", "hello"
  - `product_search` - "show me frames"
  - `price_query` - "what can I buy under 500?"
  - `product_info` - "tell me about the magazine"
  - `combo_query` - "do you have combos?"
  - `farewell` - "bye", "thanks"
- This is done using **keyword matching + embedding similarity** against intent examples.

### 4. Price Filtering
- Queries like "under 500", "below 1000", "between 500 and 1000" are parsed with regex.
- Products are filtered by price before ranking by relevance.

---

## Project Structure

```
chatbot-project/
|-- PLAN.md                    # This file
|-- requirements.txt           # Python dependencies
|-- app.py                     # Flask server (main entry point)
|-- chatbot/
|   |-- __init__.py
|   |-- intent_classifier.py   # Classifies user intent
|   |-- product_search.py      # Semantic search over products
|   |-- response_generator.py  # Formats responses
|   |-- training_data.py       # Intent examples & training data
|-- data/
|   |-- products.json          # Product catalog
|-- static/
|   |-- style.css              # Chat UI styles
|-- templates/
|   |-- index.html             # Chat UI page
|-- train_model.py             # Script to pre-compute embeddings
|-- run.bat                    # One-click launcher for Windows
```

---

## Setup & Execution Instructions (Windows)

### Prerequisites
1. Install **Python 3.10+** from https://www.python.org/downloads/
   - IMPORTANT: Check **"Add Python to PATH"** during installation.

### Step-by-Step Setup

```bash
# Step 1: Open Command Prompt (cmd) or PowerShell
# Step 2: Navigate to the project folder
cd path\to\chatbot-project

# Step 3: Create a virtual environment
python -m venv venv

# Step 4: Activate the virtual environment
venv\Scripts\activate

# Step 5: Install dependencies
pip install -r requirements.txt

# Step 6: Train the model (pre-compute embeddings) - takes ~1-2 minutes first time
python train_model.py

# Step 7: Run the chatbot server
python app.py
```

### Or Just Double-Click `run.bat`
After initial setup (steps 3-5), you can use `run.bat` to start the chatbot.

### Access the Chatbot
Open your browser and go to: **http://localhost:5000**

---

## Example Queries the Chatbot Can Handle

| User Query | Bot Behavior |
|-----------|-------------|
| "hi" / "hello" | Greets the user |
| "what can I buy under 500?" | Filters products under Rs.500 |
| "show me frames" | Returns all frame products |
| "tell me about the magazine" | Shows magazine details |
| "do you have combos?" | Lists all combo deals |
| "what's the cheapest product?" | Returns lowest-priced item |
| "I want a gift for my boyfriend" | Suggests relevant products |
| "what products do you have?" | Lists all products |
| "bye" / "thanks" | Farewell response |

---

## Model Details (For Report)

| Property | Value |
|---------|-------|
| **Model Name** | `all-MiniLM-L6-v2` |
| **Model Size** | ~80 MB |
| **Embedding Dimensions** | 384 |
| **Training Data** | 1B+ sentence pairs |
| **RAM Usage** | ~200-300 MB |
| **Inference Time** | ~50-100ms per query (CPU) |
| **License** | Apache 2.0 (free for commercial use) |

---

## Key Gen AI Concepts Demonstrated

1. **Natural Language Understanding (NLU)** - Understanding user intent from free text
2. **Sentence Embeddings** - Converting text to numerical vectors
3. **Semantic Search** - Finding relevant products by meaning, not just keywords
4. **Cosine Similarity** - Measuring how similar two pieces of text are
5. **Intent Classification** - Routing queries to appropriate handlers
6. **Named Entity Recognition (NER)** - Extracting prices, product names from queries
7. **Retrieval-Augmented Generation (RAG)** - Using product data to generate accurate responses

---

## Performance Notes

- **First run** downloads the model (~80MB) - needs internet once
- **Subsequent runs** use cached model - works offline
- **RAM usage**: ~300-400MB total (well within 8GB)
- **Response time**: < 1 second per query
- **No GPU required** - runs entirely on CPU
