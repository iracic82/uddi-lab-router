# Instruqt Lab Router 🚀

[![GitHub license](https://img.shields.io/github/license/iracic82/uddi-lab-router)](./LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/iracic82/uddi-lab-router)](https://github.com/iracic82/uddi-lab-router/commits/main)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)]()

**Maps natural-language prompts to Instruqt labs and returns one-click invite links—ideal for AI agent integration, partner onboarding, and frictionless lab access.**

---

## ✨ Features

- ⚡️ **FastAPI** backend, React UI, OpenAPI & ReDoc docs
- 🦾 **Agent-ready:** Built for LangChain, OpenAI, and LLMs
- 🔒 Token-based API (secure, no hard-coded secrets)
- 🌗 Dark/light mode UI
- 📑 Live `/docs` (Swagger) and `/portal` (ReDoc) API documentation

---

## 🚀 Quickstart

### 1. Clone & Setup

```bash
git clone https://github.com/iracic82/uddi-lab-router.git
cd uddi-lab-router
cp .env.example .env          # Fill in your secrets!
```


### 2. Docker

```bash
docker build -t lab-router:latest .
docker run --rm -p 8000:8000 --env-file .env lab-router:latest
```


### 3. Local Dev

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:api --reload
```
Then open: http://localhost:8000


### ⚙️ .env Setup

Copy .env.example and set your values:

```bash
ROUTER_API_KEY=your_router_token
INSTRUQT_API_TOKEN=...
INSTRUQT_API_URL=https://play.instruqt.com/graphql
INSTRUQT_TEAM_SLUG=your_team
OPENAI_API_KEY=sk-...
```

Never commit your real .env!


### 🧪 API Usage


	•	Swagger: http://localhost:8000/docs
	•	ReDoc: http://localhost:8000/portal


Example API Calls


```bash
export API=http://localhost:8000
export TOKEN=your_router_api_key

# List labs
curl -H "Authorization: Bearer $TOKEN" $API/tracks | jq

# Create invite
curl -X POST -H "Authorization: Bearer $TOKEN" "$API/invite?slug=infoblox-threat-defense"

# Free-text to invite link
curl -X POST -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Threat Defense security lab"}' \
     $API/resolve
```


### 🤖 AI Agent Integration


Plug-and-play with LangChain or any OpenAPI/LLM agent.

Drop-in example:

```bash
from langchain.tools.openapi import RequestsToolkit
toolkit = RequestsToolkit.from_openapi_spec("https://your-api/portal/openapi.json")
llm_agent.run(toolkit)
```

See docs/AI_INTEGRATION.md for details.

🛡️ License

MIT, see LICENSE.


🙋 FAQ

	•	401 Invalid API Key? — Double-check your .env and use the correct token!
	•	UI or asset 404s in Docker? — Ensure the static/ folder is populated at build time.
	•	Can’t hit OpenAI? — Set your OPENAI_API_KEY in .env.


🤝 Contributing

Pull requests and issues welcome! Want a feature? Open an issue.


📣 About

Created by Igor Racic for the Instruqt/Infoblox ecosystem.


---

### Download as a file

Here’s your [README-lab-router.md](sandbox:/mnt/data/README-lab-router.md?_chatgptios_conversationID=688353a5-5940-832a-a423-b8d475222e42&_chatgptios_messageID=762c200c-9039-4f70-bc20-b238fe846982) ready for download.

---

**Pro tip:**  
- Put screenshots in `docs/`, update the `README.md` links.
- Push to GitHub—your repo will look clean, pro, and self-documenting!

If you want a `pyproject.toml` or `setup.cfg` template for metadata, just say the word!