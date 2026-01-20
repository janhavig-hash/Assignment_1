import streamlit as st
import requests
import uuid

# --- CONFIGURATION ---
API_URL = "http://127.0.0.1:8000/api" 
st.set_page_config(page_title="Tax Assistant AI", page_icon="⚖️")

# --- INITIALIZE SESSION STATE ---
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

if "file_passwords" not in st.session_state:
    st.session_state.file_passwords = {}

if "processing" not in st.session_state:
    st.session_state.processing = False

# --- CUSTOM CSS ---
st.markdown("""
<style>
    .chat-answer {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: UPLOAD ---
with st.sidebar:
    st.title("📂 Document Upload")
    st.caption(f"Session: {st.session_state.session_id[:8]}")
    
    uploaded_files = st.file_uploader(
        "Upload Form-16 / ITR", 
        type=["pdf"], 
        accept_multiple_files=True
    )
    
    # BUTTON LOGIC: Sets a flag so the loop runs even after refresh
    if uploaded_files and st.button("Process Documents"):
        st.session_state.processing = True
    
    # THE PROCESSING LOOP (Controlled by Flag, not just Button)
    if st.session_state.processing and uploaded_files:
        progress_bar = st.progress(0)
        status_area = st.empty()
        
        all_success = True # Track if we are done
        
        for idx, file in enumerate(uploaded_files):
            status_area.text(f"Processing {file.name}...")
            
            # 1. Reset File Pointer (Crucial)
            file.seek(0)
            
            # 2. Prepare Data
            data_payload = {"session_id": st.session_state.session_id}
            
            # 3. Inject Password if it exists in State
            if file.name in st.session_state.file_passwords:
                data_payload["password"] = st.session_state.file_passwords[file.name]
            
            try:
                files_payload = {"file": (file.name, file, "application/pdf")}
                response = requests.post(f"{API_URL}/upload", files=files_payload, data=data_payload)
                
                if response.status_code == 200:
                    st.success(f"✅ {file.name} Indexed!")
                
                elif response.status_code in [422, 400]:
                    all_success = False # We hit a snag
                    st.error(f"🔒 Password Required for {file.name}")
                    
                    # CALLBACK FUNCTION to Save Password
                    def save_pass():
                        st.session_state.file_passwords[file.name] = st.session_state[f"pw_{file.name}"]
                    
                    # The Password Input
                    st.text_input(
                        f"Enter password for {file.name} & PRESS ENTER:",
                        type="password",
                        key=f"pw_{file.name}",
                        on_change=save_pass # <--- This saves it BEFORE reload
                    )
                    
                    # Stop here so user can type. Loop will resume on reload because 'processing' is True
                    st.warning("⚠️ Enter password above and press ENTER.")
                    st.stop()
                        
                else:
                    st.error(f"❌ {file.name} Error: {response.json().get('detail')}")
                    
            except Exception as e:
                st.error(f"Server Error: {e}")
            
            progress_bar.progress((idx + 1) / len(uploaded_files))
        
        status_area.empty()
        
        # Only turn off processing if everything succeeded
        if all_success:
            st.session_state.processing = False
            # REPLACED BALLOONS WITH PROFESSIONAL TOAST
            st.toast("Document processing complete!", icon="✅")

# --- MAIN CHAT ---
st.header("⚖️ AI Personal Tax Assistant")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f"<div class='chat-answer'>{msg['content']}</div>", unsafe_allow_html=True)
            if "citations" in msg and msg["citations"]:
                with st.expander("📚 View Sources"):
                    for cit in msg["citations"]:
                        st.markdown(f"- **Page {cit['page']}** ({cit['source']}): _{cit['text']}..._")
        else:
            st.write(msg["content"])

if prompt := st.chat_input("Ask about your tax documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            try:
                payload = {"question": prompt, "session_id": st.session_state.session_id}
                response = requests.post(f"{API_URL}/query", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.markdown(f"<div class='chat-answer'>{data['answer']}</div>", unsafe_allow_html=True)
                    if data.get("citations"):
                        with st.expander("📚 View Sources"):
                            for cit in data["citations"]:
                                st.markdown(f"- **Page {cit['page']}** ({cit['source']}): _{cit['text']}..._")
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": data["answer"], 
                        "citations": data.get("citations")
                    })
                else:
                    st.error(f"Error: {response.json().get('detail')}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
