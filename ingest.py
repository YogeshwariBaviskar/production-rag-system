import os
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Text → Semantic Vector
model = SentenceTransformer("all-MiniLM-L6-v2")

def load_documents(folder):
    docs = []
    for file in os.listdir(folder):
        with open(os.path.join(folder, file)) as f:
            docs.append(f.read())
    return docs

def chunk_text(text, chunk_size=200):
    # Split long documents into smaller pieces
    words = text.split()
    return [
        " ".join(words[i:i+chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

def build_index(docs):

    chunks = []
    for doc in docs:
        chunks.extend(chunk_text(doc))

    embeddings = model.encode(chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim) # Brute force similarity search using Euclidean distance
    index.add(np.array(embeddings))

    faiss.write_index(index, "vector.index")

    with open("chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

# MAIN EXECUTION
if __name__ == "__main__":

    folder = "documents"
    print("Loading documents...")
    docs = load_documents(folder)
    print("Total documents:", len(docs))

    print("Building vector index...")
    build_index(docs)