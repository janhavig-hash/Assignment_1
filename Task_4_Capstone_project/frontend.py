import streamlit as st
import requests

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api"
st.set_page_config(page_title="Tax Assistant AI", page_icon="⚖️")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .chat-answer {
        font-size: 1.1em;
        line-height: 1.6;
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: UPLOAD ---
with st.sidebar:
    st.title("📂 Document Upload")
    uploaded_file = st.file_uploader("Upload Form-16 / ITR", type=["pdf"])
    
    if uploaded_file and st.button("Process Document"):
        with st.spinner("Encrypting and indexing..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            try:
                response = requests.post(f"{API_URL}/upload", files=files)
                if response.status_code == 200:
                    st.success("✅ Indexing Complete!")
                else:
                    st.error("❌ Upload Failed")
            except Exception as e:
                st.error(f"Server Error: {e}")

# --- MAIN CHAT ---
st.header("⚖️ AI Personal Tax Assistant")

# Initialize History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History (Only Text, No Citations)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        # Use custom class for Assistant, normal text for User
        if msg["role"] == "assistant":
            st.markdown(f"<div class='chat-answer'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.write(msg["content"])

# User Input
if prompt := st.chat_input("Ask about your tax..."):
    # 1. Show User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. Get Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            try:
                payload = {"question": prompt}
                response = requests.post(f"{API_URL}/query", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    
                    # Display Answer (The text already contains the Page Number)
                    message_placeholder.markdown(f"<div class='chat-answer'>{answer}</div>", unsafe_allow_html=True)
                    
                    # Save ONLY the answer to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer
                    })
                
                else:
                    st.error("I couldn't find an answer.")
            
            except Exception as e:
                st.error(f"Connection Failed: {e}")