import streamlit as st
from openai import OpenAI

st.subheader("Multi-Domain AI Assistant (Week 10 Lab)")

# ---------------------------
#   DOMAIN SYSTEM PROMPTS
# ---------------------------
DOMAIN_PROMPTS = {
    "Cybersecurity": "You are a cybersecurity expert. Help with threats, incidents, malware, and remediation.",
    "Data Science": "You are a data science expert. Help with ML, statistics, data cleaning, and Python code.",
    "IT Operations": "You are an IT operations expert. Help with servers, networks, troubleshooting, and deployments."
}

# ---------------------------
#   OPENAI CLIENT
# ---------------------------
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("❌ ERROR: OPENAI_API_KEY missing in .streamlit/secrets.toml")
    st.stop()

# ---------------------------
#   SIDEBAR — Domain Selector
# ---------------------------
st.sidebar.header("Domain Selector")
domain = st.sidebar.selectbox(
    "Choose a Domain",
    ["Cybersecurity", "Data Science", "IT Operations"]
)

# ---------------------------
#   INITIALISE CHAT STORAGE
# ---------------------------
if "messages" not in st.session_state:
    st.session_state.messages = {}

# Create chat history for selected domain
if domain not in st.session_state.messages:
    st.session_state.messages[domain] = [
        {"role": "system", "content": DOMAIN_PROMPTS[domain]}
    ]

domain_messages = st.session_state.messages[domain]

# ---------------------------
#   DISPLAY CHAT HISTORY
# ---------------------------
for msg in domain_messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------
#   USER INPUT
# ---------------------------
prompt = st.chat_input("Ask something...")

if prompt:
    # Show user's message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Save user's message
    domain_messages.append({"role": "user", "content": prompt})

    # ---------------------------
    #   STREAMING OPENAI RESPONSE
    # ---------------------------
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_reply = ""

        try:
            stream = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=domain_messages,
                stream=True
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_reply += chunk.choices[0].delta.content
                    placeholder.write(full_reply + "▌")

            placeholder.write(full_reply)

        except Exception as e:
            placeholder.write(f"❌ Error: {e}")
            full_reply = "API Error."

    # Save assistant response
    domain_messages.append({"role": "assistant", "content": full_reply})

# Save updated messages back
st.session_state.messages[domain] = domain_messages
