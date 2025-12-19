import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests
from datetime import datetime

load_dotenv()

def log_event(event: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    if "logs" not in st.session_state:
        st.session_state.logs = []
    st.session_state.logs.append(f"[{timestamp}] {event}")

@tool
def calculator(expression: str) -> str:
    """
    Solves arithmetic expressions safely.
    """
    log_event(f"Calculator called with: {expression}")
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def read_file(filepath: str) -> str:
    """
    Reads a text file and returns its contents as a string.
    """
    log_event(f"File reader called with: {filepath}")
    try:
        with open(filepath, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: Cannot read file ({str(e)})"

@tool
def get_weather(city: str) -> str:
    """
    Fetches current weather information for a given city using OpenWeather API.
    """
    log_event(f"Weather tool called for city: {city}")
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OPENWEATHER_API_KEY not set"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return f"Error: City not found or API error ({response.status_code})"
        data = response.json()
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error: Could not fetch weather ({str(e)})"

@tool
def knowledge_lookup(query: str) -> str:
    """
    Provides answers to general knowledge questions using the LLM.
    """
    log_event(f"Knowledge lookup called with: {query}")
    return f"Searching knowledge for: {query}"

# ---------------- STREAMLIT UI ----------------

st.set_page_config(page_title="Agent with Tools", layout="wide")
st.title("🤖 LangChain Agent with Tools (Streamlit)")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "logs" not in st.session_state:
    st.session_state.logs = []

# ---------------- MODEL ----------------

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- AGENT ----------------

agent = create_agent(
    model=llm,
    tools=[calculator, read_file, get_weather, knowledge_lookup],
    system_prompt=(
        "You are a helpful assistant. "
        "Use tools only when required. "
        "Otherwise answer directly."
    )
)

user_input = st.text_input("Ask something:")

if st.button("Send") and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    log_event(f"User input received: {user_input}")

    try:
        result = agent.invoke({"messages": st.session_state.messages})
        # Store the returned messages (LangChain objects)
        st.session_state.messages = result["messages"]
    except Exception as e:
        log_event(f"Error calling agent: {str(e)}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Chat")
    for msg in st.session_state.messages:
        # Handle LangChain message objects
        if hasattr(msg, "type") and hasattr(msg, "content"):
            role = msg.type.upper()
            content = msg.content
        else:
            role = msg.get("role", "UNKNOWN").upper()
            content = msg.get("content", "")
        st.markdown(f"**{role}:** {content}")

with col2:
    st.subheader("🧠 Tool & Agent Logs")
    for log in st.session_state.logs:
        st.code(log)

st.subheader("📜 Raw Message History (Tool Flow)")
st.json([
    {
        "role": getattr(m, "type", "UNKNOWN").upper(),
        "content": getattr(m, "content", "")
    }
    for m in st.session_state.messages
])
