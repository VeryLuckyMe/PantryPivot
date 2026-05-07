# PantryPivot 🥗 — Advanced AI Kitchen Manager

**Turn What's Left Into What's Next.** PantryPivot is a production-ready, agentic AI application designed to reduce food waste through intelligent recipe generation, automated inventory management, and expert-verified culinary advice.

---

## 🚀 Advanced AI Architecture (Finals Edition)

This version of PantryPivot has been upgraded with a professional-grade AI stack:

### 1. 🤖 Agentic AI (Reasoning Loop)
Unlike a standard chatbot, PantryPivot is an **AI Agent**. It has "hands" through **Function Calling**.
- **Autonomous Inventory Management**: The AI reasons about your cooking activities and automatically triggers a `deduct_pantry_items` tool to update your stock.
- **State Persistence**: Uses a local JSON-based persistence layer to ensure your kitchen inventory is remembered across sessions.

### 2. 📚 RAG (Retrieval-Augmented Generation)
The system is grounded in expert knowledge using a **Vector Database (ChromaDB)**.
- **Domain-Specific Knowledge**: Injected with the "Food Too Good To Waste" expert guide (PDF).
- **Citation Engine**: Every advice or storage tip provided by the AI is cited directly from the knowledge base (e.g., *"Source: Page 4"*).
- **Semantic Search**: Uses Google Gemini Embeddings to find the most relevant advice for your specific food waste situation.

### 3. 🛡️ Multi-Layer Security (Sandwich Defense)
Hardened against prompt injection and jailbreaking using advanced security patterns:
- **The Sandwich Defense**: System instructions are reinforced at the bottom of every prompt to prevent instruction overrides.
- **Random Delimiter Encapsulation**: Dynamic, unique tags (e.g., `<USER_INPUT_X7Y2>`) isolate user input to prevent tag breakout attacks.
- **Input Validation**: Real-time filtering for malicious keywords and prompt injection attempts.

---

## 🌟 Core Features

- **Expert Recipe Pivot Engine**: Transform meals using Cuisine, Meal Type, and Difficulty pivots.
- **Waste Analytics**: Track your financial and environmental impact in real-time.
- **Modular Refactor**: Clean, package-based Python structure for maximum maintainability.

---

## 🛠️ Tech Stack

- **Framework**: Streamlit (Python)
- **AI Models**: Google Gemini 2.5 (Pro/Flash/Flash-Lite)
- **Embeddings**: Google Gemini Embedding-001
- **Vector DB**: ChromaDB
- **Document Loading**: PyPDF
- **Security**: Custom "Sandwich Defense" Logic

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.10+
- Google Gemini API Key

### Quick Start
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Secrets**:
   Create `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
4. **Run the Application**:
   ```bash
   streamlit run PantryPivot.py
   ```

---

## 📄 License & Credits
Built for the **Applied AI Finals**. 
*Focus: RAG, Agentic AI, and Secure Prompt Engineering.*