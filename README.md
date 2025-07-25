# Instruqt Lab Router 🚀

Maps natural-language prompts to Instruqt labs and returns one-click invite links.

---

## Quick-start

```bash
export API=https://api.example.com          # or http://localhost:8000
export TOKEN=mysecret                       # ROUTER_API_KEY you issued

# List labs the token can see
curl -H "Authorization: Bearer $TOKEN" \
     $API/tracks | jq

# Create an invite when you already know the slug
curl -X POST \
     -H "Authorization: Bearer $TOKEN" \
     "$API/invite?slug=infoblox-threat-defense"

# Resolve free-text to an invite link
curl -X POST \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"prompt":"Threat Defense security lab"}' \
     $API/resolve

```md
## 🤖  Integrating with AI agents
See [docs/AI_INTEGRATION.md](docs/AI_INTEGRATION.md) for a drop-in LangChain example.


### 🧑‍💻 Example: driving the router from LangChain
```bash
python examples/langchain_demo.py