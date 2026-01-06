import streamlit as st
import chromadb
import pandas as pd
from src.backend.core.settings import settings

st.set_page_config(page_title="AutoCode MD - DB Viewer", layout="wide")
st.title("🧠 AutoCode MD Database Viewer")

# Connect to DB
try:
    client = chromadb.HttpClient(host=settings.CHROMA_HOST, port=settings.CHROMA_PORT)
    st.success(f"Connected to ChromaDB at {settings.CHROMA_HOST}:{settings.CHROMA_PORT}")

    # List Collections
    collections = client.list_collections()
    col_names = [c.name if hasattr(c, 'name') else c for c in collections]

    selected_col = st.selectbox("Select Collection", col_names)

    if selected_col:
        collection = client.get_collection(selected_col)
        count = collection.count()
        st.metric(label="Total Documents", value=count)

        # Show Data
        st.subheader("Last 10 Added Chunks")
        data = collection.peek(limit=10)

        # Create a clean table
        if data['ids']:
            df = pd.DataFrame({
                'ID': data['ids'],
                'Content': data['documents'],
                'Metadata': [str(m) for m in data['metadatas']]
            })
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Collection is empty.")

except Exception as e:
    st.error(f"Connection Error: {e}")
    st.info("Tip: Is Docker running? Try 'docker-compose up -d'")