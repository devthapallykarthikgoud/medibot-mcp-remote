# 🩺 MediBot — AI Medical Assistant

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-2.0+-028090?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?style=for-the-badge)

**A production-grade Agentic AI Healthcare Assistant built on pure MCP (Model Context Protocol) architecture.**  
No LangChain. No simulation. Real MCP — real tools — real agentic reasoning.

[Live Demo](https://mcpclient.streamlit.app/) · [GitHub Repo](https://github.com/devthapallykarthikgoud/medibot-mcp-remote) · [Report Bug](https://github.com/devthapallykarthikgoud/medibot-mcp-remote/issues)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [MCP Tools](#-mcp-tools)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Deployment](#-deployment)
- [How It Works](#-how-it-works)
- [Key Concepts](#-key-concepts)
- [Disclaimer](#-disclaimer)
- [Author](#-author)

---

## 🔍 Overview

**MediBot** is an AI-powered medical assistant that uses a genuine **MCP (Model Context Protocol)** architecture to connect a Streamlit frontend to a remotely deployed FastMCP server. The LLM autonomously selects and invokes medical tools using **function calling** — no hard-coded routing, no simulation.

> This project demonstrates **Agentic AI in practice**: the LLM reasons about the user's input, decides which tool to call, executes it on a remote server, and synthesizes a structured medical response — all autonomously.

**What makes it different from a regular chatbot:**

| Regular Chatbot | MediBot (Agentic MCP) |
|---|---|
| LLM generates text from a prompt | LLM autonomously selects and calls tools |
| Single LLM call per response | Multi-step: LLM → tool → result → final answer |
| Static knowledge only | Real-time tool execution on remote server |
| Hard-coded if/else routing | LLM decides tool selection dynamically |
| No standard protocol | Full MCP protocol compliance |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                   Streamlit (app.py)                        │
│         Symptom Input Tab  │  Medicine Photo Tab            │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                   MCP CLIENT LAYER                          │
│              controller/mcp_client.py                       │
│                                                             │
│  1. Sends user input + TOOL SCHEMAS to Groq LLM             │
│  2. LLM uses function calling → selects tool                │
│  3. Client calls FastMCP Server via HTTP                    │
│  4. Sends tool result back to LLM for final formatting      │
└──────────────────┬──────────────────────────────────────────┘
                   │  HTTPS  (MCP Protocol)
                   │  POST /mcp
┌──────────────────▼──────────────────────────────────────────┐
│            FASTMCP SERVER  (Render)                         │
│    https://medibot-mcp-remote.onrender.com/mcp              │
│                                                             │
│  @mcp.tool()  ┌─────────────────────────────────────────┐  │
│               │  symptom_checker(symptoms)               │  │
│               │  medicine_lookup(medicine_name)          │  │
│               │  medicine_photo_analyzer(image_b64)      │  │
│               └─────────────────────────────────────────┘  │
└──────────────────┬──────────────────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                    GROQ LLM API                             │
│   Text:   llama-3.3-70b-versatile                           │
│   Vision: meta-llama/llama-4-scout-17b-16e-instruct         │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Features

- 🔬 **Symptom Analysis** — Describe symptoms in plain English and receive structured medical guidance
- 💊 **Medicine Lookup** — Get complete information about any medicine by name
- 📷 **Medicine Photo Analyzer** — Upload a medicine photo and Vision AI reads the label
- 🤖 **Agentic Tool Selection** — LLM autonomously decides which tool to call using function calling
- 🌐 **Remote MCP Server** — FastMCP server deployed on Render, accessible from anywhere
- 🔒 **Pure Protocol** — Real FastMCP implementation, not a simulated Flask API
- 🐍 **No Frameworks** — Built from scratch in pure Python — no LangChain, no n8n

---

## 🛠 MCP Tools

### 1. `symptom_checker(symptoms: str)`
Analyzes patient-described symptoms and returns:
- Possible conditions (2–3 most likely)
- Severity level: **Mild / Moderate / Severe**
- Safe home remedies (3–4 suggestions)
- OTC medicine category recommendations *(no dosage)*
- Clear guidance on when to see a doctor

### 2. `medicine_lookup(medicine_name: str)`
Provides complete medicine information:
- Medicine name and drug category
- Therapeutic uses and indications
- When to use and when **NOT** to use
- Common side effects
- Important safety warnings and contraindications

### 3. `medicine_photo_analyzer(image_b64: str)`
Vision AI medicine identification:
- Accepts base64-encoded medicine images
- Uses **Llama 4 Scout** (multimodal vision model)
- Reads medicine labels, packaging, and strips
- Returns full medicine details from visual analysis

---

## 💻 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **UI** | Streamlit | Web interface — symptom input, image upload |
| **MCP Client** | FastMCP Client + requests | LLM communication, tool orchestration |
| **MCP Server** | FastMCP 2.0 | Tool registration, protocol compliance |
| **LLM (Text)** | Groq — Llama 3.3 70B | Symptom/medicine analysis, function calling |
| **LLM (Vision)** | Groq — Llama 4 Scout | Medicine photo interpretation |
| **Protocol** | MCP (Model Context Protocol) | Universal LLM–tool interface standard |
| **Deployment** | Render | Remote MCP server hosting |
| **Package Mgr** | uv | Fast Python dependency management |

---

## 📁 Project Structure

```
medibot-mcp-remote/
│
├── app.py                    # Streamlit UI — main frontend application
├── main.py                   # Entry point / runner
├── mcp_server.py             # FastMCP server — tool registration + /mcp endpoint
├── mcp.json                  # MCP configuration (server metadata)
│
├── controller/
│   └── mcp_client.py         # MCP client — LLM function calling + tool execution
│
├── tools/
│   ├── symptom_checker.py    # Tool 1: Symptom analysis via Groq LLM
│   ├── medicine_lookup.py    # Tool 2: Medicine info via Groq LLM
│   └── medicine_photo.py     # Tool 3: Image analysis via Groq Vision
│
├── .gitignore                # Excludes .env, __pycache__, etc.
├── .python-version           # Python version pin (3.11+)
├── requirements.txt          # pip dependencies
├── pyproject.toml            # Project metadata (uv)
└── uv.lock                   # Locked dependency versions
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A free [Groq API key](https://console.groq.com) *(no credit card required)*

### 1. Clone the repository

```bash
git clone https://github.com/devthapallykarthikgoud/medibot-mcp-remote.git
cd medibot-mcp-remote
```

### 2. Install dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv (faster)
uv sync
```

### 3. Set your API key

```bash
# Mac / Linux
export GROQ_API_KEY=your_groq_api_key_here

# Windows
set GROQ_API_KEY=your_groq_api_key_here
```

> Get your free API key at [console.groq.com](https://console.groq.com)

### 4. Run the MCP Server (Terminal 1)

```bash
python mcp_server.py
# Server starts at: http://localhost:8000/mcp
```

### 5. Run the Streamlit UI (Terminal 2)

```bash
streamlit run app.py
# Opens at: http://localhost:8501
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq API key from console.groq.com |
| `MCP_SERVER_URL` | Optional | Override default server URL (default: Render) |
| `PORT` | Auto | Set by Render automatically on deployment |

> **Security:** Never commit your `.env` file. The `.gitignore` already excludes it.

---

## ☁️ Deployment

### MCP Server → Render

The FastMCP server is deployed as a standalone web service on Render.

**Live MCP Endpoint:**
```
https://medibot-mcp-remote.onrender.com/mcp
```

**Steps to deploy your own:**

1. Push code to GitHub
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repository
4. Set the following:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python mcp_server.py`
5. Add environment variable: `GROQ_API_KEY = your_key`
6. Deploy — Render provides a permanent HTTPS URL

### Streamlit UI → Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect GitHub → select `app.py`
3. Add `GROQ_API_KEY` in Settings → Secrets
4. Deploy

---

## ⚙️ How It Works

### Function Calling Flow

```
User: "I have fever 101°F and sore throat"
         │
         ▼
[MCP Client] → Sends to Groq LLM with tool schemas
         │
         ▼
[Groq LLM] → Reads tool descriptions → Decides: symptom_checker
         │
         ▼  finish_reason = "tool_calls"
[MCP Client] → Extracts tool_name="symptom_checker", args={"symptoms": "..."}
         │
         ▼
[FastMCP Server] → Runs symptom_checker() → Calls Groq with medical prompt
         │
         ▼
[Tool Result] → Returned to MCP Client
         │
         ▼
[MCP Client] → Sends tool result back to Groq LLM as tool message
         │
         ▼
[Groq LLM] → Formats final structured response
         │
         ▼
[Streamlit UI] → Displays result to user
```

### Why the LLM picks the right tool

The LLM reads the `description` field of each tool schema and compares it to the user's input. This is why tool descriptions are written precisely:

```python
# LLM reads this and decides WHEN to use each tool
"symptom_checker"       → "Analyze patient symptoms..."
"medicine_lookup"       → "Look up medicine info by name..."
"medicine_photo_analyzer" → "Analyze a medicine photo..."
```

---

## 📚 Key Concepts

### What is MCP (Model Context Protocol)?
MCP is an open standard by Anthropic that defines how LLMs connect to external tools. It standardizes tool discovery, invocation, and response handling — any MCP-compatible LLM can use any MCP server.

### What is FastMCP?
FastMCP is a Python library that implements the MCP specification. The `@mcp.tool()` decorator registers a function as an MCP tool, automatically generating its schema from type hints and docstrings.

### What makes this Agentic?
The LLM autonomously decides which tool to invoke based on user intent — no if/else routing in application code. The LLM acts as a reasoning agent: it observes the input, selects the appropriate tool, executes it, and synthesizes a response.

---

## ⚠️ Disclaimer

> **MediBot is for informational and educational purposes only.**
>
> - This is NOT a substitute for professional medical advice, diagnosis, or treatment
> - Never prescribes specific dosages or makes definitive diagnoses
> - Always consult a qualified healthcare professional for medical decisions
> - Emergency symptoms should be treated as emergencies — call emergency services immediately

---

## 👤 Author

**Devathapally Umakarthikeya (Karthik)**

- 🎓 B.Tech CSE (AI & ML) — SVIT, JNTUH, Hyderabad
- 💼 Data Science Trainee — Innomatics Research Labs
- 🔗 [LinkedIn](https://linkedin.com/in/devathapallyumakarthikeya)
- 🐙 [GitHub](https://github.com/devthapallykarthikgoud)
- 📧 devathapallyumakarthikeya@gmail.com

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ using **FastMCP · Groq · Streamlit · Python**

⭐ Star this repo if you found it useful!

</div>
