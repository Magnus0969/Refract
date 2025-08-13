# 🧠 Refract: An AI-Powered Research Agent

**Refract** is an intelligent, agentic AI assistant designed to support researchers, students, and knowledge-seekers in exploring complex topics.  
Built using the ReAct (Reasoning + Acting) paradigm, it leverages large language models and real-time web tools to reason, search, and summarize information step-by-step — just like a human researcher.

---

## 🔍 Key Features

- 🤖 **LLM-powered Agent** using [`Qwen/Qwen1.5-1.8B-Chat`](https://huggingface.co/Qwen/Qwen1.5-1.8B-Chat)  
- 🧠 **ReAct Loop**: Think, act (search/scrape), and reflect iteratively  
- 🌐 **Web-Augmented**: Uses Playwright for dynamic web search and scraping  
- 🛠️ **Tool-Use Capable**: Executes `Search[...]` and `Scrape[...]` commands during reasoning  
- 📄 **Auto-Generated Reports** in PDF and Markdown  
- 🧪 **Partial Summary Fallback**: When the reasoning step limit is hit, Refract summarizes and verifies what it has collected so far  
- 🧭 **Extensible Design** for integrating new tools and models  

---

## 📦 Tech Stack

- `transformers` + `torch` for language model inference  
- `playwright` + `beautifulsoup4` for real-time web scraping  
- `langchain` for tool abstraction and compatibility  
- `reportlab` for structured PDF report generation  

---

## 🚀 How It Works

1. User enters a topic (e.g., *"Foundation Models in Machine Learning"*)  
2. Refract reasons about the topic and decides when to take actions like `Search[...]` or `Scrape[...]`  
3. It gathers evidence, reflects, and eventually produces a concise, verified summary  
4. If it hits the max step limit, it summarizes what it found and runs a verification pass  

---

## 📁 Folder Structure

```
Refract/
├── main.py # Main entry point for the agent
├── llm.py # Model logic and ReAct prompt templates
├── tools.py # Executes Search[...] and Scrape[...] actions
├── playwright_search_scrape.py # Search and scrape logic using Playwright
├── report_utils.py # Generates reports in Markdown and PDF formats
├── requirements.txt # Python dependencies
├── README.md
```


---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/refract.git
cd refract
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright browser drivers

```bash
playwright install
```

### 4. Run the agent

```bash
python app.py
```
---

## ✅ Requirements
- Python 3.8+
- Internet connection for model and scraping
- GPU (recommended) for faster model inference

---

## ✨ Future Improvements
- Create own ReAct prompt
- Support for more tools (e.g., Wolfram, Wikipedia API, Paper API)
- RAG-based memory integration
- Support for larger Qwen variants or open-source alternatives
- Web UI using Gradio or Streamlit

---

## 📜 License

This project is licensed under the [MIT License](LICENSE)

---
## 👨‍💻 Author

**Karthik B Magadi**  
GitHub: [@Magnus0969](https://github.com/Magnus0969)

---

⭐ **Star this repo if you found it helpful!**
