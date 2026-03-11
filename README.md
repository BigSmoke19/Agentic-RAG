# ⚽ Football RAG — Question Answering System

A Retrieval-Augmented Generation (RAG) system that answers football-related questions using Wikipedia data, local embeddings, and a free LLM. Ask questions like *"Who won the 2013 Champions League Final?"* or *"Who won the Ballon d'Or in 2018?"* — entirely from the command line.

---

## 🧠 How It Works

```
Wikipedia Articles → Text Chunks → Local Embeddings → ChromaDB Vector Store
                                                              ↓
User Question → Embed Question → Similarity Search → Relevant Chunks
                                                              ↓
                                                            LLM → Answer
```

1. **Data collection** — Wikipedia articles about UCL finals, Ballon d'Or, World Cups, and top players are scraped and saved as `.txt` files
2. **Chunking** — Articles are split into overlapping chunks for better retrieval
3. **Embedding** — Each chunk is embedded locally using `sentence-transformers` (no API needed)
4. **Storage** — Embeddings are stored in a persistent ChromaDB vector database
5. **Retrieval** — User questions are embedded and matched against stored chunks
6. **Generation** — Relevant chunks are injected into a prompt sent to Mistral via HuggingFace

---

## 📁 Project Structure

```
Agentic RAG/
├── data.py                  # Scrapes Wikipedia and saves .txt files
├── rag.py                   # Main RAG pipeline (embed, store, query, answer)
├── football_data/           # Scraped Wikipedia .txt files
├── chroma_persistent_storage/  # Local vector database (auto-generated)
├── .env                     # API keys (never commit this)
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Agentic RAG.git
cd Agentic RAG
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
HF_TOKEN=your_huggingface_token_here
```

Get your free HuggingFace token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

### 5. Scrape Wikipedia data

```bash
python data_generation.py
```

This will download articles about Champions League finals, Ballon d'Or winners, World Cups, and top players into the `football_data/` folder.

### 6. Run the RAG pipeline

// This can be ignored if data already embedded and stored in vectordb (chroma_persistent_storage)

```bash
python rag.py
```

---

## 💬 Example Questions

```
You: Who won the 2013 UEFA Champions League Final?
Bot: Bayern Munich won the 2013 UEFA Champions League Final, defeating Borussia Dortmund 2-1...

You: Who won the Ballon d'Or in 2018?
Bot: Luka Modrić won the 2018 Ballon d'Or, ending the 10-year dominance of Messi and Ronaldo...

You: How many World Cup goals did Messi score?
Bot: Lionel Messi scored 13 goals across his World Cup career...

You: Who scored in the 2016 Champions League Final?
Bot: Sergio Ramos, Gareth Bale, and Marco Asensio scored for Real Madrid...
```

---

## 🗂️ Data Coverage

| Category | Coverage |
|---|---|
| UEFA Champions League Finals | 2010 – 2024 |
| Ballon d'Or | 2010 - 2011 – 2016 - 2017 - 2018 |
| FIFA World Cup | 2010, 2014, 2018, 2022 |
| Players | Messi, Ronaldo, Modric, Benzema, Mbappe, Haaland, Salah, and more |

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| `wikipedia-api` | Scrape Wikipedia articles |
| `sentence-transformers` | Local text embeddings (no API needed) |
| `chromadb` | Local persistent vector database |
| `huggingface-hub` | Access Mistral LLM via Inference API |
| `python-dotenv` | Manage environment variables |

---

## 📦 Requirements


Install all with:

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `HF_TOKEN` | HuggingFace API token (free) |

---

## 📌 Notes

- The vector database is **persistent** — you only need to embed documents once. Subsequent runs will reuse the stored embeddings.
- Embeddings run **fully locally** using `sentence-transformers` — no API calls needed for the embedding step.
- The LLM (meta-llama/Llama-3.1-8B-Instruct) runs on HuggingFace's free inference API.

---

## 👤 Author

**Mohammad Safieddine**  
CS Graduate | Full Stack Developer | AI Engineer in progress  
[LinkedIn](www.linkedin.com/in/mohammad-safieddine-153635248) • [GitHub](https://github.com/BigSmoke19)
