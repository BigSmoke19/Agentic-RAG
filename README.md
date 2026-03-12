# ⚽ Agentic RAG — Football Intelligence System

A full **Agentic Retrieval-Augmented Generation (RAG)** system that answers football-related questions using Wikipedia data, local embeddings, and a free LLM. The agent intelligently decides whether to search internal documents, search the web, perform calculations, or answer directly.

---

## 🧠 How It Works

```
Wikipedia Articles → Text Chunks → Local Embeddings → ChromaDB Vector Store
                                                              ↓
User Question → Agent Thinks → Picks Tool → Executes Tool → Fed Back to Agent
                                                              ↓
                                                    Groq LLM → Final Answer
```

1. **Data collection** — Wikipedia articles about UCL finals, Ballon d'Or, World Cups, and top players are scraped and saved as `.txt` files
2. **Chunking** — Articles are split into overlapping chunks for better retrieval
3. **Embedding** — Each chunk is embedded locally using `sentence-transformers` (no API needed)
4. **Storage** — Embeddings are stored in a persistent ChromaDB vector database
5. **Agent Loop** — Agent decides which tool to use based on the question
6. **Generation** — Relevant chunks or web results are injected into a prompt sent to Llama via Groq

---

## 🤖 Agent Tools

| Tool | Description |
|---|---|
| `search_documents` | Searches internal football Wikipedia documents via RAG |
| `search_web` | Searches the internet via DDGS for general or recent info |
| `calculator` | Evaluates math expressions |
| `get_current_date` | Returns today's date |

**Agent decision logic:**
- Football questions → `search_documents` first
- Non-football / general questions → `search_web` directly
- If documents return irrelevant results → fallback to `search_web`
- Never calls the same tool twice with the same input

---

## 📁 Project Structure

```
Agentic-RAG/
├── data_generation.py           # Scrapes Wikipedia and saves .txt files
├── rag.py                       # RAG pipeline (embed, store, query, answer)
├── main.py                      # Agent loop with tool calling
├── eval.py                      # Evaluation suite (LLM-as-judge)
├── football_data/               # Scraped Wikipedia .txt files
├── chroma_persistent_storage/   # Local vector database (auto-generated)
├── .env                         # API keys (never commit this)
├── requirements.txt             # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/BigSmoke19/Agentic-RAG.git
cd Agentic-RAG
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your environment variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

### 5. Scrape Wikipedia data

```bash
python data.py
```

This downloads articles about Champions League finals, Ballon d'Or winners, World Cups, and top players into the `football_data/` folder.

### 6. Embed and store documents

> Skip this step if `chroma_persistent_storage/` already exists — embeddings are persistent.

```bash
python rag.py
```

### 7. Run the agent

```bash
python main.py
```

---

## 💬 Example Questions

```
You: Who won the 2013 UEFA Champions League Final?
Agent: Bayern Munich won the 2013 UEFA Champions League Final, defeating Borussia Dortmund 2-1...

You: Who won the Ballon d'Or in 2018?
Agent: Luka Modrić won the 2018 Ballon d'Or, ending the 10-year dominance of Messi and Ronaldo...

You: Who is Lionel Messi?
Agent: Lionel Messi is an Argentine professional footballer widely regarded as one of the greatest players of all time...

You: What is 25 * 4?
Agent: 100

You: What is today's date?
Agent: 2026-03-12
```

---

## 🗂️ Data Coverage

| Category | Coverage |
|---|---|
| UEFA Champions League Finals | 2010 – 2024 |
| Ballon d'Or | 2010 – 2018 |
| FIFA World Cup | 2010, 2014, 2018, 2022 |
| Players | Messi, Ronaldo, Modric, Benzema, Mbappe, Haaland, Salah, and more |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `wikipedia-api` | Scrape Wikipedia articles |
| `sentence-transformers` | Local text embeddings (no API needed) |
| `chromadb` | Local persistent vector database |
| `ddgs` | Free web search (DuckDuckGo) |
| `groq` | Fast free LLM inference (Llama 3.3 70B) |
| `python-dotenv` | Manage environment variables |

---

## 📊 Evaluation

The project includes an automated eval suite using **LLM-as-judge**:

```bash
python eval.py
```

Example output:
```
✅ Who won the 2013 Champions League Final?
✅ Who won the 2022 World Cup?
❌ Who won Ballon d'Or in 2018?

Score: 4/5 (80%)
```

Metrics measured:
- Answer correctness
- Grounding in retrieved context
- Hallucination detection

---

## 📦 Requirements

```
groq
chromadb
sentence-transformers
ddgs
wikipedia-api
python-dotenv
pyyaml
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key (free, no credit card) |

---

## 📌 Notes

- The vector database is **persistent** — embed documents once, reuse forever
- Embeddings run **fully locally** using `sentence-transformers` — no API needed
- The LLM (Llama 3.3 70B) runs on **Groq's free inference API** — fast and unlimited
- Agent uses a **max 5 iteration loop** to prevent infinite loops
- Duplicate tool calls are automatically detected and blocked

---

## 👤 Author

**Mohammad Safieddine**
CS Graduate | Full Stack Developer | AI Engineer in progress
[LinkedIn](https://www.linkedin.com/in/mohammad-safieddine-153635248) • [GitHub](https://github.com/BigSmoke19)