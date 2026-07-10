import os
from supabase.client import Client, create_client
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore

def get_vector_store():
    """Initializes the connection to Supabase and the Embedding model."""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY") 
    
    supabase: Client = create_client(supabase_url, supabase_key)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    vector_store = SupabaseVectorStore(
        client=supabase,
        embedding=embeddings,
        table_name="documents",
        query_name="match_documents"
    )
    return vector_store

def clear_db():
    """Deletes all previous records from the documents table to refresh it."""
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    
    # This deletes all rows where ID is greater than 0 (which is everything)
    supabase.table("documents").delete().gt("id", 0).execute()
    print("Database cleared successfully!")

def add_chunks_to_db(chunks):
    """Embeds and uploads chunks to Supabase."""
    vector_store = get_vector_store()
    vector_store.add_texts(texts=chunks)