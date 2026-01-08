import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/search"

st.set_page_config(page_title="Vector Search Demo", layout="centered")

st.title("🔍 Vector Database Semantic Search")
st.write("Search documents using vector embeddings.")

# Inputs
query = st.text_input("Enter your search query:")
top_k = st.slider("Number of results", min_value=1, max_value=10, value=3)

# Button
if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        payload = {
            "query": query,
            "top_k": top_k
        }

        try:
            with st.spinner("Searching..."):
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                data = response.json()

            results = data.get("results", [])

            if not results:
                st.info("No results found.")
            else:
                st.success(f"Found {len(results)} results")

                for idx, text in enumerate(results, start=1):
                    st.markdown(
                        f"""
                        ### 🔹 Result {idx}
                        {text}
                        ---
                        """
                    )

        except requests.exceptions.ConnectionError:
            st.error("❌ Backend API is not running. Please start FastAPI server.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
