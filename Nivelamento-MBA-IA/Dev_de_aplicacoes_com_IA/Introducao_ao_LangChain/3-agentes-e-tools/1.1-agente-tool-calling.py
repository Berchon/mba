from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import tool

load_dotenv()

# -----------------------------
# Tools
# -----------------------------

@tool
def calculator(expression: str) -> str:
    """Evaluate a simple mathematical expression and return the result as a string."""
    try:
        result = eval(expression)
    except Exception as e:
        return f"Error: {e}"

    result += 3
    return str(result)

@tool
def web_search_mock(query: str) -> str:
    """Return the capital of a given country if it exists in the mock data."""
    data = {
        "Brazil": "Brasíliaaa",
        "France": "Paris",
        "Germany": "Berlin",
        "Italy": "Rome",
        "Spain": "Madrid",
        "United States": "Washington, D.C."
    }

    for country, capital in data.items():
        if country.lower() in query.lower():
            return f"The capital of {country} is {capital}."

    return "I don't know the capital of that country."

tools = [calculator, web_search_mock]

# -----------------------------
# LLM
# -----------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)

# -----------------------------
# Prompt (chat-based)
# -----------------------------

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an assistant that can only answer questions using the provided tools. "
     "The tools are the only source of truth. "
     "If a tool does not provide the answer, say 'I don't know'. "
     "You are forbidden from using any prior knowledge or searching the internet."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

# -----------------------------
# Agent
# -----------------------------

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# -----------------------------
# Tests
# -----------------------------

print(agent_executor.invoke({"input": "What is the capital of Iran?"}))
print(agent_executor.invoke({"input": "What is the capital of Brazil?"}))
print(agent_executor.invoke({"input": "How much is 10 + 10?"}))
