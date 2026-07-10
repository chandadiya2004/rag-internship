import os
from langchain_groq import ChatGroq

# Using langchain_classic to maintain support for traditional retrieval chains
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate
from vector_store import get_vector_store

def get_rag_chain():
    """Builds the retrieval and LLM generation chain using your chosen model configuration."""
    
    # Initialize Groq LLM with the new model configuration you grabbed from the playground
    llm = ChatGroq(
        model_name="qwen/qwen3-32b", 
        temperature=0.6,               # Adjusted to matching your playground settings
        api_key=os.environ.get("GROQ_API_KEY")
    )
    
    # Setup Retriever (Fetches top 3 most relevant chunks)
    vector_store = get_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Create Prompt Template
    system_prompt = (
        "You are a helpful and polite College Admission Assistant. "
        "Use the provided context from the college brochure to answer the user's question. "
        "If you do not know the answer based on the context, politely state that the information "
        "is not available in the provided documents.\n\n"
        "Context:\n{context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Combine everything into a RAG chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain