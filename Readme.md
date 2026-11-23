# AI Upskilling Roadmap Generator


A multi-agent RAG (Retrieval-Augmented Generation) system built for corporate upskilling. It takes an employee's current tech stack, compares it to a target role, and generates a personalized, week-by-week learning roadmap. 

Instead of just dumping raw LLM text onto a screen, this project focuses on **strict JSON orchestration**, **dynamic timeline calculation**, and **Zero-Latency client-side guardrails**.

## 🧠 Core Architecture

This isn't a standard "chat-with-a-PDF" wrapper. The backend utilizes three distinct agents:

1. **Auditor Agent:** Calculates the "cognitive distance" between the user's current skills and their goal. (e.g., A C++ developer transitioning to Rust gets a 3-week plan; a UX designer gets a 40-week plan).
2. **Tutor Agent (Self-Reflective RAG):** Queries the local ChromaDB for training materials. Uses an "LLM-as-a-Judge" step to evaluate the relevance of the retrieved text *before* passing it downstream.
3. **Planner Agent:** Enforces strict formatting. Uses bulletproof prompting to guarantee the output is a valid, double-quoted JSON array (bypassing the common markdown block ` ```json ` parsing errors).

## ⚡ Engineering Highlights

* **Zero-Latency Guardrails:** "Shift-left" security. The frontend intercepts non-Rust queries (e.g., "Learn Java") using client-side JS, instantly rejecting them without burning backend API calls or waiting for LLM latency.
* **Deterministic Output:** The backend API strictly returns JSON containing `current_level`, `target_level`, `timeline`, and an array of `weeks`.
* **Dynamic UI Parsing:** The Vanilla JS frontend parses the JSON to build a vertical CSS timeline and a dynamic progress bar, automatically converting raw URLs into clickable reference links.

## 🛠️ Tech Stack

* **Backend:** Python, Flask, LangChain
* **LLM:** Google Gemini 2.5 Flash
* **Vector Store:** ChromaDB (Local SQLite)
* **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
* **Frontend:** HTML5, CSS3, Vanilla JS (Fetch API)

