import streamlit as st
import os
from openai import OpenAI

st.title("Chat with LLama")

# Modify OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = os.getenv('OPENAI_API_BASE')
model = os.getenv('MODEL')
all_response=''

def get_response(user_prompt):

    global all_response

    client = OpenAI(
        api_key=openai_api_key,
        base_url=openai_api_base,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_prompt},
        ],
        stream=True 
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            all_response = all_response + str(content)
            yield content

if "messages" not in st.session_state.keys(): 
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question !"}
    ]

if prompt := st.chat_input("Your question"): 
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            st.write_stream(get_response(prompt))
            message = {"role": "assistant", "content": all_response}
            st.session_state.messages.append(message) 


