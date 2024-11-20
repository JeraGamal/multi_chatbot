import os
import uuid
import PyPDF2
import nltk
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb
import markdown2

class DocumentProcessor:
    def __init__(self):
        # Download necessary NLTK resources
        nltk.download('punkt')
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize Chroma client for vector storage
        self.chroma_client = chromadb.Client()

    def preprocess_document(self, file_path: str) -> str:
        """
        Preprocess document based on file type
        Supports PDF, TXT, and Markdown
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_extension == '.pdf':
                return self._process_pdf(file_path)
            elif file_extension == '.txt':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_extension in ['.md', '.markdown']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return markdown2.markdown(f.read())
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        except Exception as e:
            raise ValueError(f"Error processing document: {str(e)}")

    def _process_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return ' '.join([page.extract_text() for page in reader.pages])

    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """
        Split text into chunks for embedding
        """
        # Use NLTK to split into sentences
        sentences = nltk.sent_tokenize(text)
        
        chunks = []
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            if current_length + len(sentence) > chunk_size:
                chunks.append(' '.join(current_chunk))
                current_chunk = [sentence]
                current_length = len(sentence)
            else:
                current_chunk.append(sentence)
                current_length += len(sentence)
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def generate_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks
        """
        return self.embedding_model.encode(chunks).tolist()

    def store_embeddings(self, chatbot_id: int, chunks: List[str], embeddings: List[List[float]]):
        """
        Store embeddings in Chroma vector database
        """
        collection = self.chroma_client.get_or_create_collection(f"chatbot_{chatbot_id}")
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            collection.add(
                ids=[f"{chatbot_id}_{i}"],
                documents=[chunk],
                embeddings=[embedding]
            )

    def semantic_search(self, chatbot_id: int, query: str, top_k: int = 3) -> List[str]:
        """
        Perform semantic search on stored embeddings
        """
        collection = self.chroma_client.get_collection(f"chatbot_{chatbot_id}")
        query_embedding = self.embedding_model.encode([query])[0]
        
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        
        return results['documents'][0]
