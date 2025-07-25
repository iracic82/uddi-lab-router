# examples/langchain_demo.py
from langchain.tools.openapi import RequestsToolkit
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent

BASE_URL = "http://localhost:8000"          # or your prod URL
API_KEY  = "mysecret"                       # same key you set in .env

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

toolkit = RequestsToolkit.from_openapi_spec(
    f"{BASE_URL}/openapi.json",
    headers={"Authorization": f"Bearer {API_KEY}"}
)

agent = initialize_agent(
    tools=toolkit.to_tool_list(),
    llm=llm,
    verbose=True,
)

print(
    agent.run("Give me an invite for the Threat Defense security lab")
)
