from openai import OpenAI
import streamlit as st


# Show intro initially
if "intro_visible" not in st.session_state:
    st.session_state["intro_visible"] = True

st.title("Dennis AI Chat Bot :raising_hand_man:")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": st.secrets.INIT_PROMPT}]

if st.session_state["intro_visible"]:
    st.markdown("Hi! You have found an AI chat bot imitation of me. Type something to get started!")

client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)


# Display chat messages from conversation
for message in st.session_state.messages[1:]:
    if message["role"] == 'assistant':
        with st.chat_message(message["role"], avatar='./sqskog.png'):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Say something!"):
    st.session_state["intro_visible"] = False
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Model response
    response = client.chat.completions.create(
        model=st.secrets.MODEL,
        messages=st.session_state.messages
    )

    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar='./sqskog.png'):
        st.markdown(response.choices[0].message.content)

    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})

    
