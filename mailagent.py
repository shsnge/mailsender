# agent.py
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from ddgs import DDGS
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

# --- Config ---
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER", "zeshanabduljabbar@gmail.com")
EMAIL_PASS = os.getenv("EMAIL_PASS", "jmkc fung kcyp vcrv")  # better to load from env vars

# --- LLM ---
llm = ChatGoogleGenerativeAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    model="gemini-2.5-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

# --- Tools ---
def searchOnInternet(query: str):
    """Search the internet for a query."""
    results = DDGS().text(query, max_results=5)
    return results

def send_email(to: str, subject: str, body: str):
    """Send an email to a recipient."""
    msg = EmailMessage()
    msg["From"] = EMAIL_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        return {"status": "sent", "to": to, "subject": subject}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# --- Memory ---
memory = InMemorySaver()

# --- Agent ---
agent = create_react_agent(
    model=llm,
    tools=[searchOnInternet, send_email],
    prompt="You are a helpful assistant who can search the internet and send emails.",
    checkpointer=memory
)
