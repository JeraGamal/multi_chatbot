from sentence_transformers import SentenceTransformer
import chromadb

model = SentenceTransformer("all-MiniLM-L6-v2")  # Example model
client = chromadb.Client()

# Process document and store embeddings
def process_and_store_document(document: str, chatbot_id: int):
    chunks = document.split("\n\n")  # Simple split by paragraphs
    embeddings = model.encode(chunks)
    collection = client.get_or_create_collection(f"chatbot_{chatbot_id}")
    for idx, chunk in enumerate(chunks):
        collection.add(ids=[f"{chatbot_id}_{idx}"], documents=[chunk], embeddings=[embeddings[idx]])
    return {"message": "Document processed and stored"}

