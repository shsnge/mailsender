# app.py
import streamlit as st
from mailagent import agent



# Keep chat history in session state
if 'messages' not in st.session_state:
    st.session_state['messages'] = []





st.markdown("---")
st.subheader("Send Email Directly")

with st.form("email_form"):
    to_email = st.text_input("Recipient Email:")
    subject = st.text_input("Subject:")
    body = st.text_area("Body:")
    send_btn = st.form_submit_button("Send Email")

if send_btn and to_email and subject and body:
    # Build the instruction for the agent
    instruction = f"Send an email to {to_email} with subject '{subject}' and body '{body}'"
    st.session_state['messages'].append({"role": "user", "content": instruction})
    with st.spinner("Agent is sending email..."):
        response = agent.invoke(
            {"messages": st.session_state['messages']},
            config={"configurable": {"thread_id": "user123"}}
        )
    agent_message = response['messages'][-1].content
    st.session_state['messages'].append({"role": "assistant", "content": agent_message})
    st.success("Email instruction sent to agent. Check response below.")

