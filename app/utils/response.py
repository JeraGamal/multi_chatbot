def generate_response(query: str, chatbot_id: int):
    collection = client.get_collection(f"chatbot_{chatbot_id}")
    results = collection.query(query_texts=[query], n_results=3)
    context = " ".join(results["documents"])
    # Use a GPT-like model here for response
    response = f"Context: {context}\n\nResponse: I'm not integrated with GPT yet!"
    return response

