# ⚡️ Calling the Instruqt Lab Router from an LLM

The router exposes a normal REST/OpenAPI interface (**/openapi.json**).  
Tools such as **LangChain, LlamaIndex,** or **OpenAI Function Calling** can ingest that spec and auto-generate the correct HTTP calls.

---

## 0. Prerequisites

```bash
pip install langchain langchain-openai
export OPENAI_API_KEY=<your-OpenAI-key>
